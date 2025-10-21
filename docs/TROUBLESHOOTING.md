# 🔧 Troubleshooting Guide

Common issues and solutions for Proxmox AI Infrastructure.

## 📋 Quick Diagnostics

Run this comprehensive health check:

```bash
# Create health check script
curl -o health-check.sh https://raw.githubusercontent.com/fatihhbayramm/proxmox-ai-infrastructure/main/scripts/health-check.sh
chmod +x health-check.sh
./health-check.sh
```

---

## GPU Issues

### GPU Not Detected in VM

**Symptoms:**

- `lspci` doesn't show NVIDIA GPU
- `nvidia-smi` returns "No devices found"

**Solutions:**

1. **Verify IOMMU is enabled on host:**

```bash
# On Proxmox host
dmesg | grep -e DMAR -e IOMMU
```

2. **Check VFIO driver binding:**

```bash
# On Proxmox host
lspci -nnk | grep -i nvidia -A 3
```

Should show: `Kernel driver in use: vfio-pci`

3. **Verify VM configuration:**

```bash
# On Proxmox host
qm config 100 | grep hostpci
```

Should show: `hostpci0: 0000:01:00,pcie=1,x-vga=1`

4. **Restart VM with clear:**

```bash
qm stop 100
qm start 100
```

### NVIDIA Driver Installation Fails

**Symptoms:**

- Driver install errors
- `nvidia-smi` not found after installation

**Solutions:**

1. **Remove conflicting drivers:**

```bash
sudo apt purge -y nvidia-* libnvidia-*
sudo apt autoremove -y
sudo apt autoclean
```

2. **Reinstall from scratch:**

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt update
sudo apt install -y nvidia-driver-535
sudo reboot
```

3. **Check secure boot (must be disabled):**

```bash
mokutil --sb-state
# Should show: SecureBoot disabled
```

If enabled, disable in BIOS/UEFI settings.

### GPU Shows "No devices were found"

**Symptoms:**

- `nvidia-smi` returns error

**Solutions:**

1. **Check if driver is loaded:**

```bash
lsmod | grep nvidia
```

2. **Reload driver:**

```bash
sudo rmmod nvidia_uvm
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
sudo rmmod nvidia
sudo modprobe nvidia
```

3. **Check kernel logs:**

```bash
dmesg | grep -i nvidia
```

### GPU Memory Issues

**Symptoms:**

- Out of memory errors
- Slow performance

**Solutions:**

1. **Check GPU memory usage:**

```bash
nvidia-smi
```

2. **Use smaller models:**

```bash
# Instead of 13B models, use 7B
docker exec ollama ollama pull llama2:7b
```

3. **Limit context window in Open WebUI:**

- Settings → Models → Context Length: 2048

---

## Docker Issues

### Docker Containers Won't Start

**Symptoms:**

- `docker compose up -d` fails
- Containers exit immediately

**Solutions:**

1. **Check container logs:**

```bash
docker logs ollama
docker logs open-webui
docker logs n8n
```

2. **Check disk space:**

```bash
df -h
```

3. **Restart Docker:**

```bash
sudo systemctl restart docker
docker compose down
docker compose up -d
```

### GPU Not Available in Docker

**Symptoms:**

- Docker can't access GPU
- Ollama shows CPU-only mode

**Solutions:**

1. **Verify NVIDIA Container Toolkit:**

```bash
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

2. **Reconfigure Docker:**

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

3. **Check docker-compose.yml GPU config:**

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

### Port Already in Use

**Symptoms:**

- `Error: port 11434 already in use`

**Solutions:**

1. **Find process using port:**

```bash
sudo lsof -i :11434
```

2. **Kill process:**

```bash
sudo kill -9 <PID>
```

3. **Change port in docker-compose.yml:**

```yaml
ports:
  - "11435:11434"  # Use different external port
```

---

## Ollama Issues

### Ollama API Not Responding

**Symptoms:**

- `curl http://localhost:11434` fails
- Open WebUI can't connect

**Solutions:**

1. **Check Ollama is running:**

```bash
docker ps | grep ollama
```

2. **Restart Ollama:**

```bash
docker restart ollama
```

3. **Check Ollama logs:**

