# Makefile for Docker Compose operations

.PHONY: help start stop restart logs status clean update backup restore models

# Default target
help:
	@echo "AI Infrastructure Docker Management"
	@echo ""
	@echo "Available commands:"
	@echo "  make start       - Start all services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs (all services)"
	@echo "  make status      - Show service status"
	@echo "  make clean       - Clean up unused resources"
	@echo "  make update      - Update all services"
	@echo "  make backup      - Backup all volumes"
	@echo "  make restore     - Restore from backup"
	@echo "  make models      - Download default AI models"
	@echo "  make prod        - Start in production mode"
	@echo "  make dev         - Start in development mode"

# Check if .env exists
.env:
	@echo "Creating .env from .env.example..."
	@cp .env.example .env
	@echo "Please edit .env with your configuration"

# Development mode
dev: .env
	docker compose up -d

# Production mode
prod: .env
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Start services
start: .env
	docker compose up -d
	@echo "Services started!"
	@echo "Open WebUI: http://localhost:3000"
	@echo "n8n: http://localhost:5678"
	@echo "Portainer: http://localhost:9000"

# Stop services
stop:
	docker compose down

# Restart services
restart:
	docker compose restart

# View logs
logs:
	docker compose logs -f

# Logs for specific service
logs-ollama:
	docker compose logs -f ollama

logs-webui:
	docker compose logs -f open-webui

logs-n8n:
	docker compose logs -f n8n

# Show status
status:
	@echo "=== Docker Services Status ==="
	@docker compose ps
	@echo ""
	@echo "=== Resource Usage ==="
	@docker stats --no-stream
	@echo ""
	@echo "=== GPU Status ==="
	@nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader

# Clean up
clean:
	docker compose down
	docker system prune -f
	@echo "Cleanup complete!"

# Update services
update:
	docker compose pull
	docker compose up -d
	@echo "Services updated!"

# Backup volumes
backup:
	@mkdir -p backups
	@echo "Backing up Ollama data..."
	@docker run --rm \
		-v ollama_data:/data \
		-v $(PWD)/backups:/backup \
		ubuntu tar czf /backup/ollama-$$(date +%Y%m%d-%H%M%S).tar.gz /data
	@echo "Backing up Open WebUI data..."
	@docker run --rm \
		-v open-webui_data:/data \
		-v $(PWD)/backups:/backup \
		ubuntu tar czf /backup/webui-$$(date +%Y%m%d-%H%M%S).tar.gz /data
	@echo "Backing up n8n data..."
	@docker run --rm \
		-v n8n_data:/data \
		-v $(PWD)/backups:/backup \
		ubuntu tar czf /backup/n8n-$$(date +%Y%m%d-%H%M%S).tar.gz /data
	@echo "Backup complete! Files in backups/"

# Restore from backup (specify BACKUP_FILE=filename)
restore:
ifndef BACKUP_FILE
	@echo "Error: Specify backup file with BACKUP_FILE=filename"
	@echo "Example: make restore BACKUP_FILE=backups/ollama-20240101-120000.tar.gz"
else
	@echo "Restoring from $(BACKUP_FILE)..."
	@docker run --rm \
		-v ollama_data:/data \
		-v $(PWD):/backup \
		ubuntu tar xzf /backup/$(BACKUP_FILE) -C /
	@echo "Restore complete! Restart services with 'make restart'"
endif

# Download AI models
models:
	@echo "Downloading default AI models..."
	@echo "This may take several minutes..."
	@docker exec ollama ollama pull llama2
	@docker exec ollama ollama pull mistral
	@docker exec ollama ollama pull codellama
	@echo "Models downloaded! List with: docker exec ollama ollama list"

# Download specific model
model:
ifndef MODEL
	@echo "Error: Specify model with MODEL=name"
	@echo "Example: make model MODEL=llama2:13b"
else
	@echo "Downloading $(MODEL)..."
	@docker exec ollama ollama pull $(MODEL)
	@echo "Model $(MODEL) downloaded!"
endif

# List models
list-models:
	@docker exec ollama ollama list

# Remove model
remove-model:
ifndef MODEL
	@echo "Error: Specify model with MODEL=name"
	@echo "Example: make remove-model MODEL=llama2"
else
	@docker exec ollama ollama rm $(MODEL)
	@echo "Model $(MODEL) removed!"
endif

# Health check
health:
	@echo "=== Service Health Check ==="
	@echo "Ollama:"
	@curl -s http://localhost:11434/api/tags | jq -r '.models[].name' || echo "Not accessible"
	@echo ""
	@echo "Open WebUI:"
	@curl -s http://localhost:3000/health || echo "Not accessible"
	@echo ""
	@echo "n8n:"
	@curl -s http://localhost:5678/healthz || echo "Not accessible"

# Show disk usage
disk:
	@echo "=== Disk Usage ==="
	@df -h | grep -E "Filesystem|/$"
	@echo ""
	@echo "=== Docker Disk Usage ==="
	@docker system df
	@echo ""
	@echo "=== Volume Sizes ==="
	@docker system df -v | grep VOLUME

# Execute shell in container
shell-ollama:
	docker exec -it ollama /bin/bash

shell-webui:
	docker exec -it open-webui /bin/bash

shell-n8n:
	docker exec -it n8n /bin/sh

# Reset everything (DANGEROUS!)
reset:
	@echo "WARNING: This will delete all data!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm; \
	if [ "$confirm" = "yes" ]; then \
		docker compose down -v; \
		docker system prune -af; \
		echo "Reset complete!"; \
	else \
		echo "Cancelled."; \
	fi

# Install/setup
install: .env
	@echo "Setting up AI Infrastructure..."
	@docker compose pull
	@docker compose up -d
	@echo "Waiting for services to start..."
	@sleep 30
	@echo "Downloading default models..."
	@make models
	@echo ""
	@echo "Installation complete!"
	@echo ""
	@echo "Access your services at:"
	@echo "  Open WebUI: http://localhost:3000"
	@echo "  n8n: http://localhost:5678"
	@echo "  Portainer: http://localhost:9000"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure Cloudflare Tunnel for external access"
	@echo "  2. Set up authentication (see docker/README.md)"
	@echo "  3. Start chatting!"

# Quick commands
up: start
down: stop
ps: status
build:
	docker compose build

# GPU check
gpu:
	@nvidia-smi

# Network info
network:
	@docker network ls
	@echo ""
	@docker network inspect ai-network | jq '.[0].Containers'