---
type: concept
date_created: 2026-10-06
date_updated: 2026-10-06
tags:
  - wiki/concept
  - infrastructure/local
  - pattern/architecture
  - tech/ansible
  - tech/docker
confidence: high
source_count: 1
---

# Idempotent Standalone-Docker Post-Deploy Configuration Pattern

Architectural pattern for configuring an application *after* its container is already running as **standalone Docker** (plain `docker ps`/`docker exec`, no Swarm), using a consistent workflow: discover the container, wait for readiness, configure idempotently, then validate.

> **Naming note:** The reference implementation below names its tasks/variables/modules with "swarm" (`*_swarm_manager`, `docker_swarm_container_exec`, role READMEs claiming "Docker Swarm environments"). Direct verification of the actual task bodies shows this is legacy/vestigial naming — the real discovery mechanism is plain `docker ps --filter name=...`, not any Swarm API, and Swarm mode is never initialized on the host. This page is named for what the code *does*, not what it's labeled.

## Definition

Many self-hosted apps don't support configuration purely through environment variables or compose-level settings — they need a setup wizard completed, an admin API called, or files written inside the running container. Doing this reliably in Ansible requires a repeatable sequence:

1. **Discover** — Find the running container by a known, fixed `container_name` set in the Compose template (e.g. `docker ps --filter "name=^jellyfin$"`). Because standalone Compose uses a fixed container name, this is a simple lookup, not a cluster-wide service query.
2. **Wait for readiness** — Poll the container/service (HTTP health check or port) until it actually accepts requests, since `docker compose up -d` returns before the app inside is ready.
3. **Configure idempotently** — Perform the one-time setup (wizard completion, API calls, file writes) only if not already done, usually by checking for an existing marker/resource first.
4. **Validate** — Confirm the configuration took effect (e.g. a follow-up read-back call) before marking the task successful.

## Why It Matters

**Problems it solves:**

| Problem | Without the pattern | With the pattern |
|---|---|---|
| Container lookup at runtime | Playbook hardcodes an assumed container ID | Dynamic lookup via `docker ps --filter name=...` each run, tolerant of container recreation |
| Startup race conditions | Playbook fails intermittently because app isn't ready yet | Explicit wait-for-readiness step before any configuration |
| Re-running playbooks | Setup wizard/API call re-run and either errors or duplicates state | Existence checks make every step a no-op on repeat runs |
| Debuggability | Silent partial configuration, no way to tell if it worked | Explicit validation step surfaces failures immediately |

## Reference Implementation — [[Wiki/entities/Homelab-Ansible]]

This pattern is implemented across four independent roles, each applying it to a different application. Verified by reading the actual task files (not just role READMEs):

| Role | App Configured | Discovery Mechanism (verified) | Step 3 Mechanism |
|---|---|---|---|
| `jellyfin_config` | Jellyfin media server | `tasks/discover_container.yml`, explicitly commented `# standalone Docker`, runs `docker ps --filter name=^jellyfin$` | Completes setup wizard, manages API keys (dedup-checked), configures libraries via the custom `jellyfin_api` module |
| `pihole_config` | Pi-hole DNS | Similar fixed-name `docker ps` lookup | Manages adlists (triggers gravity update), custom DNS entries, dnsmasq settings via the custom `docker_swarm_container_exec` module (name is legacy; it's just `docker exec` + idempotency guards) |
| `nginx_proxy_manager_config` | Nginx Proxy Manager | Fixed-name container lookup | Checks existing proxy hosts via NPM REST API v2.33.7 before creating new ones |
| `koffan_config` | Koffan grocery app | Fixed-name container lookup | Verifies API readiness, optional NFS backup setup |

**Supporting custom modules** (built because no stock Ansible module fit the need):
- `docker_swarm_container_exec` — `docker exec` into a container with `creates`/`removes` idempotency guards. Its own docstring states it works for "standalone or Swarm" containers; in this codebase it's always used against standalone containers.
- `jellyfin_api` / `pihole_api` — Generic REST clients for apps whose only configuration surface is an HTTP API.

**Dead code note:** `tasks/common/set_swarm_manager.yml` implements genuine Swarm-manager-node lookup (`groups['swarm_managers'][0]`), but `inventory.yml` defines no `swarm_managers` group and this task is never actually included in the live flow — it's orphaned, documented only in its own README example. It is **not** part of the pattern as actually executed.

## General Shape (pseudo-tasks, as actually implemented)

```yaml
- name: Discover container by fixed name
  ansible.builtin.shell: docker ps --filter "name=^{{ container_name }}$" --format '{{ "{{" }}.ID{{ "}}" }}'
  register: container_id_result

- name: Wait for service readiness
  include_tasks: tasks/common/wait_for_swarm_service.yml   # name is legacy; logic is a generic TCP/HTTP wait_for

- name: Check if already configured
  <api_or_module_call>:
    ...
  register: existing_state

- name: Apply configuration (only if needed)
  <api_or_module_call>:
    ...
  when: not existing_state.found

- name: Validate configuration took effect
  <api_or_module_call>:
    ...
  register: verification
  failed_when: not verification.success
```

## When To Use This Pattern

- The app's desired state can't be fully expressed in the Compose file itself (e.g. first-run setup wizards, admin API-only settings).
- Container names are fixed/known (standalone Compose with `container_name:` set) — discovery is a simple filtered lookup, not a cluster query.
- The playbook needs to be safely re-runnable without manual cleanup.

## When It's Overkill

- Apps that are fully configured via environment variables at container start (no post-deploy role needed — just set the right compose template variables).
- A genuine multi-node Swarm/Kubernetes cluster where container placement is dynamic — that scenario would actually need the Swarm-aware discovery this codebase's naming implies but doesn't contain.

## Related Concepts

- [[Wiki/entities/Homelab-Ansible]] — Source project implementing this pattern across four roles

## Sources

- Derived from a full systematic review of the Homelab-Ansible repository on 2026-10-06 (`tasks/common/`, `roles/jellyfin_config`, `roles/pihole_config`, `roles/nginx_proxy_manager_config`, `roles/koffan_config`, `library/docker_swarm_container_exec.py`)
- Corrected same-day after verifying actual task bodies (vs. role README/variable-name claims) showed standalone Docker, not Swarm

