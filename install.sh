#!/bin/bash

##### change container/network name to customer name to avoid conflict #####
##### ^ will require refactoring code here and in other files #####
##### add conditional use of email here and in web
##### restart nginx ?
##### add getting certificate (must be run after subdomain created on server)
#### add /run_prod.sh at end
#### add curl? on mozilla site checker at end?

###############################################################################
# Get arguments for dev vs prod
###############################################################################
DEV_MODE=0
PROD_MODE=0
USE_DEFAULTS=0
MODE=""
USE_EMAIL=""
USE_ACCOUNT=""

while getopts "dpuae" opt; do 
    case $opt in 
        d) DEV_MODE=1 ;;
        p) PROD_MODE=1 ;;
        u) USE_DEFAULTS=1 ;;
        a) USE_ACCOUNT="True" ;;
        e) USE_EMAIL="True" ;;
    esac 
done 

#  Get the user input for using either dev or prod
if (( PROD_MODE && DEV_MODE )); then  # User flaged prod and dev
    echo "Error: cannot use prod (-p) and dev (-d)"
    echo "Exiting..."
    exit
elif (( ! PROD_MODE && ! DEV_MODE )); then  # User didn't flag eithr prod or dev
    while true; do
        read -p "Use prod (p) or dev (d): " MODE
        if [[ "$MODE" == "p" ]]; then
            PROD_MODE=1
            MODE="p"
            break
        elif [[ "$MODE" == "d" ]]; then
            DEV_MODE=1
            MODE="d"
            break
        else 
            echo "Invalid input. Type (p) for prod or (d) for dev."
        fi
    done
fi

#  Update the directory based on the mode
if (( DEV_MODE )); then
    echo "-d was used"
    BASE_DIRECTORY="/Users/jeremy/Desktop"
else
    echo "-p was used"
    BASE_DIRECTORY="/home/developer"
fi

# Prompot for values or use defaults for testing
if (( USE_DEFAULTS )); then
    CONTAINER_PORT="8000"
    PROJECT_NAME="test_project"
    CUSTOMER_NAME="test_customer"
    GH_USER="test_user"
    GH_TOKEN="test_token"
    EMAIL_USER="test_email_user"
    EMAIL_HOST="test_email_host"
else
    read -p "Project Name: " PROJECT_NAME
    read -p "Container Port: " CONTAINER_PORT
    read -p "Github User: " GH_USER
    read -p "GitHub Token: " GH_TOKEN
    read -p "Customer Name: " CUSTOMER_NAME
    if [[ "$USE_EMAIL" == "True"  ]]; then
        read -p "Email Password: " EMAIL_PASSWORD
        read -p "Email User: " EMAIL_USER
        read -p "Email Host: " EMAIL_HOST
    fi 
fi

DOMAIN_NAME="${PROJECT_NAME}.programmingondemand.com"
CONTAINER_NAME="$PROJECT_NAME"

exit

###############################################################################
# Create the .env file
###############################################################################
ENV_FILE=".env"
rm $ENV_FILE
touch $ENV_FILE

###############################################################################
# Define functions for use in the program
###############################################################################
# Writes a secret to the .env file
# $1 = key and $2 = value
write_secret(){
    printf '\n%s="%s"' "$1" "$2" >> $ENV_FILE
}

# Writes a comment for readability in .env file
write_comment(){
    printf '\n\n# %s' "$1" >> $ENV_FILE
}

# Encrypts a secret. $1 is the plain text secret and $2 is the plain text key
encrypt_secret(){
    printf "%s" "$1" | \
    openssl enc -aes-256-cbc -pbkdf2 -salt -base64 -pass pass:"$2" 
}

# Decrypts a secret. $1 is the encrypted secret and $2 is the plain text key
decrypt_secret(){
    printf "%s\n" "$1" | \
    openssl enc -aes-256-cbc -pbkdf2 -d -base64 -pass pass:"$2" 
}

###############################################################################
# Make sure that the container and directory does not already exist
###############################################################################
PROJECT_DIRECTORY="${BASE_DIRECTORY}/${PROJECT_NAME}"

# Check the project directory
if [ -d "$PROJECT_DIRECTORY" ]; then
    echo "Project Directory already exists, exiting"
    exit
else
    cd $BASE_DIRECTORY
    pwd
fi

# Check the Docker container
if [ "$(docker ps -a -q -f name="$CONTAINER_NAME")" ]; then
    echo "Container already exists, exiting"
    exit
fi

###############################################################################
# Create directory and pull base code from GitHub
###############################################################################
# git clone https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${PROJECT_NAME} $PROJECT_NAME
# cd $PROJECT_DIRECTORY

