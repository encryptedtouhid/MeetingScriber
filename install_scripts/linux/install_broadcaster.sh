#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Create the systemd service file
cat > /tmp/meetingscriber-broadcaster.service << EOL
[Unit]
Description=MeetingScriber Broadcaster Service
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=${PROJECT_DIR}
ExecStart=${PROJECT_DIR}/.venv/bin/python ${PROJECT_DIR}/broadcaster/main.py
Restart=always
RestartSec=5
StandardOutput=append:${PROJECT_DIR}/logs/broadcaster.log
StandardError=append:${PROJECT_DIR}/logs/broadcaster.error.log

[Install]
WantedBy=multi-user.target
EOL

# Create logs directory
mkdir -p "${PROJECT_DIR}/logs"

# Install the service
sudo mv /tmp/meetingscriber-broadcaster.service /etc/systemd/system/

# Reload systemd and enable/start the service
sudo systemctl daemon-reload
sudo systemctl enable meetingscriber-broadcaster
sudo systemctl start meetingscriber-broadcaster

echo "Broadcaster service installed and started. Check logs at ${PROJECT_DIR}/logs/"
echo "Use 'systemctl status meetingscriber-broadcaster' to check service status"