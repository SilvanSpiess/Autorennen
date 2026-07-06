#!/bin/bash
echo "========================================================"
echo "Building Car Race Game 3.0 for macOS..."
echo "========================================================"

# PyInstaller command using direct CLI flags
pyinstaller --noconsole --onefile --name "Car Race Game 3.0" --icon="resources/assets/icon.icns" --windowed --noconfirm --add-data "resources:resources" car_race_3_0.py

echo "Build complete! Check the 'dist' folder for your .app bundle."