# For local development and testing only.

FROM --platform=linux/amd64 ubuntu:16.04

# Install sudo
RUN apt-get update && apt-get install -y sudo

# Create a new user "devuser" with user ID 1000
RUN useradd -m -s /bin/bash -u 1000 devuser

# Add the user to the sudo group
RUN usermod -aG sudo devuser

# Set up password-less sudo for the user
RUN echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to the new user
USER devuser

# Install OS level dependencies
RUN sudo apt-get update && sudo apt-get install -y \
  python \
  python-pip \
  build-essential \
  libssl-dev \
  libffi-dev \
  python-dev \
  wkhtmltopdf \
  xauth \
  xvfb \
  postgresql \
  libpq-dev \
  redis-server \
  git \
  curl \
  vim

# Start PostgreSQL, set a password and create eaa database
USER postgres
RUN service postgresql start && \
  psql -c "ALTER USER postgres PASSWORD 'password';" && \
  psql -c "CREATE ROLE eaa WITH LOGIN PASSWORD 'password';" && \
  psql -c "CREATE DATABASE donations;" && \
  psql -c "GRANT ALL PRIVILEGES ON DATABASE donations TO eaa;"
USER devuser

# Upgrade pip to the last version that supports Python 2.7 and install the last
# version of virtualenv that works for Python 2.7
RUN pip install --upgrade "pip<21.0" && \
  pip install virtualenv==16.7.10

# Set the working directory
# WORKDIR /usr/src/app

# Copy over all the files from this repo
# COPY . .

# Install nvm and node
ENV NVM_DIR=/home/devuser/.nvm
RUN mkdir $NVM_DIR && \
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
  . $NVM_DIR/nvm.sh && nvm install 8.14.0

# Create and activate a Python virtual environment and install the dependencies
# RUN virtualenv donation_portal_env && \
#   . donation_portal_env/bin/activate && \
#   pip install -r deps/pip.base && \
#   pip install -r deps/pip

# Fix "missing locales" errors in this Ubuntu image
RUN sudo locale-gen "en_US.UTF-8"

# Document that the service listens on port 8000. Note, this doesn't actually
# open the port - you'll need to run `docker run -p 8000:8000 <image name>`.
EXPOSE 8000