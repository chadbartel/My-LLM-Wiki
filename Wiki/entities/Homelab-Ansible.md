---
type: entity
date_created: 2026-08-07
date_updated: 2026-10-06
tags:
  - wiki/entity
  - project/infrastructure
  - infrastructure/local
  - status/active
  - tech/ansible
  - tech/docker
  - tech/nginx
  - tech/tailscale
source_count: 2
---

# Homelab-Ansible

Infrastructure-as-code automation for a single powerful monolith server (192.168.1.17, Ubuntu, AMD Ryzen 9 5900XT, NVIDIA RTX 2070 SUPER) using Ansible and Docker Compose. Orchestrates a growing media/application stack (Jellyfin, Bazarr, Pi-hole, Ollama + Open WebUI, Dispatcharr, RetroArch, Audiobookshelf) plus native Tailscale VPN, all via modern Compose V2. Demonstrates local-first architecture with VRAM-conscious GPU acceleration.

## Purpose

Declarative infrastructure automation for a home media server and services lab. Replace manual server configuration with reproducible Ansible playbooks that define 13+ roles / 10+ containerized services on a single Ubuntu host using Docker Compose.

## Recent Changes (as of 2026-08-14)

Since the last deep review (2026-08-07), the repo has grown substantially — recent PR history (`git log --oneline`) shows:

- **#43 Monolith Docker hardening and subnet-routing updates** — bootstrap/deploy phase split, Tailscale subnet router hardening
- **#42 Feat/audiobookshelf** — new `audiobookshelf` role (audiobook/ebook server)
- **#41 fix/jellyiptvtuner**
- **#40 Feat/retroarch** — new `retroarch` role (GPU-accelerated emulation via KasmVNC)
- **#39 Feat/dispatcharr** — new `dispatcharr` role (IPTV/VOD platform, GPU transcoding)
- **#38 Feat/ollama** — Ollama + Open WebUI local LLM stack added
- **#37 Feat/bazarr** — Bazarr subtitle management added
- **#36 Feat/tailscale** — native Tailscale role replacing the earlier Docker-based OpenVPN/Tailscale approach
- **#35 Feat/monolith**, **#34 Fix/vpn idempotency**, **#33 Fix/npm restart**, **#32 Fix homelab**

**Net effect:** OpenVPN is gone from the current architecture — VPN access is now handled entirely by the native **Tailscale** role (exit node + subnet router mode, `192.168.1.0/24` advertised). A `pihole_api` role was also added providing full Pi-hole REST API v6.0 coverage (80+ endpoints), largely to fix a DNS rate-limiting incident (see `docs/PIHOLE_RATE_LIMIT_INCIDENT.md`, referenced from README).

## Core Architecture

> **CORRECTION (2026-10-06):** Verified by direct source review (`grep` across the full repo) — most of the stack runs under **Docker Swarm**, not standalone Docker as earlier versions of this page claimed. Evidence: `main.yml`/`stack_deployer` deploy via `docker stack deploy`; a custom module `library/docker_swarm_container_exec.py` execs into Swarm-managed containers; and four post-deploy roles (`jellyfin_config`, `pihole_config`, `nginx_proxy_manager_config`, `koffan_config`) explicitly auto-discover their target container **in Docker Swarm** (`tasks/common/set_swarm_manager.yml`, `tasks/common/wait_for_swarm_service.yml`). The README itself describes the project as "Docker, Docker Swarm, Portainer, and various services." **Exception:** the `audiobookshelf` role is explicitly documented as pure standalone Compose with "No Swarm dependencies." The sections below are retained for history but should be read with this correction in mind.

**Three-Layer Architecture:**
```
Ansible Playbook (main.yml)
    ↓ (defines desired state, tags: bootstrap | deploy)
Docker Compose Configuration (templated .yml.j2)
    ├─ Media Services (Jellyfin, Pi-hole, etc.)
    ├─ Application Services (Portainer, Nginx Proxy Manager)
    └─ Monitoring Services (optional)
    ↓
Docker Swarm (single-node swarm; `docker stack deploy` / Portainer Swarm API)
    ├─ homelab-bridge overlay/bridge network
    └─ Services with persistent storage
    │  (exception: audiobookshelf runs as plain standalone Compose, no Swarm)
    ↓
Host Storage
    ├─ Local NVMe (OS, container state)
    └─ External USB SSDs mounted at /mnt/ssd_media
```

