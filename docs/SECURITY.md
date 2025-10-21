🔒 Security Best Practices
Comprehensive security guide for your AI infrastructure.
📋 Table of Contents

Overview
Network Security
Access Control
Data Protection
Container Security
Monitoring & Logging
Compliance

Overview
Security Layers
┌─────────────────────────────────────────┐
│  Layer 1: Cloudflare (DDoS, WAF)       │
├─────────────────────────────────────────┤
│  Layer 2: Zero Trust Access (Optional)  │
├─────────────────────────────────────────┤
│  Layer 3: Cloudflare Tunnel (TLS)      │
├─────────────────────────────────────────┤
│  Layer 4: Firewall (UFW)                │
├─────────────────────────────────────────┤
│  Layer 5: Docker Network Isolation      │
├─────────────────────────────────────────┤
│  Layer 6: Application Authentication    │
└─────────────────────────────────────────┘

Network Security
Cloudflare Tunnel Benefits
✅ Zero open ports - No direct internet exposure
✅ DDoS protection - Cloudflare's global network
✅ TLS encryption - End-to-end HTTPS
✅ No public IP needed - Works behind NAT
Firewall Configuration
Enable UFW (Uncomplicated Firewall):
bashsudo apt install ufw

# Default policies

sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)

sudo ufw allow 22/tcp

# Allow from local network only

sudo ufw allow from 192.168.1.0/24

# Enable firewall

sudo ufw enable

# Check status

sudo ufw status verbose
Network Isolation
Docker network isolation:
yaml# docker-compose.yml
networks:
  ai-network:
    internal: true  # No external access
    driver: bridge
  
  public-network:
    driver: bridge
Proxmox firewall:

Datacenter → Firewall → Options
Enable firewall
Create rules:

Input: DROP (default)
Allow: SSH from specific IPs
Allow: Internal network traffic

Access Control
SSH Security

1. Disable password authentication:
bashsudo nano /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no
bashsudo systemctl restart sshd
2. Use SSH keys:
bash# Generate key pair (on your machine)
ssh-keygen -t ed25519 -C "<your_email@example.com>"

# Copy to server

ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Test

ssh -i ~/.ssh/id_ed25519 user@server
3. Change default SSH port (optional):
bashsudo nano /etc/ssh/sshd_config

# Change: Port 22 → Port 2222

sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp
sudo systemctl restart sshd
4. Install fail2ban:
bashsudo apt install fail2ban

# Configure

sudo nano /etc/fail2ban/jail.local
ini[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
bashsudo systemctl enable fail2ban
sudo systemctl start fail2ban
Cloudflare Access (Zero Trust)
Enable Zero Trust authentication:

Cloudflare Dashboard → Zero Trust → Access
Create Application:

Name: AI Infrastructure
Subdomain: ai, n8n
Policy: Email OTP or SSO

Add users/groups
Save and test

Example policy:

Allow: Specific emails
Require: Email verification
Session duration: 24 hours

Application Authentication
Open WebUI:
Enable in docker-compose.yml:
yamlenvironment:

- WEBUI_AUTH=true
First user becomes admin.
n8n:
Set credentials:
yamlenvironment:
- N8N_BASIC_AUTH_ACTIVE=true
- N8N
