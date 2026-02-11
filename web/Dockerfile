# Pull Python Image
FROM python:3.10-slim

# Read container port from .env file
ARG CONTAINER_PORT
ENV CONTAINER_PORT=$CONTAINER_PORT

# Set work directory
WORKDIR /app

# Update packages
RUN apt-get update && apt-get install -y postgresql-client sudo passwd nano curl

# Upgrade Pip
RUN pip3 install --upgrade pip

# Install dependencies
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN rm -rf staticfiles/*
RUN cp -r static/* staticfiles/

# Copy project
COPY . /app

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Grant permissions to the entrypoint bash file
COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

# Change container permissions
RUN mkdir -p /app/staticfiles /app/media /app/logs
RUN chown -R www-data:www-data /app
RUN chmod -R 755 /app
RUN chmod -R 775 /app/staticfiles /app/media /app/logs
USER www-data

# Run the entrypoint bash file
ENTRYPOINT ["/entry.sh"]

# Start the application using Gunicorn
CMD gunicorn --bind 0.0.0.0:$CONTAINER_PORT project.wsgi:application