**Why This Design:**
- Single-node Swarm (no multi-node cluster complexity, but still gets Swarm's service reconciliation/restart semantics)
- Docker Compose V2 syntax, translated to Swarm stacks by `stack_deployer`
- Ansible (agentless, idempotent)
- GPU acceleration via NVIDIA container toolkit
- Persistent storage via local mounts + UUID-based fstab

## Key Features

- **Declarative Infrastructure** — Ansible playbooks define all state
- **Docker Compose V2** — Modern Compose with proper syntax
- **Multi-Service Orchestration** — 10+ services on single host
- **GPU Acceleration** — NVIDIA RTX 2070 SUPER via nvidia-container-toolkit
- **Reverse Proxy** — Nginx Proxy Manager for domain-based routing
- **DNS Management** — Pi-hole for LAN DNS + ad blocking, managed via native `pihole_config` role plus a full `pihole_api` role (Pi-hole REST API v6.0, 80+ endpoints)
- **VPN Access** — Native Tailscale (exit node + subnet router mode); OpenVPN has been removed from the architecture
- **Media Server** — Jellyfin (video), Bazarr (subtitles), Audiobookshelf (audiobooks/ebooks), Dispatcharr (IPTV/VOD), RetroArch (GPU-accelerated emulation via KasmVNC)
- **Local LLM** — Ollama + Open WebUI stack for local model inference
- **Monitoring** — Portainer for container management (no Prometheus/Grafana stack)
- **Data Preservation** — USB SSD mounting with nofail option, tiered storage (NVMe for Docker data, USB SSDs for bulk media)

## Tech Stack

- **Orchestration:** Ansible 2.10+
- **Container Runtime:** Docker Engine (standalone, not Swarm)
- **Compose:** Docker Compose V2 (space-separated command)
- **Host OS:** Ubuntu (NVIDIA driver 550 series referenced, Ubuntu 24.04-compatible)
- **Server IP:** 192.168.1.17 ("monolith")
- **GPU:** NVIDIA RTX 2070 SUPER (8GB VRAM) — used by Jellyfin, Dispatcharr, RetroArch
- **Python:** 3.11 (venv at `/opt/homelab-ansible`) + custom Ansible modules
- **VPN:** Native Tailscale (not Dockerized)
- **Dynamic DNS:** DuckDNS (`chadbartel.duckdns.org`)
- **Key Collections:** community.docker, community.general

## Architecture

**Project Structure:**
```
homelab-ansible/
├── main.yml                          # Main playbook orchestrator
├── handler.yml                       # EventBridge handler (optional)
├── ansible.cfg                       # Ansible config (inventory, roles_path)
├── inventory.yml                     # Host definitions (192.168.1.17)
├── vars.yml                          # Global variables
├── pyproject.toml                    # Python dependencies
├── Makefile                          # Task automation
├── roles/
│   ├── stack_deployer/              # Generic Compose deployment
│   │   ├── tasks/
│   │   │   ├── direct/              # Deploy via docker compose
│   │   │   └── portainer/           # Deploy via Portainer API
│   │   └── templates/
│   │       └── docker-compose.yml.j2
│   ├── nginx_proxy_manager_config/   # Reverse proxy configuration
│   │   ├── tasks/
│   │   │   └── fix_host_network_upstreams.yml  # Auto-fix for host-mode containers
│   │   └── templates/
│   ├── pihole_config/                # DNS + ad-blocking configuration
│   │   ├── tasks/
│   │   │   ├── add_adlists.yml
│   │   │   ├── setup_pihole.yml
│   │   │   └── configure_dns_records.yml
│   │   └── templates/
│   ├── jellyfin_config/              # Media server tuning
│   │   └── tasks/
│   │       └── enable_gpu_transcoding.yml
│   ├── pihole_api/                   # Pi-hole REST API v6.0 client (80+ endpoints, rate-limit fixes)
│   ├── tailscale/                    # Native Tailscale VPN (exit node + subnet router)
│   ├── dispatcharr/                  # IPTV/VOD platform (GPU transcoding, modular web/db/redis/celery)
│   ├── retroarch/                    # GPU-accelerated emulator frontend (KasmVNC web UI)
│   ├── audiobookshelf/               # Audiobook/ebook server
│   ├── jellyctl/                     # CLI wrapper role for jellyfin management
│   └── koffan_config/                # Post-setup role for a grocery/koffan app (NFS backup optional)
├── group_vars/
│   └── monolith.yml                  # Host-specific variables
├── host_vars/
│   └── [host-specific configs]
├── tasks/
│   └── common/
│       ├── wait_for_container.yml    # Health check pattern
│       └── [other common tasks]
└── templates/
    ├── pihole-compose.yml.j2         # Pi-hole + DNS configuration
    ├── jellyfin-compose.yml.j2       # Jellyfin with GPU
    └── [other Compose templates]
```

**Key Pattern:** Each service (Jellyfin, Pi-hole, etc.) has:
1. Compose template with jinja2 variables
2. Role with post-deploy configuration tasks
3. Variables in group_vars/monolith.yml
4. Orchestrated by main.yml

## Single-Node Architecture

**Single-Node, But Swarm-Mode (see correction above):**
- ✅ Docker Swarm initialized on the one host (`manager_node_ip`); the stack is deployed via `docker stack deploy` / Portainer's Swarm API, not plain `docker compose up`
- ✅ No additional manager/worker nodes — it's a one-node Swarm, so none of Swarm's multi-node scheduling/HA benefits apply, just the stack-management API surface
- ✅ `homelab-bridge` Docker network for service-to-service traffic
- ✅ Post-deploy roles use `docker_swarm_container_exec` (custom module) for idempotent `docker exec` into Swarm-managed containers
- ❌ No multi-node placement constraints or node labels in use
- ⚠️ `audiobookshelf` is the one role that deliberately opts out of Swarm and runs plain standalone Compose

**All Services on One Host (192.168.1.17):**
- Container-to-container via container names on bridge network (`homelab-bridge`)
- Host-mode containers for privileged operations (Tailscale runs natively on the host, not in a container)
- GPU via nvidia-container-toolkit on host
- Deployment is split into two explicit phases in `main.yml`: **bootstrap** (system prep, drivers, Tailscale, storage mounts — no containers started) and **deploy** (network creation, Portainer, Dispatcharr, Compose stacks via `tasks/deploy_stacks.yml`)

## Storage Architecture

**Local Storage:**
- OS and container state on NVMe
- Fast for container operations

**External Media Storage:**
- USB SSDs mounted locally (not NFS)
- Path: /mnt/ssd_media
- Mounted via /etc/fstab with UUID entries
- nofail option prevents boot failures if disconnected
- Bind-mounted into containers

**Data Preservation Rule:**
- ⚠️ CRITICAL: Never suggest destructive disk operations
- External SSDs store irreplaceable media
- USB mounts assumed to be working correctly
- Infrastructure changes must preserve media

## Reverse Proxy Patterns

**Bridge Network Services (Container Name Routing):**
```yaml
# For services on homelab-bridge network (172.18.0.0/16)
proxy_hosts:
  - domain: jellyfin.chadbartel.com
    forward_host: jellyfin              # Container name
    forward_port: 8096                  # Container internal port
```

**Host Network Services (Gateway IP Routing):**
```yaml
# For services in host mode (e.g. native Tailscale)
proxy_hosts:
  - domain: vpn.chadbartel.com
    forward_host: 172.18.0.1            # Docker bridge gateway IP
    forward_port: 943                   # Port on host network
```

**Why the Exception:**
- Bridge network containers can reach each other by name
- Host-mode containers not on bridge network
- Gateway IP provides route from bridge to host network stack
- Automatic fix via `fix_host_network_upstreams.yml` task

## GPU Acceleration

**Hardware:**
- NVIDIA RTX 2070 SUPER (8GB VRAM)
- Supports video transcoding acceleration

**Container Configuration:**
```yaml
# In docker-compose.yml
services:
  jellyfin:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

**Why Not `runtime: nvidia`:**
- ❌ Deprecated in Compose v1.29+
- ✅ Modern approach: device reservations

**VRAM Management:**
- Single GPU shared across services
- Jellyfin gets priority (4-5GB transcode + 1GB model)
- Other services backoff or share GPU time

## DNS Architecture

**Pi-hole (Local DNS + Ad Blocking):**
1. Runs on homelab-bridge network (container name: pihole)
2. Listens on 192.168.1.17:53 (DNS port)
3. Provides DNS for all local devices
4. Ad-list blocking (EasyList, etc.)
5. Custom DNS records for internal services

**Critical Requirement:**
- Every service proxied via Nginx Proxy Manager needs DNS entry
- DNS entry resolves domain to 192.168.1.17
- Entry stored in `/etc/pihole/custom.list`
- **IMPORTANT:** Three locations must be synchronized:
  1. `templates/pihole-compose.yml.j2` in `FTLCONF_dns_hosts`
  2. `group_vars/monolith.yml` in `proxy_hosts` list
  3. `vars.yml` in `pihole_config_custom_dns_entries`

**Missing DNS Entry = 502 Bad Gateway**
- If you add new service to Nginx Proxy Manager
- But forget DNS entry
- Result: Domain resolution fails or times out
- Add to all three locations immediately

**Pi-hole API Role (`pihole_api`):**
- Full Pi-hole REST API v6.0 client (80+ endpoints): config, domains, clients, groups, stats, Teleporter export/import
- Added specifically to fix a DNS rate-limiting incident — default `FTLCONF_dns_rateLimit` was too aggressive for the number of clients on the LAN
- Current setting: `pihole_rate_limit_count: 2000` queries per `pihole_rate_limit_interval: 60` seconds (10x the Pi-hole default of ~200/60s)
- Includes ready-made playbooks: `roles/pihole_api/examples/rate_limit_fix.yml` and `identify_rate_limit_source.yml`

## Deployment Model

**Main Playbook:**
```bash
ansible-playbook main.yml -i inventory.yml --ask-vault-pass
```

**What It Does:**
1. Read all variables from vars.yml / vault.yml
2. `--tags bootstrap`: system prep, Docker/NVIDIA install, Tailscale, storage mounts (no containers started)
3. `--tags deploy`: create `homelab-bridge` network, deploy Portainer, Dispatcharr, then all remaining stacks via `stack_deployer` — which runs `docker stack deploy` (direct backend, default) or the Portainer Swarm API, **not** plain `docker compose up -d`
4. Run post-deploy tasks (`tasks/post_setup_*.yml`, each delegating to the matching `*_config` role) to finish setup wizards and API configuration
5. Idempotent: Safe to run multiple times; post-deploy roles check existing state before re-applying

**Feature Branch Deployment:**
- Ansible supports per-branch configurations
- Each branch can deploy to separate environment
- Tested via GitHub Actions before merging

## Custom Ansible Modules

Three custom modules live under `roles/*/library/` or the top-level `library/`, built because no stock Ansible module fit the need:

- **`docker_swarm_container_exec`** ([library/docker_swarm_container_exec.py](Homelab-Ansible/library/docker_swarm_container_exec.py)) — Runs a shell command inside a Swarm-managed container via `docker exec`, with Ansible-style `creates`/`removes` idempotency guards (stock `docker_container_exec`/`shell` modules don't support this for containerized commands). Used heavily by `pihole_config` (adlists, custom DNS, dnsmasq tasks).
- **`jellyfin_api`** (in the `jellyfin` role) — Generic Jellyfin API v10.11.6 client: takes `endpoint`/`method`/`query_params`/`body` and handles both API-token and username/password auth, avoiding manual JSON construction in tasks.
- **`pihole_api`** (in the `pihole_api` role) — Full Pi-hole REST API v6.0 client covering 80+ endpoints (auth/session, config, domains, clients, groups, lists, DHCP, Teleporter backup/restore, gravity updates) with automatic session/auth reuse.

## Operational Playbooks

Standalone playbooks under `playbooks/`, run independently of `main.yml`, for diagnostics and lifecycle operations:

| Playbook | Purpose |
|----------|---------|
| `playbooks/debug.yml` | Diagnostics: Docker version, service status, **Swarm status**, running containers, host info |
| `playbooks/destroy.yml` | ⚠️ Full teardown of the Docker Swarm configuration and deployed stacks — gated behind typing the literal confirmation phrase `NUCLEAR_ANNIHILATION` |
| `playbooks/prepare_ssd_media.yml` | Mounts/prepares the USB SSD media drives without running a full deployment |
| `playbooks/test-ssh.yml` | Verifies SSH connectivity to all inventory hosts before a real run |

## Bash Scripts & SSH Workflow

`bash_scripts/` plus `Makefile` targets wrap the raw `ansible-playbook` invocations:

- **`setup-ssh.sh`** — Starts/reuses an SSH agent, loads the deploy key (`SSH_AGENT_TIMEOUT=3600`), persists agent info to `~/.ssh-agent-info`, and tests connectivity to inventory hosts.
- **`ansible-wrapper.sh`** — Sources the saved SSH agent info and verifies keys are loaded before any `ansible-playbook` call, avoiding silent permission-denied failures.
- **`troubleshoot-ssh.sh`** — Diagnoses SSH agent/key/connectivity problems per host.
- **`validate.sh`** — Pre-deployment sanity check: confirms core files (`main.yml`, `ansible.cfg`, `vars.yml`, `vault.yml`, `inventory.yml`, `requirements.yml`) and expected directories/task/template files all exist.
- **`fix-docker-socket.sh`** — Repairs Docker socket permission/connectivity issues, including restarting affected Swarm services.

Typical `Makefile` targets: `make setup-ssh`, `make deploy`, `make deploy-roles`, `make debug`, `make test`, `make teardown-swarm`, `make destroy`, `make validate`, `make lint`.

## Cost Model

**Hardware:**
- Monolith: Amortized cost (already owned)
- No AWS cost for media services
- Power consumption: ~200W (electricity cost ~$30/month)

**No Cloud Cost:**
- All media services local
- No ingress/egress fees
- Only optional: Tailscale exit node (free for home use)

**Total:** Power cost only (~$30/month)

## Services Orchestrated

| Service | Purpose | Role | GPU | Network |
|---------|---------|------|-----|---------|
| Jellyfin | Media streaming (port 8096) | jellyfin, jellyfin_config, jellyctl | ✅ | bridge |
| Bazarr | Subtitle management (port 6767) | (stack_deployer) | ❌ | bridge |
| Pi-hole | DNS + ad-blocking (web 8081, DNS 53/80) | pihole_config, pihole_api | ❌ | bridge |
| Dispatcharr | IPTV/VOD platform (port 9191) | dispatcharr | ✅ | bridge |
| RetroArch | Emulation via KasmVNC (port 3000) | retroarch | ✅ | bridge |
| Audiobookshelf | Audiobook/ebook server (port 13378) | audiobookshelf | ❌ | bridge |
| Ollama | Local LLM inference (port 11434) | (stack_deployer) | ✅ (shared) | bridge |
| Open WebUI | LLM chat frontend | (stack_deployer) | ❌ | bridge, public via `chat.chadbartel.duckdns.org` |
| Tailscale | Mesh VPN, exit node + subnet router | tailscale | ❌ | native (host) |
| Nginx Proxy Manager | Reverse proxy (admin port 81) | nginx_proxy_manager_config | ❌ | bridge |
| Portainer | Container management (HTTPS 9443) | (main.yml direct) | ❌ | bridge |
| koffan | Grocery/list app (custom) | koffan_config | ❌ | bridge |

**Removed from architecture:** OpenVPN Access Server (superseded by native Tailscale, PR #36 `Feat/tailscale`).

## Getting Started

```bash
git clone [repo-url]
cd homelab-ansible
poetry install

# Configure target host
# Edit inventory.yml to point to your server (default: 192.168.1.17)

# Run playbook
poetry run ansible-playbook main.yml -i inventory.yml

# Verify
# Check services on host:
ssh 192.168.1.17 docker ps
curl http://192.168.1.17:53  # Pi-hole DNS test
curl http://192.168.1.17:8096  # Jellyfin test
```

## Maintenance

**Regular:**
- Monitor container health (docker ps on host)
- Check Pi-hole ad-blocking stats
- Monitor Jellyfin transcode performance
- Verify VPN connectivity

**Periodic:**
- Update Ansible playbooks
- Update Docker images (security patches)
- Monitor storage usage on USB SSDs
- Audit Nginx Proxy Manager rules

**Troubleshooting:**
- "502 Bad Gateway" → Check DNS entry in Pi-hole custom.list
- Container crash loops → Check logs: `docker logs container-name`
- No internet from container → Verify bridge network DNS
- GPU not available → Check nvidia-container-toolkit installation

## Key Insights

**Single-Node Philosophy:**
- Single-node Swarm, not a standalone-vs-Swarm choice (see correction in Core Architecture) — one node means no raft consensus overhead across multiple managers, but the stack still gets Swarm's service reconciliation and restart semantics
- Powerful single machine (Ryzen 9 5900XT, 16GB RAM)
- Idempotent Ansible (safe to re-apply)
- Media services don't need multi-node clustering

**Ansible Strengths:**
- Agentless (no daemons on host)
- Idempotent (safe to run multiple times)
- Declarative (what, not how)
- Template-driven (DRY principle)

**Docker Compose V2:**
- Modern standard (replaces docker-compose binary)
- Integrated into Docker CLI (`docker compose`)
- Better UX than Swarm for single-node
- YAML format (version: '3.9+' modern syntax)

## Related Concepts

- [[AWS Infrastructure Ecosystem]] — Contrast with cloud (this is local-first)
- [[Docker-Based Infrastructure]] — Container orchestration patterns
- [[Home Lab Design]] — Single-node philosophy
- [[NVIDIA GPU Acceleration]] — GPU sharing patterns
- [[Wiki/concepts/Idempotent Swarm Post-Deploy Configuration Pattern]] — Discover-wait-configure-validate pattern used by jellyfin_config, pihole_config, nginx_proxy_manager_config, koffan_config

## Open Questions — Resolved (as of 2026-08-14)

- **Wireguard VPN (alternative to OpenVPN)?** → Resolved differently: OpenVPN was removed entirely in favor of a native **Tailscale** role (exit node + subnet router mode). No Wireguard role exists.
- **Separate media storage pool into its own compose stack?** → Not a separate stack, but storage is now clearly tiered: NVMe (`docker_data_device`) for `/var/lib/docker`, and two USB SSDs (`/mnt/ssd_media`, `/mnt/ssd_media2`) mounted by device ID for bulk media, shared across all service containers via `shared_storage_mounts`.

## Open Questions — Still Open

- [Add monitoring/alerting (Prometheus + Grafana)?] — Still not implemented; only Portainer's built-in stats and `docker logs`/`docker stats` are available.
- [Implement automated backup for Pi-hole configs?] — Still no cron/scheduled backup. The `pihole_api` role exposes Teleporter export/import tasks, but nothing calls them on a schedule.
- [Formalize `docs/` folder referenced in README (e.g. `docs/PIHOLE_RATE_LIMIT_INCIDENT.md`)?] — README links to it but no `docs/` directory currently exists in the repo; likely dropped or never committed.
- [Add automated NFS backup for other stateful services beyond koffan?] — Only `koffan_config` currently supports an optional NFS backup path.

## Key Files

- **Main Playbook:** [main.yml](main.yml)
- **Inventory:** [inventory.yml](inventory.yml)
- **Variables:** [vars.yml](vars.yml)
- **Group Vars:** [group_vars/monolith.yml](group_vars/monolith.yml)
- **Stack Deployer Role:** [roles/stack_deployer/tasks/main.yml](roles/stack_deployer/tasks/main.yml)
- **Nginx Config Role:** [roles/nginx_proxy_manager_config/tasks/main.yml](roles/nginx_proxy_manager_config/tasks/main.yml)
- **Pi-hole Config Role:** [roles/pihole_config/tasks/main.yml](roles/pihole_config/tasks/main.yml)
- **Pi-hole API Role:** [roles/pihole_api/README.md](roles/pihole_api/README.md)
- **Tailscale Role:** [roles/tailscale](roles/tailscale)
- **Dispatcharr Role:** [roles/dispatcharr/README.md](roles/dispatcharr/README.md)
- **RetroArch Role:** [roles/retroarch](roles/retroarch)
- **Audiobookshelf Role:** [roles/audiobookshelf/README.md](roles/audiobookshelf/README.md)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- Deep repository re-review on 2026-08-14 (roles, main.yml, vars, git log through PR #43)
- Full systematic repo review on 2026-10-06: every role, task file, playbook, custom module, template, and bash script read directly; corrected the Docker Swarm vs. standalone contradiction via `grep` verification across the full source tree
- README analysis from `/home/thatsmidnight/projects/Homelab-Ansible`
- Copilot instructions from `.github/copilot-instructions.md` (comprehensive guidelines)
- Docker Compose V2 documentation
- Ansible documentation
