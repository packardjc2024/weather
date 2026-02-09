#!/bin/bash

# Load the .env file
source .env

# Move into the project's root directory
cd /home/developer/${PROJECT_NAME}

# Decrypt secret values
decrypt_secret(){
    printf "%s\n" "$1" | \
    openssl enc -aes-256-cbc -pbkdf2 -d -base64 -pass pass:"$2" 
}
GH_USER="$(decrypt_secret "$GH_USER" "$ENCRYPTION_KEY")"
GH_TOKEN="$(decrypt_secret "$GH_TOKEN" "$ENCRYPTION_KEY")"

# Pull the GitHub repository
git stash
git pull https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${PROJECT_NAME}
git stash clear

# Make sure permissions are still good for new update file
sudo chmod u+x run_prod.sh

# Copy root files in case of updates
cp .env db/.env
cp .env web/.env
cp .dockerignore db/.dockerignore
cp .dockerignore web/.dockerignore

# Make Sure DEBUG = False in settings.py
sed -i 's|^DEBUG[[:space:]]*=[[:space:]]*True[[:space:]]*#Bash_Target|DEBUG = False #Bash_Target|' "web/project/settings.py"

# Rebuild the containers
# docker compose down
# docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

# Make sure volumes permissions are correct
sudo groupadd staticgroup
sudo usermod -aG staticgroup www-data

# Make sure the file paths exists with correct permissions
sudo mkdir -p /srv/docker/${PROJECT_NAME}/staticfiles
sudo mkdir -p /srv/docker/${PROJECT_NAME}/media
sudo mkdir -p /srv/docker/${PROJECT_NAME}/logs
sudo chown -R www-data:www-data /srv/docker/${PROJECT_NAME}

# Rebuild the containers
# docker compose down
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

exit
