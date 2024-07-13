#!/bin/bash

# Change ownership of the log directory to the user running the Flask application
sudo chown -R $USER:$USER /var/log/messaging_system.log

# Set permissions so that the owner can read, write, and execute files in the directory
sudo chmod -R 700 /var/log/messaging_system.log

echo "Permissions updated."
