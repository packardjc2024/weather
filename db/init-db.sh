#!/bin/bash
set -e

source /.env

decrypt_secret(){
    printf "%s\n" "$1" | \
    openssl enc -aes-256-cbc -pbkdf2 -d -base64 -pass pass:"$2" 
}

DECRYPTED_PASSWORD="$(decrypt_secret "$DB_PASSWORD" "$ENCRYPTION_KEY")"

# Start the PostgreSQL service and create the database and user
psql -v ON_ERROR_STOP=1 --username $DB_USER --dbname postgres <<-EOSQL
    ALTER ROLE $DB_USER WITH ENCRYPTED PASSWORD '$DECRYPTED_PASSWORD';
    \c $DB_NAME;
EOSQL

# Copy my pg_hba.conf file to require password login and block host server access
rm /var/lib/postgresql/data/pg_hba.conf
cp /tmp/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf

# reload .conf
psql -U "$DB_USER" -d postgres -c "SELECT pg_reload_conf();"
