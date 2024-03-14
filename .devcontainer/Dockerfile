# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for building liberasurecode
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    autoconf \
    automake \
    libtool \
    python3-dev

# Clone and install liberasurecode from source
RUN git clone https://github.com/openstack/liberasurecode.git /tmp/liberasurecode && \
    cd /tmp/liberasurecode && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    ldconfig

# Install pyeclib
RUN pip install pyeclib

# Copy the current directory contents into the container at /usr/src/app
COPY . .
