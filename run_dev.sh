#!/bin/bash

set -e

# Load the .env file
source .env

# Make sure permissions are still good for new update file
chmod u+x run_dev.sh

# Copy root files in case of updates
cp .env db/.env
cp .env web/.env
cp .dockerignore db/.dockerignore
cp .dockerignore web/.dockerignore

# Set debug = True for development
sed -i '' 's|^DEBUG[[:space:]]*=[[:space:]]*False[[:space:]]*#Bash_Target|DEBUG = True #Bash_Target|' "web/project/settings.py"

# Rebuild the containers
docker compose -f docker-compose.yml up --build -d

exit
