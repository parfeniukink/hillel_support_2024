# /bin/bash

cd ~/projects/hillel_support_2024

git pull
docker compose build && docker compose down && docker compose up -d

echo "🚀 Successfully deployed"