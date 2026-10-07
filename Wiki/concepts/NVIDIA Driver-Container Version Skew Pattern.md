---
type: concept
date_created: 2026-10-06
tags:
  - wiki/concept
  - tech/nvidia
  - tech/docker
  - tech/ansible
---

# NVIDIA Driver-Container Version Skew Pattern

A chain of failure modes that occurs when NVIDIA driver packages are upgraded (via `apt`) on a long-running Linux host, and the fixes required at each layer before GPU containers work again. Discovered and verified live on [[Homelab-Ansible]]'s `monolith` host (2026-10-06).

## Why this happens

`apt upgrade`-ing `nvidia-driver-*` packages only replaces files **on disk**. It does not, by itself, fix three other places where the old version lingers:

1. **The kernel module already resident in memory** — `modprobe`/`insmod` only runs once; an apt upgrade doesn't unload and reload the module that's currently running. NVML (used by `nvidia-smi`, `nvidia-persistenced`, `nvidia-container-cli`) talks to *that* in-memory module, so it reports the *old* version until something explicitly unloads and reloads it.
2. **The dynamic linker cache (`/etc/ld.so.cache`)** — dpkg's `ldconfig` trigger isn't always reliable when several `nvidia-*` packages upgrade in one transaction. The cache can keep pointing at a versioned `.so` file (e.g. `libEGL_nvidia.so.<old-version>`) that the upgrade already deleted.
3. **Long-running daemons that cache GPU/device state in memory** — `dockerd`/`containerd` resolve GPU devices and library mount lists once and keep them for the life of the process. A daemon that's been running since before the driver change keeps handing containers a stale mount list regardless of what's now correct on disk.
4. **Already-created containers** — a GPU-reserved container (`deploy.resources.reservations.devices: driver: nvidia`) bakes its NVIDIA library mount list into its own OCI config **at creation time**. If creation happened while the driver was in a stale state, that bad mount list is permanently stuck in that specific container object — `docker start`/`compose up` on the *same* container reuses the stored config and will fail forever, even after every other layer above is fixed. It must be removed and recreated fresh.

## Diagnostic signature (by layer)

| Layer | Symptom |
|---|---|
| Kernel module | `nvidia-smi`: `Failed to initialize NVML: Driver/library version mismatch`; `dmesg`: `NVRM: API mismatch: the client '<proc>' ...` |
| `/dev` nodes missing (headless, no X/udev trigger) | `nvidia-persistenced` journal: `Failed to query NVIDIA devices. Please ensure that the NVIDIA device files (/dev/nvidia*) exist...` |
| `nvidia-modprobe` binary missing | systemd: `Unable to locate executable '/usr/bin/nvidia-modprobe'` |
| DKMS module not built for running kernel | `dkms status -k $(uname -r)` doesn't show `installed`; usually missing `linux-headers-$(uname -r)` at install time, or Secure Boot rejecting the unsigned module |
| Stale ld cache | GPU container fails with `OCI runtime create failed: ... open /usr/lib/x86_64-linux-gnu/libEGL_nvidia.so.<old-version>: no such file or directory` |
| Stale already-created container | Same error as above, persists even after `ldconfig`, kernel module reload, *and* confirming `ldconfig -p` / `nvidia-container-cli info` all report the new version — only clears after `docker rm -f` + recreate |

## Verified remediation order

1. Ensure `linux-headers-{{ ansible_kernel }}` is installed **before** the driver packages (so DKMS builds cleanly on first install).
2. `dkms autoinstall` + `dkms status -k {{ ansible_kernel }}` check — fail fast with an actionable message (Secure Boot / missing headers) instead of a cryptic systemd error later.
3. `ldconfig` immediately after the driver apt task, unconditionally — cheap, idempotent, closes the ld-cache gap.
4. Compare `modinfo -F version nvidia` (on-disk) vs the version parsed from `/proc/driver/nvidia/version` (loaded). If they differ: stop `nvidia-persistenced`, `modprobe -r nvidia_uvm nvidia_drm nvidia_modeset nvidia`, `modprobe` them back in order, then restart Docker (see step 6). Safe to do without a reboot as long as nothing is actively holding `/dev/nvidia*` (check at a bootstrap phase before containers start).
5. `nvidia-modprobe -c0 -u` to (re)create `/dev/nvidia*` device nodes on headless hosts with no X/udev trigger. Make this self-healing via a systemd drop-in (`ExecStartPre=-/usr/bin/nvidia-modprobe -c0 -u` on `nvidia-persistenced.service`) so it survives future reboots, not just this run.
6. Restart the Docker daemon whenever the kernel module was reloaded — it may have been running since long before the driver change and will otherwise keep serving a stale GPU device cache to every container it creates from here on.
7. For any GPU-reserved container service: before `docker compose up`, check each GPU container's running state and `docker rm` any found in a **non-running** state (e.g. `Created` but never `Started`). A compose config-hash diff alone will not catch this, because the compose definition hasn't changed — only the container's internal (bad) cached mount list has gone stale.

## Related

- [[Homelab-Ansible]] — where this was discovered and fixed (`tasks/initial_setup.yml`, `roles/dispatcharr/tasks/main.yml`)
- [[Idempotent Standalone-Docker Post-Deploy Configuration Pattern]] — sibling pattern for discover-wait-configure-validate idempotency on this same host

## Post-fix verification (2026-10-06)

Confirmed live over SSH after the fix deployed cleanly end-to-end:

- Jellyfin: `/dev/nvidia*` bind-mounted into the container, `jellyfin-ffmpeg -encoders` lists `h264_nvenc`/`hevc_nvenc`/`av1_nvenc`, and real playback sessions in the container logs show `-init_hw_device cuda=cu:0 -hwaccel cuda ... -codec:v:0 h264_nvenc` with clean `FFmpeg exited with code 0` completions.
- Dispatcharr: its own startup GPU self-check reports NVIDIA Container Toolkit detected, all 5/5 NVIDIA devices accessible, and `FFmpeg NVIDIA acceleration: AVAILABLE (cuda)`.

## Known non-issue: `dispatcharr-web` healthcheck is cosmetically "unhealthy"

`docker ps` shows `dispatcharr-web` as `(unhealthy)`. This is **unrelated** to this pattern and to GPU/transcoding — it's a pre-existing bug in [templates/dispatcharr-compose.yml.j2](Homelab-Ansible/templates/dispatcharr-compose.yml.j2) in [[Homelab-Ansible]]: the container's healthcheck Python script is wrapped in a YAML folded scalar (`>`), which collapses all newlines into spaces and destroys the script's required indentation, so the probe itself crashes with `IndentationError: unexpected indent` on every run. The container is otherwise fully functional (API, GPU access, transcoding all confirmed working); only the Docker-reported health status is wrong. Deliberately left unfixed (low priority, cosmetic only) — do not re-investigate this as a GPU/driver problem if seen again.
