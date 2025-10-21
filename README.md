# 🤖 Self-Hosted AI Infrastructure with Proxmox

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Proxmox](https://img.shields.io/badge/Proxmox-8.x-E57000?logo=proxmox)](https://www.proxmox.com/)
[![Docker](https://img.shields.io/badge/Docker-24.x-2496ED?logo=docker)](https://www.docker.com/)
[![NVIDIA](https://img.shields.io/badge/NVIDIA-CUDA%2012.x-76B900?logo=nvidia)](https://developer.nvidia.com/cuda-toolkit)

> Production-ready AI server with GPU passthrough, running Ollama, Open WebUI, and n8n for complete AI automation - **Zero API costs, 100% data privacy**

![Architecture](https://img.shields.io/badge/Architecture-Homelab-blue)
![Status](https://img.shields.io/badge/Status-Production-success)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

This project provides a complete guide and configuration files for building a self-hosted AI infrastructure using Proxmox virtualization, GPU passthrough, and containerized AI services. Say goodbye to API costs and hello to unlimited, private AI compute!

### What This Achieves

- **💰 Cost Savings**: $480/year → $0 (ChatGPT Plus + n8n Cloud eliminated)
- **🔒 Privacy**: 100% data sovereignty - your data never leaves your server
- **⚡ Performance**: 40-50 tokens/sec on 7B models with RTX A2000
- **🚀 Unlimited Usage**: No rate limits, no API quotas
- **🛠️ Full Control**: Run any LLM model, customize everything

## ✨ Features

### Core Services

- **🧠 Ollama**: Local LLM runtime supporting multiple models
- **💬 Open WebUI**: Beautiful ChatGPT-like interface
- **🔄 n8n**: Workflow automation engine for AI tasks
- **🔐 Cloudflare Tunnel**: Secure zero-trust access without port forwarding
- **🎨 Portainer** *(optional)*: Docker management GUI

### Technical Highlights

- ✅ NVIDIA GPU passthrough with VFIO
- ✅ Docker containerization with GPU support
- ✅ Automated deployment with docker-compose
- ✅ TLS/HTTPS via Cloudflare Tunnel
- ✅ Health monitoring and auto-restart
- ✅ Resource optimization for homelab

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Proxmox Host (PVE1)                      │
│                                                             │
│  ┌──────────────────┐         ┌───────────────────────┐   │
│  │  CF-Tunnel VM    │         │   AI Server VM        │   │
│  │  Ubuntu 22.04    │         │   Ubuntu 22.04        │   │
│  │                  │         │                       │   │
│  │  cloudflared     │────────▶│  Docker Services:     │   │
│  │                  │         │  ┌─────────────────┐  │   │
│  │  Tunnels:        │         │  │ Ollama :11434   │  │   │
│  │  • ai.*          │         │  │ Open WebUI:3000 │  │   │
│  │  • n8n.*         │         │  │ n8n :5678       │  │   │
│  │  • pve.*         │         │  └─────────────────┘  │   │
│  └──────────────────┘         │                       │   │
│                                │  GPU: NVIDIA RTX A2000│   │
│                                │  VRAM: 5754MB         │   │
│                                └───────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ Cloudflare Global Network
                         ▼
                   ☁️ Internet (HTTPS)
                         │
                         ▼
                 🌐 Your Domains
         • https://ai.yourdomain.com
         • https://n8n.yourdomain.com
```

## 📦 Prerequisites

### Hardware Requirements

**Minimum:**
- CPU: 4 cores (Intel/AMD with VT-d/AMD-Vi)
- RAM: 16GB
- Storage: 100GB SSD
- GPU: NVIDIA GPU with 4GB+ VRAM

**Recommended:**
- CPU: 6+ cores
- RAM: 32GB+
- Storage: 500GB NVMe SSD
- GPU: NVIDIA RTX series (RTX 3060, 4060, A2000, etc.)

### Software Requirements

- Proxmox VE 8.x
- Ubuntu Server 22.04 LTS (for VMs)
- NVIDIA GPU (compatible with Linux drivers)
- Domain name (for Cloudflare Tunnel)
- Cloudflare account (free tier works)

### Knowledge Prerequisites

- Basic Linux command line
- Understanding of virtualization concepts
- Docker fundamentals
- Basic networking knowledge

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/fatihhbayramm/proxmox-ai-infrastructure.git
cd proxmox-ai-infrastructure
```

### 2. Configure Variables

```bash
cp .env.example .env
nano .env
```

Edit with your settings:
```env
# Domain Configuration
DOMAIN=yourdomain.com
AI_SUBDOMAIN=ai
N8N_SUBDOMAIN=n8n

# Cloudflare
CF_TUNNEL_TOKEN=your_token_here

# GPU Configuration
GPU_PCI_ID=01:00.0
GPU_VENDOR_ID=10de:2544
```

### 3. Run Installation Script

```bash
chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### 4. Deploy Services

```bash
cd docker
docker-compose up -d
```

### 5. Access Services

- **Open WebUI**: https://ai.yourdomain.com
- **n8n**: https://n8n.yourdomain.com
- **Proxmox**: https://pve.yourdomain.com:8006

## 📖 Installation

For detailed step-by-step installation guide, see:

📝 **[INSTALLATION.md](docs/INSTALLATION.md)** - Complete setup guide

Key sections covered:
1. Proxmox GPU Passthrough Setup
2. VM Creation and Configuration
3. NVIDIA Driver Installation
4. Docker and NVIDIA Container Runtime
5. Service Deployment
6. Cloudflare Tunnel Setup

## ⚙️ Configuration

### Docker Compose Structure

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - open-webui_data:/app/backend/data
    depends_on:
      - ollama
    restart: unless-stopped

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=n8n.yourdomain.com
      - WEBHOOK_URL=https://n8n.yourdomain.com
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped
```

### Available Models

Download models with:
```bash
docker exec -it ollama ollama pull llama2
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull codellama
docker exec -it ollama ollama pull llama2:13b
```

Full model list: https://ollama.com/library

## 🎯 Usage

### Basic Chat Interface

1. Open https://ai.yourdomain.com
2. Select a model from dropdown
3. Start chatting!

### API Usage

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?"
}'
```

### n8n Workflow Example

Create AI-powered email automation:
1. Access n8n: https://n8n.yourdomain.com
2. Create new workflow
3. Add Gmail Trigger → Ollama Node → Gmail Send
4. Activate workflow

Example workflows included in `workflows/` directory.

## 📊 Performance

### Benchmark Results (RTX A2000, 5754MB VRAM)

| Model | Size | Tokens/sec | RAM Usage | Response Quality |
|-------|------|------------|-----------|------------------|
| Llama 2 7B | 3.8GB | 45-50 | 4.2GB | ⭐⭐⭐⭐ |
| Mistral 7B | 4.1GB | 40-45 | 4.5GB | ⭐⭐⭐⭐⭐ |
| CodeLlama 7B | 3.8GB | 42-48 | 4.3GB | ⭐⭐⭐⭐ |
| Llama 2 13B | 7.3GB | 20-25 | OOM | ⭐⭐⭐⭐⭐ |

### Resource Usage

- **Idle**: ~2GB RAM, 5% CPU
- **Active Chat**: ~6GB RAM, 60% GPU
- **Batch Processing**: ~8GB RAM, 95% GPU

## 🔧 Troubleshooting

### GPU Not Detected

```bash
# Check GPU status
nvidia-smi

# Verify Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### Ollama Connection Issues

```bash
# Check Ollama logs
docker logs ollama

# Restart service
docker-compose restart ollama
```

### Common Issues

See **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** for detailed solutions.

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Complete setup walkthrough
- **[GPU Passthrough Guide](docs/GPU_PASSTHROUGH.md)** - VFIO configuration
- **[Docker Setup](docs/DOCKER_SETUP.md)** - Container configuration
- **[Cloudflare Tunnel](docs/CLOUDFLARE_TUNNEL.md)** - Secure access setup
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[API Reference](docs/API.md)** - Ollama API documentation
- **[Workflow Examples](workflows/)** - n8n automation templates

## 🛡️ Security

- ✅ All external access via Cloudflare Tunnel (zero open ports)
- ✅ TLS/HTTPS encryption for all services
- ✅ Zero Trust access with Cloudflare Access (optional)
- ✅ Private network isolation
- ✅ No data leaves your infrastructure

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Amazing local LLM runtime
- [Open WebUI](https://github.com/open-webui/open-webui) - Beautiful UI
- [n8n](https://n8n.io/) - Powerful automation platform
- [Proxmox](https://www.proxmox.com/) - Excellent virtualization platform
- [Cloudflare](https://www.cloudflare.com/) - Secure tunneling solution

## 📞 Support

### Getting Help

**Before asking for help:**
1. ✅ Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. ✅ Search [GitHub Issues](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues)
3. ✅ Review relevant documentation
4. ✅ Collect diagnostic information

**Where to get help:**
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions)
- 📧 **Email**: fatihxbayram@yandex.com.tr
- 📝 **Blog**: [Medium](https://medium.com/@fatihhbayramm)

### Diagnostic Commands

```bash
# Check service status
docker compose ps
docker compose logs

# Check GPU
nvidia-smi
docker exec ollama nvidia-smi

# Test Ollama
curl http://localhost:11434/api/tags

# Check network
docker network inspect ai-network

# System resources
free -h
df -h
```

---

## 🌟 Acknowledgments

Built with amazing open-source projects:
- **[Ollama](https://ollama.ai/)** - Fast local LLM runtime
- **[Open WebUI](https://github.com/open-webui/open-webui)** - Beautiful chat interface
- **[n8n](https://n8n.io/)** - Powerful workflow automation
- **[Proxmox](https://www.proxmox.com/)** - Excellent virtualization platform
- **[Cloudflare](https://www.cloudflare.com/)** - Secure tunneling solution

Special thanks to the self-hosted AI community!

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🗺️ Roadmap

### Completed ✅
- [x] Basic infrastructure setup
- [x] GPU passthrough configuration
- [x] Docker containerization
- [x] Open WebUI integration
- [x] n8n workflow examples
- [x] Cloudflare Tunnel setup
- [x] Comprehensive documentation
- [x] System prompts library

### Planned 🚧
- [ ] Kubernetes deployment option
- [ ] Monitoring with Prometheus + Grafana
- [ ] Automated backup scripts
- [ ] Multi-GPU support guide
- [ ] Voice AI integration (Whisper + TTS)
- [ ] Stable Diffusion integration
- [ ] Advanced RAG examples
- [ ] Video tutorials

### Community Requests 💭
- [ ] AWS/Azure deployment guides
- [ ] Ansible playbooks
- [ ] Docker Swarm setup
- [ ] Terraform configurations

**Have a suggestion?** [Open a discussion](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions)!

---

<div align="center">

### ⭐ Star this repo if you found it helpful!

**Built with ❤️ in Istanbul, Turkey**

[Report Bug](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/issues) · 
[Request Feature](https://github.com/fatihhbayramm/proxmox-ai-infrastructure/discussions) · 
[Read Blog](https://medium.com/@fatihhbayramm)

</div>