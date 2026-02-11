#!/bin/bash

# Change permissions of volumes inside container
# Will be copied over to host server
# Just make sure host container has permissions through
# /var/lib/docker/volumes
VOLUMES=(
    "/app/staticfiles"
    "/app/media"
    "/app/logs"
    "/app/static"
)

# sudo chown -R www-data:www-data /app/static || true
# sudo chmod -R 755 /app/static || true

for dir in "${VOLUMES[@]}"; do
    mkdir -p "$dir"
    # chmod -R g+rwX "$dir"
done

touch /app/logs/django_logs.txt

until pg_isready -h db -p 5432; do
  echo "Waiting for database..."
  sleep 1
done

# Read the theme  files
python3 generate_themes.py

# Collect static files
python3 manage.py collectstatic --noinput

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

exec "$@"