---
name: hybrid-desktop-server-ops
description: "Comprehensive runbook and operational architecture for running a single Linux machine as both a daily development desktop and a 24/7 home/cloud server (Debian/Ubuntu, GNOME, Docker, Caddy, Cloudflare Tunnels, ZeroTier/Tailscale, AdGuard Home, and CLI utilities)."
author: DevOps / Linux Community
---

# Hybrid Desktop + 24/7 Server Architecture & Operations

This skill guides the setup, maintenance, networking, storage, and optimization of a Linux machine (Debian/Ubuntu/GNOME) functioning simultaneously as a **daily-driver development workstation** and a **24/7 headless home/cloud server**.

---

## 1. Core Architecture Overview

In a dual-role Linux setup, the system balances graphical desktop productivity with persistent server services across multiple network interfaces.

```
                    ┌────────────────────────────────────────────────────────┐
                    │               INTERNET / EXTERNAL ACCESS              │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
                                    [Cloudflare Tunnel]
                               (Public Domains: *.domain.com)
                                                │
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                LINUX HYBRID HOST (Debian)                                  │
│                                                                                            │
│  ┌───────────────────────┐  ┌─────────────────────────────┐  ┌──────────────────────────┐ │
│  │   LAN (192.168.0.x)   │  │   Tailscale (100.x.x.x)     │  │   ZeroTier (172.26.x.x)  │ │
│  └───────────┬───────────┘  └──────────────┬──────────────┘  └────────────┬─────────────┘ │
│              │                             │                              │               │
│              └─────────────────────────────┼──────────────────────────────┘               │
│                                            ▼                                              │
│                                  [Caddy Reverse Proxy]                                    │
│                             (Private Routes & tls internal)                               │
│                                            │                                              │
│                    ┌───────────────────────┴───────────────────────┐                      │
│                    ▼                                               ▼                      │
│         [Internal Web Services]                         [AdGuard Home DNS]                │
│    (FileBrowser, Cockpit, Relatex)                   (Port 53 DNS Sinkhole & BBR)         │
│                    │                                               │                      │
│                    ▼                                               ▼                      │
│         [Docker Storage Pool]                           [Modern CLI/TUI Tools]            │
│         (/home/docker-data)                           (lazygit, glances, ctop, agy)       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Kernel & System Tuning (24/7 Server Mode)

### Disabling Automatic Sleep & Suspend
To ensure the machine remains accessible 24/7 over the network without entering standby:

```bash
# 1. Mask systemd sleep & suspend targets
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# 2. Configure GNOME power management to prevent idle sleep
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 0
```

### Enabling Google TCP BBR + Fair Queuing (FQ)
BBR (Bottleneck Bandwidth and RTT) reduces bufferbloat and maximizes throughput for home/server network transfers:

```bash
sudo tee /etc/sysctl.d/99-bbr.conf << 'EOF'
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF

sudo /sbin/sysctl --system
```

Verify activation:
```bash
sudo /sbin/sysctl net.ipv4.tcp_congestion_control net.core.default_qdisc
# Output: net.ipv4.tcp_congestion_control = bbr, net.core.default_qdisc = fq
```

---

## 3. Storage Optimization & Docker Data-Root Migration

When running on partitioned drives where root (`/`) is small (e.g. 50–60 GB) and `/home` is large (e.g. 500 GB–1 TB), Docker and developer caches can quickly fill the root partition.

### Migrating Docker Data-Root to `/home`
Prevent Docker container layers, volumes, and images from consuming root storage:

1. Configure `/etc/docker/daemon.json`:
   ```json
   {
     "data-root": "/home/docker-data"
   }
   ```
2. Restart Docker service: `sudo systemctl restart docker`
3. Verify active root directory: `sudo docker info | grep -i "Root Dir"`
4. Remove obsolete leftover directory `/var/lib/docker` if lingering from previous setup.

### Safe Routine Cleanup Runbook
Reclaim 10–25 GB of disk space without deleting any projects or configuration:

```bash
# 1. Clean APT package cache and unneeded packages
sudo apt-get clean && sudo apt-get autoremove -y

# 2. Prune old systemd journal logs (keep last 3 days)
sudo journalctl --vacuum-time=3d

# 3. Prune Docker build caches and dangling images
sudo docker builder prune -a -f && sudo docker image prune -f

