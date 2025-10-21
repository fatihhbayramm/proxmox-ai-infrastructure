#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Proxmox AI Infrastructure Installation${NC}"
echo "================================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}" 
   exit 1
fi

# Load environment variables
if [ -f .env ]; then
    source .env
    echo -e "${GREEN}✓ Loaded environment variables${NC}"
else
    echo -e "${YELLOW}⚠ .env file not found. Copying from .env.example${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your configuration and run again${NC}"
    exit 1
fi

# Update system
echo -e "\n${YELLOW}Updating system packages...${NC}"
apt update && apt upgrade -y

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
apt install -y curl wget git vim htop

# Setup GPU passthrough
echo -e "\n${YELLOW}Setting up GPU passthrough...${NC}"
bash scripts/setup-gpu.sh

# Install NVIDIA drivers
echo -e "\n${YELLOW}Installing NVIDIA drivers...${NC}"
bash scripts/install-nvidia.sh

# Install Docker
echo -e "\n${YELLOW}Installing Docker...${NC}"
bash scripts/install-docker.sh

# Deploy services
echo -e "\n${YELLOW}Deploying Docker services...${NC}"
cd docker
docker-compose up -d

# Wait for services to start
echo -e "\n${YELLOW}Waiting for services to start...${NC}"
sleep 30

# Download default models
echo -e "\n${YELLOW}Downloading default AI models...${NC}"
docker exec ollama ollama pull llama2
docker exec ollama ollama pull mistral

echo -e "\n${GREEN}✓ Installation completed successfully!${NC}"
echo -e "\nAccess your services at:"
echo -e "  🤖 Open WebUI: https://${AI_SUBDOMAIN}.${DOMAIN}"
echo -e "  🔄 n8n: https://${N8N_SUBDOMAIN}.${DOMAIN}"
echo -e "  🖥️  Proxmox: https://${PVE_SUBDOMAIN}.${DOMAIN}:8006"