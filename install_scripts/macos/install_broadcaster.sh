#!/bin/bash

# Get the absolute path of the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Create the launchd plist file
cat > ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.meetingscriber.broadcaster</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PROJECT_DIR}/.venv/bin/python</string>
        <string>${PROJECT_DIR}/broadcaster/main.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${PROJECT_DIR}/logs/broadcaster.log</string>
    <key>StandardErrorPath</key>
    <string>${PROJECT_DIR}/logs/broadcaster.error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOL

# Create logs directory
mkdir -p "${PROJECT_DIR}/logs"

# Set correct permissions
chmod 644 ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist

# Load the service
launchctl load ~/Library/LaunchAgents/com.meetingscriber.broadcaster.plist

echo "Broadcaster service installed and started. Check logs at ${PROJECT_DIR}/logs/"