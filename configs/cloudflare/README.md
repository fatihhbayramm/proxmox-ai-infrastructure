# Cloudflare Tunnel Configuration

## Setup Instructions

### 1. Install Cloudflared

On CF-Tunnel VM:

```bash
# Download and install
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify installation
cloudflared --version
```

### 2. Login to Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser. Select your domain.

### 3. Create Tunnel

```bash
# Create tunnel
cloudflared tunnel create ai-infrastructure

# List tunnels to get ID
cloudflared tunnel list
```

Save the tunnel ID and credentials file location.

### 4. Configure Tunnel

Copy `tunnel-config.yml` to `/root/.cloudflared/config.yml`:

```bash
sudo mkdir -p /root/.cloudflared
sudo cp tunnel-config.yml /root/.cloudflared/config.yml
```

Edit the file with your settings:

```bash
sudo nano /root/.cloudflared/config.yml
```

### 5. Create DNS Records

For each hostname in your config:

```bash
cloudflared tunnel route dns ai-infrastructure ai.yourdomain.com
cloudflared tunnel route dns ai-infrastructure n8n.yourdomain.com
cloudflared tunnel route dns ai-infrastructure ollama.yourdomain.com
cloudflared tunnel route dns ai-infrastructure portainer.yourdomain.com
cloudflared tunnel route dns ai-infrastructure pve1.yourdomain.com
cloudflared tunnel route dns ai-infrastructure ssh.yourdomain.com
```

### 6. Run Tunnel

Test first:

```bash
cloudflared tunnel run ai-infrastructure
```

If working, install as service:

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### 7. Verify

Check status:

```bash
sudo systemctl status cloudflared
```

Check logs:

```bash
sudo journalctl -u cloudflared -f
```

## Troubleshooting

### Tunnel Not Starting

```bash
# Check config syntax
cloudflared tunnel ingress validate

# Check DNS
nslookup ai.yourdomain.com
```

### Service Not Accessible

```bash
# Test local connectivity
curl http://192.168.1.125:3000

# Check firewall
sudo ufw status
```

### Certificate Issues

```bash
# Regenerate certificate
cloudflared tunnel login
```
