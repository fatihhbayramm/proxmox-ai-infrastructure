# NVIDIA Configuration

## Host (Proxmox) Setup

### 1. Blacklist NVIDIA Drivers

Copy blacklist configuration:

```bash
sudo cp blacklist.conf /etc/modprobe.d/blacklist.conf
```

### 2. Configure VFIO

Find your GPU IDs:

```bash
lspci -nn | grep -i nvidia
```

Example output: 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106 [RTX A2000] [10de:2544]
01:00.1 Audio device [0403]: NVIDIA Corporation GA106 High Definition Audio [10de:228b]

Edit `vfio.conf` with your IDs:

```bash
nano vfio.conf
# Change: options vfio-pci ids=YOUR_IDS_HERE
```

Copy to system:

```bash
sudo cp vfio.conf /etc/modprobe.d/vfio.conf
```

### 3. Update and Reboot

```bash
sudo update-initramfs -u -k all
sudo reboot
```

### 4. Verify

After reboot:

```bash
# Should show vfio-pci as driver
lspci -nnk | grep -i nvidia -A 3

# Check VFIO
dmesg | grep -i vfio
```

---

## VM (Ubuntu) Setup

### 1. Install NVIDIA Driver

```bash
# Add NVIDIA repository
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install driver (version 535 or later)
sudo apt install nvidia-driver-535

# Reboot
sudo reboot
```

### 2. Verify Driver

```bash
nvidia-smi
```

Should show your GPU.

### 3. Install CUDA Toolkit

```bash
# Download CUDA 12.x
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-3

# Add to PATH
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Verify
nvcc --version
```

### 4. Install NVIDIA Container Toolkit

```bash
# Add Docker GPG key
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

# Add repository
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Install
sudo apt update
sudo apt install -y nvidia-container-toolkit

# Configure Docker
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

## Troubleshooting

### Driver Issues

```bash
# Remove old drivers
sudo apt purge nvidia-*
sudo apt autoremove

# Reinstall
sudo apt install nvidia-driver-535
```

### CUDA Not Found

```bash
# Check installation
ls /usr/local/cuda

# Verify PATH
echo $PATH | grep cuda
```

### Docker GPU Access

```bash
# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# If fails, restart Docker
sudo systemctl restart docker
```
