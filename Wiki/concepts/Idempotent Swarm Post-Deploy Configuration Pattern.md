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

# Idempotent Swarm Post-Deploy Configuration Pattern

Architectural pattern for configuring an application *after* its container is already running in Docker Swarm, using a consistent four-step workflow: discover the container, wait for readiness, configure idempotently, then validate.

## Definition

Many self-hosted apps don't support configuration purely through environment variables or compose-level settings — they need a setup wizard completed, an admin API called, or files written inside the running container. Doing this reliably in Ansible requires a repeatable sequence:

1. **Discover** — Find the actual running container for a Swarm service (container ID, node, task ID), since Swarm can place a service's task on any point in time and the name/ID isn't static like a plain `docker run`.
2. **Wait for readiness** — Poll the container/service (HTTP health check or port) until it actually accepts requests, since `docker stack deploy` returns before the app inside is ready.
3. **Configure idempotently** — Perform the one-time setup (wizard completion, API calls, file writes) only if not already done, usually by checking for an existing marker/resource first.
4. **Validate** — Confirm the configuration took effect (e.g. a follow-up read-back call) before marking the task successful.

## Why It Matters

**Problems it solves:**

| Problem | Without the pattern | With the pattern |
|---|---|---|
| Container identity in Swarm | Hardcoded container name assumed to exist | Dynamic discovery via Swarm service lookup each run |
| Startup race conditions | Playbook fails intermittently because app isn't ready yet | Explicit wait-for-readiness step before any configuration |
| Re-running playbooks | Setup wizard/API call re-run and either errors or duplicates state | Existence checks make every step a no-op on repeat runs |
| Debuggability | Silent partial configuration, no way to tell if it worked | Explicit validation step surfaces failures immediately |

## Reference Implementation — [[Wiki/entities/Homelab-Ansible]]

This pattern is implemented as a reusable pair of common task files plus four independent roles that each apply it to a different application:

**Shared building blocks** (`tasks/common/`):
- `set_swarm_manager.yml` — Dynamic fact gathering to identify the Swarm manager node and target container.
- `wait_for_swarm_service.yml` — Generic polling task reused by all four config roles.

**Roles that apply the pattern:**

| Role | App Configured | Step 3 Mechanism |
|---|---|---|
| `jellyfin_config` | Jellyfin media server | Completes setup wizard, manages API keys (dedup-checked), configures libraries via the custom `jellyfin_api` module |
| `pihole_config` | Pi-hole DNS | Manages adlists (triggers gravity update), custom DNS entries, dnsmasq settings via the custom `docker_swarm_container_exec` module |
| `nginx_proxy_manager_config` | Nginx Proxy Manager | Checks existing proxy hosts via NPM REST API v2.33.7 before creating new ones |
| `koffan_config` | Koffan grocery app | Verifies API readiness, optional NFS backup setup |

**Supporting custom modules** (built because no stock Ansible module fit the need):
- `docker_swarm_container_exec` — `docker exec` into a Swarm-managed container with `creates`/`removes` idempotency guards.
- `jellyfin_api` / `pihole_api` — Generic REST clients for apps whose only configuration surface is an HTTP API.

## General Shape (pseudo-tasks)

```yaml
- name: Discover container in Docker Swarm
  include_tasks: tasks/common/set_swarm_manager.yml

- name: Wait for service readiness
  include_tasks: tasks/common/wait_for_swarm_service.yml

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

- The app's desired state can't be fully expressed in the Compose/stack file itself (e.g. first-run setup wizards, admin API-only settings).
- The app runs under Docker Swarm, where container identity isn't static across deploys/restarts.
- The playbook needs to be safely re-runnable without manual cleanup.

## When It's Overkill

- Apps that are fully configured via environment variables at container start (no post-deploy role needed — just set the right compose template variables).
- Standalone Compose (not Swarm) with a fixed, known container name — the "discover" step can be skipped, though "wait" and "validate" are still useful.

## Related Concepts

- [[Wiki/entities/Homelab-Ansible]] — Source project implementing this pattern across four roles

## Sources

- Derived from a full systematic review of the Homelab-Ansible repository on 2026-10-06 (`tasks/common/`, `roles/jellyfin_config`, `roles/pihole_config`, `roles/nginx_proxy_manager_config`, `roles/koffan_config`, `library/docker_swarm_container_exec.py`)