# 4. Clean developer test runners, browser caches, and desktop trash
rm -rf ~/.local/share/Trash/*
rm -rf ~/.cache/Cypress ~/.cache/ms-playwright ~/.cache/trivy
rm -rf ~/.cache/google-chrome ~/.cache/epiphany
rm -rf ~/.cache/pip ~/.cache/uv/archive
```

---

## 4. Multi-Interface Networking & Reverse Proxying

### Traffic Division: Public vs Internal
* **Public Services**: Use **Cloudflare Tunnels** (`cloudflared`) to expose specific domains (`*.domain.com`) through Cloudflare's edge with DDoS protection and automated TLS.
* **Internal Services**: Use **Caddy** as a local reverse proxy serving all private network interfaces (LAN `192.168.0.x`, Tailscale `100.x.x.x`, and ZeroTier `172.26.x.x`).

### Caddy Configuration (`/etc/caddy/Caddyfile`)
```caddy
{
    email user@example.com
    auto_https disable_redirects
}

# Local hostname with automatic internal TLS
filebrowser.home, files.lan {
    tls internal
    reverse_proxy localhost:8080
}

# Port mapping across all interfaces (LAN, Tailscale, ZeroTier)
:8443 {
    tls internal
    reverse_proxy localhost:4470
}

# Tailscale MagicDNS with cert
service.tailscale-domain.ts.net:9443 {
    tls /etc/tailscale-certs/cert.crt /etc/tailscale-certs/cert.key
    reverse_proxy localhost:4445
}
```

### ZeroTier & Tailscale Integration
* **ZeroTier One**: Join private/public mesh network: `sudo zerotier-cli join <nwid>`
* **Tailscale**: Connect with MagicDNS enabled: `sudo tailscale up`
* Host responds directly on virtual interfaces (`tailscale0` / `zteb...`) without port forwarding on physical router.

---

## 5. Network-Wide Adblocking & DNS Sinkhole (AdGuard Home)

Deploying a local DNS sinkhole blocks advertisements, telemetry, and tracking across all household devices (Smart TVs, mobile apps, consoles) and accelerates DNS queries via RAM caching.

### Docker Compose Deployment (`/home/pedro/docker/adguardhome/docker-compose.yml`)
```yaml
services:
  adguardhome:
    image: adguard/adguardhome:latest
    container_name: adguardhome
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "3000:3000/tcp"   # Setup wizard
      - "8085:80/tcp"     # Web Dashboard
      - "853:853/tcp"     # DNS-over-TLS
      - "784:784/udp"     # DNS-over-QUIC
    volumes:
      - ./work:/opt/adguardhome/work
      - ./conf:/opt/adguardhome/conf
    environment:
      - TZ=America/Sao_Paulo
```

### Upstream DNS Optimization
In AdGuard Home settings, configure fast, encrypted DNS-over-HTTPS (DoH) upstreams:
* `https://security.cloudflare-dns.com/dns-query`
* `https://dns.quad9.net/dns-query`

---

## 6. Modern Terminal & Server CLI Ecosystem

Essential CLI/TUI tools for server maintenance and fast desktop workflow:

| Tool | Type | Purpose | Shortcut / Alias |
| :--- | :--- | :--- | :--- |
| **`lazygit`** | TUI | Git branch, commit, and diff manager | `lg` |
| **`lazydocker`**| TUI | Container, compose, and log manager | `ld` |
| **`yazi`** | TUI | Blazing-fast terminal file manager | `yazi` |
| **`glances`** | TUI/Web | Full system hardware and sensor metrics | `glances` |
| **`ctop`** | TUI | Top-like container resource monitor | `ctop` |
| **`dive`** | TUI | Docker image layer explorer and optimizer | `dive <image>` |
| **`ncdu`** | TUI | Interactive disk space analyzer | `ncdu /` |
| **`gping`** | CLI | Graphical network latency graph | `gping <host>` |
| **`zoxide`** | CLI | Smarter `cd` with database memory | `z <folder>` |
| **`fzf`** | CLI | Fuzzy finder for command history (`Ctrl+R`) | `Ctrl+R` / `Ctrl+T` |
| **`eza`** | CLI | Modern `ls` with icons and git integration | `ls` / `ll` / `tree` |
| **`bat`** | CLI | `cat` with syntax highlighting | `cat` |
| **`delta`** | CLI | Side-by-side git diff pager | Integrated in `git diff` |
| **`tealdeer`** | CLI | Fast Rust `tldr` with practical examples | `tldr <cmd>` |
| **`duf`** | CLI | Partition and disk usage table | `du` |
| **`fastfetch`** | CLI | System information visualizer | `fetch` |
| **`FileBrowser`**| Web | Remote web-based file manager | `filebrowser -r /home` |
| **`Ntfy`** | CLI | Instant push notifications to phone/desktop| `ntfy publish <topic>` |

### Shell Integration Template (`~/.bashrc`)
```bash
# Integrations
if command -v zoxide >/dev/null 2>&1; then eval "$(zoxide init bash)"; fi
if command -v fzf >/dev/null 2>&1; then eval "$(fzf --bash 2>/dev/null)" || true; fi

# Aliases
alias lg="lazygit"
alias ld="lazydocker"
alias ls="eza --icons"
alias ll="eza -la --icons --git"
alias tree="eza --tree --icons"
alias cat="bat -p"
alias du="duf"
alias fetch="fastfetch"
```
