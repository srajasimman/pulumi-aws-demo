#!/bin/bash

set -e

# Install nginx webserver
sudo apt-get update
sudo apt-get install -y nginx

# Enable nginx webserver
sudo systemctl enable nginx

# Start nginx webserver
sudo systemctl start nginx