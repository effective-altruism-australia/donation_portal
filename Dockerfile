# For local development and testing only.

FROM ubuntu:16.04

# Install OS level dependencies
RUN apt-get update && apt-get install -y \
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
  psql -c "CREATE DATABASE eaa;"
USER root

# Upgrade pip to the last version that supports Python 2.7 and install the last
# version of virtualenv that works for Python 2.7
RUN pip install --upgrade "pip<21.0" && \
  pip install virtualenv==16.7.10

# Set the working directory
WORKDIR /usr/src/app

# Copy over all the files from this repo
COPY . .

# Install nvm and node
ENV NVM_DIR /usr/src/app/.nvm
RUN mkdir $NVM_DIR && \
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
  . $NVM_DIR/nvm.sh && nvm install 8.14.0

# Create and activate a Python virtual environment and install the dependencies
RUN virtualenv donation_portal_env && \
  . donation_portal_env/bin/activate && \
  pip install -r deps/pip.base && \
  pip install -r deps/pip

# Document that the service listens on port 8000. Note, this doesn't actually
# open the port - you'll need to run `docker run -p 8000:8000 <image name>`.
EXPOSE 8000