```bash
docker logs ollama -f
```

4. **Test API directly:**

```bash
curl http://localhost:11434/api/tags
```

### Model Download Fails

**Symptoms:**

- `ollama pull` hangs or fails
- Insufficient space error

**Solutions:**

1. **Check disk space:**

```bash
df -h
docker system df
```

2. **Clean Docker:**

```bash
docker system prune -a
```

3. **Download manually:**

```bash
docker exec -it ollama ollama pull llama2
```

4. **Check internet connection:**

```bash
ping -c 4 ollama.ai
```

### Slow Model Performance

**Symptoms:**

- Responses take very long
- Low tokens/second

**Solutions:**

1. **Check GPU usage:**

```bash
watch -n 1 nvidia-smi
```

2. **Verify GPU is being used:**

```bash
docker exec ollama ollama ps
# Should show GPU in output
```

3. **Use appropriate model size:**

- 4GB VRAM: 7B models only
- 6GB VRAM: 7B models, some 13B
- 8GB+ VRAM: Up to 13B models

4. **Reduce concurrent requests:**

- Limit Open WebUI users
- Queue requests in n8n

---

## Network Issues

### Can't Access Services Locally

**Symptoms:**

- `curl http://localhost:3000` fails
- Services not accessible via IP

**Solutions:**

1. **Check container networking:**

```bash
docker network ls
docker network inspect ai-network
```

2. **Check firewall:**

```bash
sudo ufw status
# If active, allow ports:
sudo ufw allow 3000
sudo ufw allow 11434
sudo ufw allow 5678
```

3. **Test from VM:**

```bash
curl http://localhost:3000
curl http://localhost:11434/api/tags
```

### Cloudflare Tunnel Not Working

**Symptoms:**

- Can't access via domain
- Tunnel shows offline

**Solutions:**

1. **Check tunnel status:**

```bash
sudo systemctl status cloudflared
```

2. **Check tunnel logs:**

```bash
sudo journalctl -u cloudflared -f
```

3. **Verify DNS records:**

```bash
nslookup ai.yourdomain.com
```

4. **Test local connectivity:**

```bash
# From CF-Tunnel VM
curl http://192.168.1.125:3000
```

5. **Restart tunnel:**

```bash
sudo systemctl restart cloudflared
```

6. **Validate config:**

```bash
cloudflared tunnel ingress validate
```

### DNS Resolution Issues

**Symptoms:**

- Can't resolve domain names
- `wget` or `curl` fails

**Solutions:**

1. **Check DNS:**

```bash
cat /etc/resolv.conf
```

Should contain:

