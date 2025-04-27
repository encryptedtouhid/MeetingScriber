# Requires -RunAsAdministrator

# Get the absolute path of the project directory
$PROJECT_DIR = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Service name
$SERVICE_NAME = "MeetingScriber-Broadcaster"

Write-Host "Uninstalling MeetingScriber broadcaster service..."

# Stop and remove the service using NSSM
$NSSM_PATH = Join-Path $PROJECT_DIR "install_scripts\windows\nssm.exe"
if (Test-Path $NSSM_PATH) {
    & $NSSM_PATH stop $SERVICE_NAME 2>$null
    & $NSSM_PATH remove $SERVICE_NAME confirm 2>$null
}

# Kill any running processes
Get-Process | Where-Object { $_.Path -like "*python*" -and $_.CommandLine -like "*broadcaster\main.py*" } | Stop-Process -Force

# Clean up logs
$LOG_DIR = Join-Path $PROJECT_DIR "logs"
if (Test-Path $LOG_DIR) {
    Remove-Item -Path "$LOG_DIR\broadcaster.*" -Force
}

Write-Host "Broadcaster service has been uninstalled successfully"