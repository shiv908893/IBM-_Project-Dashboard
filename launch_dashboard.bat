@echo off
cd /d "%~dp0"
PowerShell -NoLogo -NoProfile -NoExit -ExecutionPolicy Bypass -File "%~dp0launch_dashboard.ps1"
