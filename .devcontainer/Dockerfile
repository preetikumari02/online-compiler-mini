FROM mcr.microsoft.com/devcontainers/python:3.11

# Install C++ compiler and required tools
RUN apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace