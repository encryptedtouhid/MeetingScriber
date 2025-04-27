#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "Uninstalling MeetingScriber broadcaster service..."

# Stop and disable the service
sudo systemctl stop meetingscriber-broadcaster 2>/dev/null
sudo systemctl disable meetingscriber-broadcaster 2>/dev/null

# Remove the service file
if [ -f /etc/systemd/system/meetingscriber-broadcaster.service ]; then
    sudo rm /etc/systemd/system/meetingscriber-broadcaster.service
    sudo systemctl daemon-reload
fi

# Kill any running processes
pkill -f "python.*broadcaster/main.py" 2>/dev/null

# Clean up logs
if [ -d "${PROJECT_DIR}/logs" ]; then
    rm -f "${PROJECT_DIR}/logs/broadcaster."*
fi

echo "Broadcaster service has been uninstalled successfully"