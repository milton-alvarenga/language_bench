FROM php:8.2-cli

# Install PostgreSQL PDO driver
RUN apt-get update && apt-get install -y \
    libpq-dev \
    procps \
    && docker-php-ext-install pdo_pgsql && apt-get clean