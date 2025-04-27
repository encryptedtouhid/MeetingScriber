#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "Uninstalling MeetingScriber broadcaster service..."

# Stop and unload the service
launchctl unload ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist 2>/dev/null
sudo launchctl bootout system/com.meetingscriber.broadcaster 2>/dev/null

# Remove the plist file
if [ -f ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist ]; then
    rm ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist
fi

# Kill any running processes
pkill -f "python.*broadcaster/main.py" 2>/dev/null

# Clean up logs
if [ -d "${PROJECT_DIR}/logs" ]; then
    rm -f "${PROJECT_DIR}/logs/broadcaster."*
fi

echo "Broadcaster service has been uninstalled successfully"