```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

2. **Test DNS:**

```bash
nslookup google.com
```

3. **Update netplan:**

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

```yaml
network:
  ethernets:
    ens18:
      addresses: [192.168.1.125/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

```bash
sudo netplan apply
```

---

## VM Issues

### VM Won't Start

**Symptoms:**

- VM fails to boot
- Black screen on console

**Solutions:**

1. **Check VM config:**

```bash
qm config 100
```

2. **Check IOMMU groups:**

```bash
# On Proxmox host
find /sys/kernel/iommu_groups/ -type l
```

3. **Try without GPU:**

```bash
# Temporarily remove GPU
qm set 100 --delete hostpci0
qm start 100
```

4. **Check kernel messages:**

```bash
dmesg | grep -i error
```

### VM Freezes or Crashes

**Symptoms:**

- VM becomes unresponsive
- Random crashes during GPU use

**Solutions:**

1. **Check host memory:**

```bash
free -h
```

2. **Reduce VM memory:**

```bash
qm set 100 --memory 12288  # Reduce to 12GB
```

3. **Check GPU temperature:**

```bash
nvidia-smi -q -d TEMPERATURE
```

4. **Update BIOS/UEFI:**

- Check manufacturer website for updates

### No Display Output from GPU

**Symptoms:**

- Can SSH but no video output
- Monitor shows "No signal"

**Solutions:**

1. **Ensure x-vga=1 is set:**

```bash
qm config 100 | grep hostpci
```

2. **Try different video port:**

- Switch between HDMI, DisplayPort

3. **Add kernel parameter in VM:**

```bash
# Edit /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash video=efifb:off"
sudo update-grub
sudo reboot
```

---

## Performance Issues

### High CPU Usage

**Symptoms:**

- System slow
- `htop` shows high CPU usage

**Solutions:**

1. **Check what's using CPU:**

```bash
htop
# Press F6 to sort by CPU%
```

2. **Limit Docker CPU:**

```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '4'
```

3. **Use CPU governor:**

```bash
sudo apt install cpufrequtils
sudo cpufreq-set -g performance
```

### High Memory Usage

**Symptoms:**

- System runs out of RAM
- OOM (Out of Memory) errors

**Solutions:**

1. **Check memory:**

```bash
free -h
docker stats
```

2. **Limit container memory:**

```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G
```

3. **Clear cache:**

```bash
sudo sync
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

### Disk Space Issues

**Symptoms:**

- "No space left on device"
- Slow performance

**Solutions:**

1. **Check disk usage:**

```bash
df -h
du -sh /var/lib/docker/*
```

2. **Clean Docker:**

```bash
docker system prune -a -f
docker volume prune -f
```

3. **Remove old models:**

```bash
docker exec ollama ollama rm old-model-name
```

4. **Expand VM disk:**

```bash
# On Proxmox host
qm resize 100 scsi0 +100G
# Then in VM:
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

---

## Data Issues

### Lost Container Data

**Symptoms:**

- Models disappeared after restart
- n8n workflows missing

**Solutions:**

1. **Check volumes:**

```bash
docker volume ls
docker volume inspect ollama_data
```

2. **Backup volumes:**

```bash
docker run --rm -v ollama_data:/data -v $(pwd):/backup ubuntu tar czf /backup/ollama-backup.tar.gz /data
```

3. **Restore volumes:**

```bash
docker run --rm -v ollama_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/ollama-backup.tar.gz -C /
```

---

## Security Issues

### Unauthorized Access Attempts

**Symptoms:**

- Strange login attempts in logs
- Unknown connections

**Solutions:**

1. **Check auth logs:**

```bash
sudo tail -f /var/log/auth.log
```

2. **Install fail2ban:**

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

3. **Use Cloudflare Access:**

- Enable Zero Trust authentication
- Add access policies

4. **Change SSH port:**

```bash
sudo nano /etc/ssh/sshd_config
# Change Port 22 to Port 2222
sudo systemctl restart sshd
```

---

## Getting Help

### Diagnostic Information to Collect

When asking for help, provide:

```bash
# System info
uname -a
lsb_release -a

# GPU info
nvidia-smi
lspci | grep -i nvidia

# Docker info
docker version
docker compose version
docker ps -a

# Service logs
docker logs ollama --tail 50
docker logs open-webui --tail 50

# Cloudflare tunnel
sudo systemctl status cloudflared
sudo journalctl -u cloudflared --tail 50
```

### Where to Get Help

- 📖 **Documentation**: Check `/docs` folder
- 🐛 **GitHub Issues**: [Report bugs](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues)
- 💬 **Discussions**: [Ask questions](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions)
- 📧 **Email**: <fatihxbayram@yandex.com.tr>

### Before Posting

- [ ] Check this troubleshooting guide
- [ ] Search existing GitHub issues
- [ ] Run diagnostic commands
- [ ] Collect relevant logs
- [ ] Try basic solutions (restart, update, etc.)

---

## Prevention Tips

### Regular Maintenance

```bash
# Weekly:
sudo apt update && sudo apt upgrade -y
docker system prune -f

# Monthly:
# Backup important data
# Check disk space
# Review logs for errors
# Update Docker images
```

### Monitoring

Set up basic monitoring:

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Create monitoring alias
echo "alias ai-health='watch -n 1 nvidia-smi'" >> ~/.bashrc
source ~/.bashrc
```

### Backups

Automate backups:

```bash
# Create backup script
nano ~/backup-ai.sh
```

```bash
#!/bin/bash
# AI Infrastructure Backup Script

BACKUP_DIR="/backups/ai-infrastructure"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup Docker volumes
docker run --rm \
  -v ollama_data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu tar czf /backup/ollama-$DATE.tar.gz /data

docker run --rm \
  -v n8n_data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu tar czf /backup/n8n-$DATE.tar.gz /data

# Backup configurations
cp -r ~/proxmox-ai-infrastructure/docker $BACKUP_DIR/docker-$DATE
cp ~/.env $BACKUP_DIR/env-$DATE

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR"
```

Make executable and add to crontab:

```bash
chmod +x ~/backup-ai.sh

# Run daily at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-ai.sh") | crontab -
```

---

## Advanced Troubleshooting

### Enable Debug Logging

**For Ollama:**

```bash
# In docker-compose.yml
environment:
  - OLLAMA_DEBUG=1
```

**For n8n:**

```bash
environment:
  - N8N_LOG_LEVEL=debug
```

**For Docker:**

```bash
sudo nano /etc/docker/daemon.json
```

```json
{
  "debug": true,
  "log-level": "debug"
}
```

```bash
sudo systemctl restart docker
```

### Network Debugging

**Test connectivity between containers:**

```bash
# Get container IPs
docker inspect ollama | grep IPAddress
docker inspect open-webui | grep IPAddress

# Test from one container to another
docker exec open-webui ping ollama
docker exec open-webui curl http://ollama:11434/api/tags
```

**Capture network traffic:**

```bash
# Install tcpdump
sudo apt install tcpdump

# Capture traffic on docker network
sudo tcpdump -i docker0 -w /tmp/docker-traffic.pcap

# Analyze with Wireshark or:
sudo tcpdump -r /tmp/docker-traffic.pcap
```

### GPU Deep Diagnostics

**Check GPU power state:**

```bash
nvidia-smi -q -d POWER
```

**Monitor GPU in real-time:**

```bash
watch -n 1 'nvidia-smi --query-gpu=timestamp,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv'
```

**Test GPU compute:**

```bash
# CUDA samples
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples/Samples/1_Utilities/deviceQuery
make
./deviceQuery
```

**Check GPU throttling:**

```bash
nvidia-smi -q -d PERFORMANCE
```

### Database Issues (if using Postgres/MySQL)

**Check database connections:**

```bash
docker exec -it postgres psql -U user -d database -c "SELECT count(*) FROM pg_stat_activity;"
```

**Optimize database:**

```bash
docker exec -it postgres psql -U user -d database -c "VACUUM ANALYZE;"
```

---

## Known Issues

### Issue 1: Ollama Fails After System Update

**Description:** After Ubuntu system update, Ollama container fails to start with GPU.

**Workaround:**

```bash
# Reinstall NVIDIA driver
sudo apt install --reinstall nvidia-driver-535

# Reconfigure Docker NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Restart containers
docker compose restart
```

### Issue 2: Cloudflare Tunnel Disconnects Randomly

**Description:** Tunnel shows offline intermittently.

**Workaround:**

```bash
# Increase tunnel timeout in config
# /root/.cloudflared/config.yml
originRequest:
  connectTimeout: 60s
  keepAliveTimeout: 90s
  
sudo systemctl restart cloudflared
```

### Issue 3: Open WebUI Slow to Load

**Description:** Web interface takes long time to load.

**Workaround:**

```bash
# Increase container resources
# In docker-compose.yml add:
deploy:
  resources:
    limits:
      memory: 4G
      cpus: '2'
```

### Issue 4: n8n Workflows Timeout

**Description:** Long-running AI workflows timeout.

**Workaround:**

```bash
# Increase execution timeout
# In docker-compose.yml:
environment:
  - EXECUTIONS_TIMEOUT: 3600
  - EXECUTIONS_TIMEOUT_MAX: 7200
```

---

## Emergency Recovery

### Complete System Reset

If everything fails, start fresh:

```bash
# 1. Stop all containers
docker compose down

# 2. Remove all containers and volumes
docker system prune -a --volumes -f

# 3. Remove data directories
sudo rm -rf /var/lib/docker/volumes/*

# 4. Restart Docker
sudo systemctl restart docker

# 5. Redeploy
cd ~/proxmox-ai-infrastructure/docker
docker compose up -d

# 6. Re-download models
docker exec ollama ollama pull llama2
```

### Restore from Backup

```bash
# Stop containers
docker compose down

# Restore volumes
docker run --rm \
  -v ollama_data:/data \
  -v /backups/ai-infrastructure:/backup \
  ubuntu tar xzf /backup/ollama-YYYYMMDD_HHMMSS.tar.gz -C /

# Start containers
docker compose up -d
```

### Rebuild VM from Scratch

Last resort - rebuild entire VM:

1. On Proxmox host, backup VM:

```bash
vzdump 100 --dumpdir /var/lib/vz/dump
```

2. Delete VM:

```bash
qm stop 100
qm destroy 100
```

3. Follow installation guide from beginning

---

## Performance Tuning

### Optimize for Speed

**1. GPU Performance Mode:**

```bash
# Set GPU to max performance
sudo nvidia-smi -pm 1
sudo nvidia-smi -pl 250  # Set power limit (watts)
sudo nvidia-smi -lgc 2100  # Set GPU clock (MHz)
```

**2. CPU Governor:**

```bash
sudo apt install cpufrequtils
echo "performance" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

**3. Swappiness:**

```bash
# Reduce swap usage
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**4. Docker Storage Driver:**

```bash
# Use overlay2 for better performance
sudo nano /etc/docker/daemon.json
```

```json
{
  "storage-driver": "overlay2"
}
```

### Optimize for Memory

**1. Limit model size:**

```bash
# Use quantized models
docker exec ollama ollama pull llama2:7b-q4_0
```

**2. Clear cache regularly:**

```bash
# Add to crontab
0 */6 * * * sync && echo 3 > /proc/sys/vm/drop_caches
```

**3. Enable zram:**

```bash
sudo apt install zram-config
sudo systemctl enable zram-config
```

---

## Logs and Debugging

### Important Log Locations

```bash
# System logs
/var/log/syslog
/var/log/kern.log

# Docker logs
/var/lib/docker/containers/*/

# NVIDIA logs
/var/log/nvidia-installer.log

# Cloudflare tunnel logs
sudo journalctl -u cloudflared

# Application logs
docker logs ollama
docker logs open-webui
docker logs n8n
```

### Useful Log Commands

```bash
# Follow logs in real-time
docker logs -f ollama

# Last 100 lines
docker logs --tail 100 ollama

# Logs since specific time
docker logs --since 2024-01-01T00:00:00 ollama

# Search logs
docker logs ollama 2>&1 | grep -i error

# Export logs
docker logs ollama &> /tmp/ollama.log
```

### Log Rotation

Prevent logs from filling disk:

```bash
sudo nano /etc/docker/daemon.json
```

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

```bash
sudo systemctl restart docker
```

---

## Contact Support

### When Nothing Works

If you've tried everything and still have issues:

1. **Collect full diagnostics:**

```bash
# Run comprehensive diagnostic
curl -o diag.sh https://raw.githubusercontent.com/fatihhbayramm/proxmox-ai-infrastructure/main/scripts/diagnostics.sh
chmod +x diag.sh
./diag.sh

# This creates a diagnostics.tar.gz file
```

2. **Create GitHub Issue:**
   - Go to: <https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues>
   - Title: Brief description of problem
   - Include:
     - What you were trying to do
     - What happened instead
     - What you've already tried
     - Output from diagnostic script
     - Relevant logs

3. **Community Help:**
   - GitHub Discussions: <https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions>
   - Reddit r/selfhosted
   - Reddit r/LocalLLaMA

---

## Quick Reference Commands

### Daily Operations

```bash
# Check system health
nvidia-smi
docker ps
df -h
free -h

# Restart services
docker compose restart
sudo systemctl restart cloudflared

# Check logs
docker logs ollama --tail 50
sudo journalctl -u cloudflared --tail 50

# Update containers
cd ~/proxmox-ai-infrastructure/docker
docker compose pull
docker compose up -d
```

### Emergency Commands

```bash
# Stop everything
docker compose down
sudo systemctl stop cloudflared

# Restart everything
sudo reboot

# Clear Docker cache
docker system prune -a -f

# Reset GPU
sudo nvidia-smi --gpu-reset
```

---

**Remember:** Most issues can be solved by:

1. Checking logs
2. Restarting services
3. Verifying configurations
4. Ensuring adequate resources

**Prevention is better than cure:** Regular backups, monitoring, and maintenance will prevent most issues.
