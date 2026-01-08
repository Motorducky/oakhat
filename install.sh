#!/bin/bash
# OAK-D Lite Hat Camera System Installer
# Run on Raspberry Pi Zero 2W

set -e

echo "=== OAK-D Lite Hat Camera Installer ==="

mkdir -p ~/oak_scripts ~/recordings ~/snapshots

echo "Installing system dependencies..."
sudo apt update
sudo apt install -y tesseract-ocr

echo "Installing Python dependencies..."
pip install depthai flask opencv-python-headless pytesseract pillow --break-system-packages

echo "Adding udev rules..."
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

echo "Installing scripts..."
cp scripts/*.py ~/oak_scripts/
chmod +x ~/oak_scripts/*.py

echo "Creating systemd service..."
sudo tee /etc/systemd/system/oakrecord.service << 'SERVICE'
[Unit]
Description=OAK-D Lite Recording Service
After=network.target

[Service]
Type=simple
User=motorducky
WorkingDirectory=/home/motorducky
ExecStart=/usr/bin/python3 /home/motorducky/oak_scripts/record_with_status.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable oakrecord.service

echo ""
echo "=== INSTALL COMPLETE ==="
echo "Test: python3 ~/oak_scripts/test_camera.py"
echo "Start: sudo systemctl start oakrecord"
echo "Status: curl http://localhost:8080"
