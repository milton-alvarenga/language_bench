# Start with a minimal Debian-based image
FROM debian:bookworm

# Install necessary tools and libraries
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    libpq5 \
    libpq-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Keep the container running interactively
CMD [ "bash" ]
