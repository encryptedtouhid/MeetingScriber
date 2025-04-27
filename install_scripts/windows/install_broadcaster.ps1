# Requires -RunAsAdministrator

# Get the absolute path of the project directory
$PROJECT_DIR = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Create the NSSM service configuration
$SERVICE_NAME = "MeetingScriber-Broadcaster"
$PYTHON_PATH = Join-Path $PROJECT_DIR ".venv\Scripts\pythonw.exe"
$SCRIPT_PATH = Join-Path $PROJECT_DIR "broadcaster\main.py"
$LOG_DIR = Join-Path $PROJECT_DIR "logs"

# Create logs directory if it doesn't exist
if (-not (Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR
}

# Download NSSM if not present
$NSSM_PATH = Join-Path $PROJECT_DIR "install_scripts\windows\nssm.exe"
if (-not (Test-Path $NSSM_PATH)) {
    $NSSM_URL = "https://nssm.cc/release/nssm-2.24.zip"
    $NSSM_ZIP = Join-Path $PROJECT_DIR "install_scripts\windows\nssm.zip"
    
    Invoke-WebRequest -Uri $NSSM_URL -OutFile $NSSM_ZIP
    Expand-Archive -Path $NSSM_ZIP -DestinationPath "$PROJECT_DIR\install_scripts\windows\temp"
    Move-Item "$PROJECT_DIR\install_scripts\windows\temp\nssm-2.24\win64\nssm.exe" $NSSM_PATH
    Remove-Item -Path "$PROJECT_DIR\install_scripts\windows\temp" -Recurse
    Remove-Item -Path $NSSM_ZIP
}

# Remove existing service if it exists
& $NSSM_PATH stop $SERVICE_NAME 2>$null
& $NSSM_PATH remove $SERVICE_NAME confirm 2>$null

# Install the new service
& $NSSM_PATH install $SERVICE_NAME $PYTHON_PATH $SCRIPT_PATH
& $NSSM_PATH set $SERVICE_NAME AppDirectory $PROJECT_DIR
& $NSSM_PATH set $SERVICE_NAME DisplayName "MeetingScriber Broadcaster"
& $NSSM_PATH set $SERVICE_NAME Description "Audio capture and streaming service for MeetingScriber"
& $NSSM_PATH set $SERVICE_NAME AppStdout (Join-Path $LOG_DIR "broadcaster.log")
& $NSSM_PATH set $SERVICE_NAME AppStderr (Join-Path $LOG_DIR "broadcaster.error.log")
& $NSSM_PATH set $SERVICE_NAME AppRotateFiles 1
& $NSSM_PATH set $SERVICE_NAME AppRotateBytes 1048576

# Start the service
& $NSSM_PATH start $SERVICE_NAME

Write-Host "Broadcaster service installed and started. Check logs at $LOG_DIR"
Write-Host "Use 'services.msc' to manage the service"