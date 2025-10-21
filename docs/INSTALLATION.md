# 📖 Installation Guide

Complete step-by-step guide to set up your self-hosted AI infrastructure with Proxmox and GPU passthrough.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Proxmox Host Setup](#proxmox-host-setup)
3. [GPU Passthrough Configuration](#gpu-passthrough-configuration)
4. [VM Creation](#vm-creation)
5. [Ubuntu Installation](#ubuntu-installation)
6. [NVIDIA Driver Setup](#nvidia-driver-setup)
7. [Docker Installation](#docker-installation)
8. [AI Services Deployment](#ai-services-deployment)
9. [Cloudflare Tunnel Setup](#cloudflare-tunnel-setup)
10. [Verification](#verification)

---

## Prerequisites

### Hardware Checklist

- [ ] CPU with virtualization support (Intel VT-d or AMD-Vi)
- [ ] NVIDIA GPU with 4GB+ VRAM
- [ ] 16GB+ RAM (32GB recommended)
- [ ] 200GB+ storage (SSD recommended)
- [ ] Network connection

### Software Requirements

- [ ] Proxmox VE 8.x installed
- [ ] Domain name registered
- [ ] Cloudflare account (free tier works)

### Knowledge Requirements

- Basic Linux command line
- SSH access knowledge
- Basic networking concepts

**Estimated Time**: 2-3 hours for complete setup

---

## Proxmox Host Setup

### Step 1: Enable IOMMU

SSH into your Proxmox host:

```bash
ssh root@your-proxmox-ip
```

Edit GRUB configuration:

```bash
nano /etc/default/grub
```

**For Intel CPU:**

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
```

**For AMD CPU:**

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"
```

Update GRUB:

```bash
update-grub
```

### Step 2: Load VFIO Modules

Add required modules to `/etc/modules`:

```bash
cat >> /etc/modules << EOF
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
EOF
```

### Step 3: Update Initramfs

```bash
update-initramfs -u -k all
```

### Step 4: Reboot

```bash
reboot
```

### Step 5: Verify IOMMU

After reboot, verify IOMMU is enabled:

```bash
dmesg | grep -e DMAR -e IOMMU
```

You should see output indicating IOMMU is enabled.

---

## GPU Passthrough Configuration

### Step 1: Find GPU IDs

```bash
lspci -nn | grep -i nvidia
```

Example output:

```
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106 [RTX A2000] [10de:2544]
01:00.1 Audio device [0403]: NVIDIA Corporation GA106 High Definition Audio [10de:228b]
```

Note both IDs: `10de:2544` (GPU) and `10de:228b` (Audio)

### Step 2: Blacklist NVIDIA Drivers on Host

Create blacklist file:

```bash
cat > /etc/modprobe.d/blacklist.conf << EOF
blacklist nouveau
blacklist nvidia
blacklist nvidiafb
blacklist nvidia_drm
blacklist nvidia_uvm
EOF
```

### Step 3: Configure VFIO

Replace `10de:2544,10de:228b` with your GPU IDs:

```bash
echo "options vfio-pci ids=10de:2544,10de:228b" > /etc/modprobe.d/vfio.conf
```

### Step 4: Update and Reboot

```bash
update-initramfs -u -k all
reboot
```

### Step 5: Verify VFIO

```bash
lspci -nnk | grep -i nvidia -A 3
```

You should see `Kernel driver in use: vfio-pci`

---

## VM Creation

### Method 1: Using Proxmox Web UI

1. **Access Proxmox Web Interface**
   - Navigate to `https://your-proxmox-ip:8006`
   - Login with root credentials

2. **Create New VM**
   - Click "Create VM" button
   - General:
     - VM ID: 100 (or your choice)
     - Name: `ai-server`

3. **OS Configuration**
   - ISO Image: Ubuntu Server 22.04 LTS
   - Type: Linux
   - Version: 5.x - 2.6 Kernel

4. **System Configuration**
   - BIOS: OVMF (UEFI)
   - Add EFI Disk: Yes
   - Machine: q35
   - SCSI Controller: VirtIO SCSI single

5. **Disks**
   - Bus/Device: SCSI
   - Storage: local-lvm (or your storage)
   - Disk size: 200 GB
   - Cache: Write back
   - Discard: Yes
   - SSD emulation: Yes
   - IO thread: Yes

6. **CPU**
   - Sockets: 1
   - Cores: 6 (adjust based on your CPU)
   - Type: host

7. **Memory**
   - Memory: 16384 MB (16GB)
   - Minimum memory: 16384
   - Ballooning Device: **Uncheck** (important!)

8. **Network**
   - Bridge: vmbr0
   - Model: VirtIO
   - Firewall: Yes

9. **Confirm and Create**

### Method 2: Using CLI

```bash
# Create VM
qm create 100 \
  --name ai-server \
  --memory 16384 \
  --balloon 0 \
  --cores 6 \
  --cpu host \
  --machine q35 \
  --bios ovmf \
  --scsihw virtio-scsi-single

# Add EFI disk
qm set 100 --efidisk0 local-lvm:1,efitype=4m,pre-enrolled-keys=1

# Add main disk
qm set 100 --scsi0 local-lvm:200,discard=on,iothread=1,ssd=1

# Add network
qm set 100 --net0 virtio,bridge=vmbr0,firewall=1

# Add ISO
qm set 100 --ide2 local:iso/ubuntu-22.04-live-server-amd64.iso,media=cdrom

# Set boot order
qm set 100 --boot order=scsi0;ide2;net0
```

### Step 3: Add GPU to VM

**Via Web UI:**

1. Select your VM
2. Hardware → Add → PCI Device
3. Device: Select your NVIDIA GPU
4. All Functions: Yes
5. Primary GPU: Yes
6. PCI-Express: Yes

**Via CLI:**

```bash
# Find PCI address
lspci | grep -i nvidia

# Add GPU (replace 01:00 with your address)
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1
```

---

## Ubuntu Installation

### Step 1: Start VM

```bash
qm start 100
```

### Step 2: Install Ubuntu

1. Access VM console from Proxmox web UI
2. Follow Ubuntu installation wizard:
   - Language: English
   - Keyboard: Your layout
   - Network: Configure static IP (recommended)
     - IP: 192.168.1.125/24
     - Gateway: 192.168.1.1
     - DNS: 8.8.8.8, 1.1.1.1
   - Storage: Use entire disk
   - Profile:
     - Name: aiuser
     - Server name: ai-server
     - Username: aiuser
     - Password: [secure password]
   - SSH: Install OpenSSH server
   - Featured snaps: Skip

3. Reboot after installation

### Step 3: Initial Ubuntu Setup

SSH into your VM:

```bash
ssh aiuser@192.168.1.125
```

Update system:

```bash
sudo apt update && sudo apt upgrade -y
```

Install essential tools:

```bash
sudo apt install -y \
  curl \
  wget \
  git \
  vim \
  htop \
  net-tools \
  build-essential \
  linux-headers-$(uname -r)
```

---

## NVIDIA Driver Setup

### Step 1: Verify GPU

```bash
lspci | grep -i nvidia
```

You should see your NVIDIA GPU.

### Step 2: Add NVIDIA Repository

```bash
sudo add-apt-repository ppa:graphics-drivers/ppa -y
sudo apt update
```

### Step 3: Install NVIDIA Driver

```bash
# Install driver (version 535 or later recommended)
sudo apt install -y nvidia-driver-535

# Reboot to load driver
sudo reboot
```

### Step 4: Verify Installation

After reboot:

```bash
nvidia-smi
```

You should see GPU information displayed.

### Step 5: Install CUDA Toolkit

```bash
# Download CUDA keyring
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb

# Update and install CUDA
sudo apt update
sudo apt install -y cuda-toolkit-12-3

# Add to PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Verify CUDA
nvcc --version
```

---

## Docker Installation

### Step 1: Install Docker

```bash
# Remove old versions
sudo apt remove -y docker docker-engine docker.io containerd runc

# Install dependencies
sudo apt install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes
```

### Step 2: Install NVIDIA Container Toolkit

```bash
# Add NVIDIA Container Toolkit repository
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker
sudo systemctl restart docker
```

### Step 3: Verify Docker GPU Access

```bash
docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu22.04 nvidia-smi
```

You should see your GPU information.

---

## AI Services Deployment

### Step 1: Clone Repository

```bash
cd ~
git clone https://github.com/fatihhbayramm/proxmox-ai-infrastructure.git
cd proxmox-ai-infrastructure
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env
```

Edit with your settings:

```env
DOMAIN=yourdomain.com
AI_SUBDOMAIN=ai
N8N_SUBDOMAIN=n8n
```

### Step 3: Deploy Services

```bash
cd docker
docker compose up -d
```

### Step 4: Download AI Models

```bash
# Download default models
docker exec ollama ollama pull llama2
docker exec ollama ollama pull mistral
docker exec ollama ollama pull codellama

# List available models
docker exec ollama ollama list
```

### Step 5: Verify Services

```bash
# Check container status
docker ps

# Check Ollama
curl http://localhost:11434/api/tags

# Check Open WebUI
curl http://localhost:3000

# Check n8n
curl http://localhost:5678
```

---

## Cloudflare Tunnel Setup

### Step 1: Create Tunnel VM

Create a separate lightweight VM for Cloudflare Tunnel:

```bash
# CLI method
qm create 101 \
  --name cf-tunnel \
  --memory 2048 \
  --cores 2 \
  --cpu host \
  --net0 virtio,bridge=vmbr0
```

Install Ubuntu Server 22.04 on this VM.

### Step 2: Install Cloudflared

```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Verify
cloudflared --version
```

### Step 3: Authenticate

```bash
cloudflared tunnel login
```

Follow the link to authenticate with Cloudflare.

### Step 4: Create Tunnel

```bash
cloudflared tunnel create ai-infrastructure
```

Note the tunnel ID from output.

### Step 5: Configure Tunnel

```bash
sudo mkdir -p /root/.cloudflared
sudo nano /root/.cloudflared/config.yml
```

Use configuration from `configs/cloudflare/tunnel-config.yml`

### Step 6: Create DNS Records

```bash
cloudflared tunnel route dns ai-infrastructure ai.yourdomain.com
cloudflared tunnel route dns ai-infrastructure n8n.yourdomain.com
```

### Step 7: Start Tunnel Service

```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

---

## Verification

### Check All Services

```bash
# GPU
nvidia-smi

# Docker containers
docker ps

# Ollama
curl http://localhost:11434/api/tags

# Cloudflare Tunnel
sudo systemctl status cloudflared
```

### Access Services

- **Open WebUI**: <https://ai.yourdomain.com>
- **n8n**: <https://n8n.yourdomain.com>
- **Proxmox**: <https://pve.yourdomain.com:8006>

### Test AI Chat

1. Open <https://ai.yourdomain.com>
2. Select "llama2" model
3. Type: "Hello, how are you?"
4. You should get a response!

---

## 🎉 Congratulations

Your self-hosted AI infrastructure is now ready!

### Next Steps

- [ ] Create n8n workflows
- [ ] Add more AI models
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Explore advanced features

### Performance Tips

1. Use smaller models (7B) for faster responses
2. Adjust GPU memory if needed
3. Monitor resource usage with `htop` and `nvidia-smi`
4. Keep system updated

---

## Troubleshooting

If you encounter issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Support

- 📖 Documentation: `/docs` folder
- 🐛 Issues: [GitHub Issues](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions)
