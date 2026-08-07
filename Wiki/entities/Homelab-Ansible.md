---
type: entity
date_created: 2026-08-07
date_updated: 2026-08-07
tags:
  - wiki/entity
  - project/infrastructure
  - infrastructure/local
  - status/active
  - tech/ansible
  - tech/docker
  - tech/nginx
source_count: 1
---

# Homelab-Ansible

Infrastructure-as-code automation for a single powerful monolith server (192.168.1.17, Ubuntu, AMD Ryzen 9 5900XT, NVIDIA RTX 2070 SUPER) using Ansible and Docker Compose. Orchestrates media server stack (Jellyfin, Pi-hole, OpenVPN, Tailscale) and application containers using modern Compose V2. Demonstrates local-first architecture with VRAM-conscious GPU acceleration.

## Purpose

Declarative infrastructure automation for a home media server and services lab. Replace manual server configuration with reproducible Ansible playbooks that define 10+ services on a single Ubuntu host using Docker Compose.

## Core Architecture

**Three-Layer Architecture:**
```
Ansible Playbook (main.yml)
    ↓ (defines desired state)
Docker Compose Configuration
    ├─ Media Services (Jellyfin, Pi-hole, etc.)
    ├─ Application Services (Portainer, Nginx Proxy Manager)
    └─ Monitoring Services (optional)
    ↓
Docker Engine (standalone, NOT Swarm)
    ├─ Docker Bridge Network (172.18.0.0/16)
    └─ Services with persistent storage
    ↓
Host Storage
    ├─ Local NVMe (OS, container state)
    └─ External USB SSDs mounted at /mnt/ssd_media
```

**Why This Design:**
- Single-node orchestration (no cluster complexity)
- Docker Compose V2 (modern, industry standard)
- Ansible (agentless, idempotent)
- GPU acceleration via NVIDIA container toolkit
- Persistent storage via local mounts + UUID-based fstab

## Key Features

- **Declarative Infrastructure** — Ansible playbooks define all state
- **Docker Compose V2** — Modern Compose with proper syntax
- **Multi-Service Orchestration** — 10+ services on single host
- **GPU Acceleration** — NVIDIA RTX 2070 SUPER via nvidia-container-toolkit
- **Reverse Proxy** — Nginx Proxy Manager for domain-based routing
- **DNS Management** — Pi-hole for LAN DNS + ad blocking
- **VPN Access** — OpenVPN Access Server + Tailscale
- **Media Server** — Jellyfin for home video streaming
- **Monitoring** — Portainer for container management
- **Data Preservation** — USB SSD mounting with nofail option

## Tech Stack

- **Orchestration:** Ansible 2.10+
- **Container Runtime:** Docker Engine (standalone, not Swarm)
- **Compose:** Docker Compose V2 (space-separated command)
- **Host OS:** Ubuntu 22.04 LTS
- **Server IP:** 192.168.1.17
- **GPU:** NVIDIA RTX 2070 SUPER (8GB VRAM)
- **Python:** 3.12 (Ansible + custom modules)
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
│   └── [other roles...]
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

**NOT a Cluster:**
- ❌ No Swarm mode
- ❌ No manager/worker nodes
- ❌ No overlay networks
- ❌ No service placement constraints
- ✅ Standalone Docker Engine
- ✅ Docker Bridge networking for service-to-service traffic

**All Services on One Host (192.168.1.17):**
- Container-to-container via container names on bridge network
- Host-mode containers for privileged operations (OpenVPN, Tailscale)
- GPU via nvidia-container-toolkit on host

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
# For services in host mode (OpenVPN, Tailscale)
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

## Deployment Model

**Main Playbook:**
```bash
ansible-playbook main.yml -i inventory.yml
```

**What It Does:**
1. Read all variables from vars.yml
2. Execute role for each service
3. Deploy Compose stack via docker compose up -d
4. Run post-deploy tasks (wait_for_container, configure pihole, etc.)
5. Idempotent: Safe to run multiple times

**Feature Branch Deployment:**
- Ansible supports per-branch configurations
- Each branch can deploy to separate environment
- Tested via GitHub Actions before merging

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
| Jellyfin | Media streaming | jellyfin_config | ✅ | bridge |
| Pi-hole | DNS + ad-blocking | pihole_config | ❌ | bridge |
| OpenVPN | VPN access | (custom) | ❌ | host |
| Tailscale | Mesh VPN | (custom) | ❌ | host |
| Nginx Proxy Manager | Reverse proxy | nginx_proxy_manager_config | ❌ | bridge |
| Portainer | Container management | (portal) | ❌ | bridge |
| Media Server Stack | RAG + search | (stack_deployer) | ❌ | bridge |

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
- Simpler than Swarm (no raft consensus, no leader election)
- Powerful single machine (Ryzen 9 5900XT, 16GB RAM)
- Idempotent Ansible (safe to re-apply)
- Media services don't need clustering

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

## Open Questions

- [Add monitoring/alerting (Prometheus + Grafana)?]
- [Implement automated backup for Pi-hole configs?]
- [Add Wireguard VPN (alternative to OpenVPN)?]
- [Separate media storage pool into its own compose stack?]

## Key Files

- **Main Playbook:** [main.yml](main.yml)
- **Inventory:** [inventory.yml](inventory.yml)
- **Variables:** [vars.yml](vars.yml)
- **Stack Deployer Role:** [roles/stack_deployer/tasks/main.yml](roles/stack_deployer/tasks/main.yml)
- **Nginx Config Role:** [roles/nginx_proxy_manager_config/tasks/main.yml](roles/nginx_proxy_manager_config/tasks/main.yml)
- **Pi-hole Config Role:** [roles/pihole_config/tasks/main.yml](roles/pihole_config/tasks/main.yml)

## Sources

- Wiki source: Project repository scan on 2026-08-07
- README analysis from `/home/thatsmidnight/projects/Homelab-Ansible`
- Copilot instructions from `.github/copilot-instructions.md` (comprehensive guidelines)
- Docker Compose V2 documentation
- Ansible documentation
