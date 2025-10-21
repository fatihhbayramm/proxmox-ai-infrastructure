# 📚 Documentation

Complete documentation for Proxmox AI Infrastructure.

## 📖 Available Guides

### Getting Started

1. **[INSTALLATION.md](INSTALLATION.md)** - Complete installation guide
   - Prerequisites and requirements
   - Step-by-step setup instructions
   - Proxmox GPU passthrough configuration
   - VM creation and Ubuntu installation
   - NVIDIA driver setup
   - Docker and AI services deployment
   - Cloudflare Tunnel configuration
   - **Start here if you're new!**

### Technical Documentation

2. **[GPU_PASSTHROUGH.md](GPU_PASSTHROUGH.md)** - GPU configuration details
   - IOMMU setup
   - VFIO configuration
   - PCI passthrough
   - Troubleshooting GPU issues

3. **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Docker configuration
   - Docker installation
   - NVIDIA Container Toolkit
   - docker-compose setup
   - Container networking
   - Volume management

4. **[CLOUDFLARE_TUNNEL.md](CLOUDFLARE_TUNNEL.md)** - Secure access setup
   - Cloudflare Tunnel installation
   - DNS configuration
   - Multi-service routing
   - Zero Trust setup (optional)

### Operations

5. **[API.md](API.md)** - API reference and examples
   - Ollama API endpoints
   - Open WebUI API
   - n8n API
   - Code examples (Python, JavaScript, cURL)
   - Model parameters

6. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
   - GPU problems
   - Docker issues
   - Network problems
   - Performance optimization
   - Emergency recovery

### Security

7. **[SECURITY.md](SECURITY.md)** - Security best practices
   - Network security
   - Access control
   - Data protection
   - Container security
   - Monitoring and logging
   - Compliance guidelines

## 🗂️ Documentation Structure

```
docs/
├── README.md                 # This file
├── INSTALLATION.md           # Complete setup guide
├── GPU_PASSTHROUGH.md        # GPU configuration
├── DOCKER_SETUP.md           # Docker setup
├── CLOUDFLARE_TUNNEL.md      # Secure access
├── API.md                    # API documentation
├── TROUBLESHOOTING.md        # Problem solving
└── SECURITY.md               # Security guide
```

## 🚀 Quick Links

### For First-Time Users

1. Read [INSTALLATION.md](INSTALLATION.md) from start to finish
2. Follow each step carefully
3. If you encounter issues, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### For Experienced Users

- **GPU Issues?** → [GPU_PASSTHROUGH.md](GPU_PASSTHROUGH.md)
- **Docker Problems?** → [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **API Usage?** → [API.md](API.md)
- **Security Hardening?** → [SECURITY.md](SECURITY.md)

### For Developers

- **API Integration**: Start with [API.md](API.md)
- **Custom Workflows**: Check n8n examples in
