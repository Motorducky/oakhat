# OAK-D Lite Setup Guide

## Hardware
- Raspberry Pi Zero 2W
- OAK-D Lite (Luxonis) Fixed Focus
- USB-C to micro-USB DATA cable
- 256GB microSD
- 5V power supply

## Pi Ports (left to right, ports facing you)
1. mini HDMI - video
2. micro USB - DATA/OTG - **camera here**
3. micro USB - PWR - **power here**

## Initial Setup
1. Flash Raspberry Pi OS Lite (64-bit)
2. Configure WiFi/SSH before first boot
3. Boot, SSH in

## Verify Camera
```bash
lsusb | grep 03e7
# Should show: ID 03e7:2485 Intel Movidius MyriadX
```

## Install
```bash
chmod +x install.sh
./install.sh
```

## Start Recording
```bash
sudo systemctl start oakrecord
curl http://localhost:8080
```

## Known Issues

### Video upside down
Recording is upside down. Flip in post:
```bash
ffmpeg -i input.mp4 -vf "rotate=PI" output.mp4
```

### Camera shows f63b instead of 2485
Camera stuck in bootloader. Fix:
```bash
sudo systemctl disable oakrecord
sudo reboot
# Wait 60 sec, SSH back
sudo systemctl enable oakrecord
sudo systemctl start oakrecord
```

## DepthAI v3 API Notes
- depthai 3.2.1
- Uses `dai.Pipeline()` context manager
- Uses `pipeline.create(dai.node.Camera).build()`
- Uses `.requestOutput((w,h)).createOutputQueue()`
- NO XLinkOut in v3
- NO setOrientation on Camera in v3

## Data Rates
- RGB 1080p H.265: ~10 MB/min
- Mono 480p x2: ~4 MB/min
- Total: ~14 MB/min / 840 MB/hr / 6.7 GB per 8hr shift