###############################################################################
# Update the nginx file
###############################################################################
# NGINX_TEMPLATE_PATH="nginx.txt"
NGINX_TEMPLATE_PATH="test_nginx.txt"
PROD_NGINX_PATH="/etc/nginx/sites-available/${PROJECT_NAME}"

# Make the necessary changes
if (( DEV_MODE )); then
    sed -i '' "s|<<DOMAIN_NAME>>|${DOMAIN_NAME}|g" "$NGINX_TEMPLATE_PATH"
    sed -i '' "s|<<PROJECT_NAME>>|${PROJECT_NAME}|g" "$NGINX_TEMPLATE_PATH"
    sed -i '' "s|<<CONTAINER_PORT>>|${CONTAINER_PORT}|g" "$NGINX_TEMPLATE_PATH"
else 
    sed -i "s|<<DOMAIN_NAME>>|${DOMAIN_NAME}|" "$NGINX_TEMPLATE_PATH"
    sed -i "s|<<PROJECT_NAME>>|${PROJECT_NAME}|g" "$NGINX_TEMPLATE_PATH"
    sed -i "s|<<CONTAINER_PORT>>|${CONTAINER_PORT}|g" "$NGINX_TEMPLATE_PATH"
    cp $NGINX_TEMPLATE_PATH $PROD_NGINX_PATH
    sudo ln -s $PROD_NGINX_PATH /etc/nginx/sites-enabled/
fi

###############################################################################
# Create an encryption key generate a db password and django secret
###############################################################################
ENCRYPTION_KEY=$(openssl rand -hex 32)
DB_PASSWORD=$(openssl rand -hex 32)
DJANGO_SECRET=$(openssl rand -hex 32)

###############################################################################
# Encrypt the necessary secrets
###############################################################################
ENCRYPTED_DB_PASSWORD="$(encrypt_secret "$DB_PASSWORD" "$ENCRYPTION_KEY")"
ENCRYPTED_DJANGO_SECRET="$(encrypt_secret "$DJANGO_SECRET" "$ENCRYPTION_KEY")"
ENCRYPTED_GH_TOKEN="$(encrypt_secret "$GH_TOKEN" "$ENCRYPTION_KEY")"
ENCRYPTED_GH_USER="$(encrypt_secret "$GH_USER" "$ENCRYPTION_KEY")"
ENCRYPTED_EMAIL_PASSWORD="$(encrypt_secret "$ENCRYPTED_EMAIL_PASSWORD" "$ENCRYPTION_KEY")"
ENCRYPTED_EMAIL_HOST="$(encrypt_secret "$ENCRYPTED_EMAIL_HOST" "$ENCRYPTION_KEY")"
ENCRYPTED_EMAIL_USER="$(encrypt_secret "$ENCRYPTED_EMAIL_USER" "$ENCRYPTION_KEY")"

###############################################################################
# Write the .env file
###############################################################################
write_comment "[DOCKER]"
write_secret "PROJECT_NAME" "$PROJECT_NAME"
write_secret "CUSTOMER_NAME" "$CUSTOMER_NAME"
write_secret "CONTAINER_PORT" "$CONTAINER_PORT"
write_secret "NETWORK_NAME" "${PROJECT_NAME}_network"
write_secret "DOMAIN_NAME" "$DOMAIN_NAME"

write_comment "[DATABASE]"
write_secret "DB_USER" "${PROJECT_NAME}_user"
write_secret "DB_NAME" "$PROJECT_NAME"
write_secret "DB_PASSWORD" "$ENCRYPTED_DB_PASSWORD"
write_secret "DB_PORT" "5432"
write_secret "DB_HOST" "db"

write_comment "[DJANGO]"
write_secret "DJANGO_SECRET" "$ENCRYPTED_DJANGO_SECRET"
write_secret "USE_ACCOUNT" "False"

write_comment "[GITHUB]"
write_secret "GH_USER" "$ENCRYPTED_GH_USER"
write_secret "GH_TOKEN" "$ENCRYPTED_GH_TOKEN"

write_comment "[EMAIL]"
write_secret "USE_EMAIL" "False"
write_secret "EMAIL_USER" "$ENCRYPTED_EMAIL_USER"
write_secret "EMAIL_PASSWORD" "$ENCRYPTED_EMAIL_PASSWORD"
write_secret "EMAIL_PORT" "587"
write_secret "EMAIL_HOST" "$ENCRYPTED_EMAIL_HOST"

write_comment "[KEYS]"
write_secret "ENCRYPTION_KEY" "$ENCRYPTION_KEY"

exit