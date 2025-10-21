bash#!/bin/bash

# Create config directory structure
mkdir -p configs/{cloudflare,proxmox,nvidia}

# Create all config files
cat > configs/cloudflare/tunnel-config.yml << 'EOF'
[Content from above]
EOF

cat > configs/proxmox/vm-template.conf << 'EOF'
[Content from above]
EOF

cat > configs/nvidia/blacklist.conf << 'EOF'
[Content from above]
EOF

cat > configs/nvidia/vfio.conf << 'EOF'
[Content from above]
EOF

echo "✓ Configuration files created successfully!"
Make executable:
bashchmod +x configs/create-configs.sh