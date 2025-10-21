#!/bin/bash

echo "🏥 System Health Check"
echo "======================"

# Check GPU
echo -e "\n📊 GPU Status:"
nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader

# Check Docker containers
echo -e "\n🐳 Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check Ollama
echo -e "\n🤖 Ollama Status:"
curl -s http://localhost:11434/api/tags | jq -r '.models[].name'

# Check disk space
echo -e "\n💾 Disk Usage:"
df -h | grep -E "/$|/var/lib/docker"

# Check memory
echo -e "\n🧠 Memory Usage:"
free -h