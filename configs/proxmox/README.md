# Proxmox Configuration

## GPU Passthrough Setup

### 1. Enable IOMMU

Edit GRUB configuration:

```bash
nano /etc/default/grub
```

For Intel CPU:
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"

For AMD CPU:
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"

Update GRUB:

```bash
update-grub
```

### 2. Load VFIO Modules

Add to `/etc/modules`:

```bash
echo "vfio" >> /etc/modules
echo "vfio_iommu_type1" >> /etc/modules
echo "vfio_pci" >> /etc/modules
echo "vfio_virqfd" >> /etc/modules
```

### 3. Find GPU IDs

```bash
lspci -nn | grep -i nvidia
```

Example output:
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106 [RTX A2000] [10de:2544]
01:00.1 Audio device [0403]: NVIDIA Corporation GA106 High Definition Audio [10de:228b]

Note the IDs: `10de:2544` and `10de:228b`

### 4. Blacklist GPU Drivers on Host

Create `/etc/modprobe.d/blacklist.conf`:

```bash
blacklist nouveau
blacklist nvidia
blacklist nvidiafb
blacklist nvidia_drm
blacklist nvidia_uvm
```

### 5. Configure VFIO

Create `/etc/modprobe.d/vfio.conf`:

```bash
options vfio-pci ids=10de:2544,10de:228b
```

Replace with your GPU IDs.

### 6. Update Initramfs

```bash
update-initramfs -u -k all
```

### 7. Reboot

```bash
reboot
```

### 8. Verify VFIO

After reboot:

```bash
dmesg | grep -i vfio
lspci -nnk | grep -i nvidia -A 3
```

Should show: `Kernel driver in use: vfio-pci`

## Create VM

### Via GUI

1. Create new VM in Proxmox
2. OS: Linux 5.x - 2.6 Kernel
3. System:
   - BIOS: OVMF (UEFI)
   - Machine: q35
   - Add EFI Disk
4. Disks: 200GB, VirtIO SCSI
5. CPU: host, 6 cores
6. Memory: 16384 MB, Ballooning: off
7. Network: VirtIO

### Add GPU

1. Hardware → Add → PCI Device
2. Select your GPU
3. All Functions: Yes
4. Primary GPU: Yes
5. PCI-Express: Yes

### Via CLI

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
  --efidisk0 local-lvm:1,format=raw,efitype=4m,pre-enrolled-keys=1

# Add disk
qm set 100 --scsi0 local-lvm:200,discard=on,iothread=1,ssd=1

# Add network
qm set 100 --net0 virtio,bridge=vmbr0,firewall=1

# Add GPU (replace with your PCI address)
qm set 100 --hostpci0 0000:01:00,pcie=1,x-vga=1

# Set boot order
qm set 100 --boot order=scsi0
```

## Network Configuration

### Static IP on VM

Edit `/etc/netplan/00-installer-config.yaml`:

```yaml
network:
  version: 2
  ethernets:
    ens18:
      addresses:
        - 192.168.1.125/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

Apply:

```bash
sudo netplan apply
```

## Troubleshooting

### VM Won't Start

- Check IOMMU groups: `pvesh get /nodes/{node}/hardware/pci --pci-class-blacklist ""`
- Verify VFIO: `lspci -nnk | grep -i nvidia -A 3`

### No Display Output

- Ensure x-vga=1 is set
- Try different display port/HDMI port
- Add `video=efifb:off` to VM kernel parameters

### GPU Not Detected in VM

- Check if VFIO is loaded: `lsmod | grep vfio`
- Verify PCI passthrough: `dmesg | grep -i vfio`
