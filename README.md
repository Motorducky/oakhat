README.md
LICENSE
install.sh
.gitignore
docs/COMMANDS.md
docs/SETUP_GUIDE.md
scripts/test_camera.py
scripts/stream.py
scripts/record_with_status.py
scripts/ocr_snapshot.py


# OAK-D Lite Hat Camera System

Wearable POV camera system for AI training data capture using OAK-D Lite and Raspberry Pi Zero 2W.

## Hardware

| Component | Spec |
|-----------|------|
| Camera | OAK-D Lite (Luxonis) Fixed Focus |
| Compute | Raspberry Pi Zero 2W |
| Storage | 256GB microSD |
| Power | 5V to Pi PWR port |

## Features

- **3-camera recording**: RGB 1080p + stereo mono 480p
- **H.265 encoding**: ~14 MB/min total
- **Auto-start on boot**: systemd service
- **Status endpoint**: HTTP server on port 8080
- **Live streaming**: MJPEG to browser on port 5000
- **OCR snapshots**: Tesseract integration

## Quick Start
```bash
# SSH into Pi
ssh motorducky@oakcam1.local

# Install everything
chmod +x install.sh
./install.sh

# Start recording
sudo systemctl start oakrecord

# Check status
curl http://oakcam1.local:8080
```

## Scripts

| Script | Purpose |
|--------|---------|
| `test_camera.py` | Quick 5-second camera test |
| `stream.py` | Live view in browser (:5000) |
| `record_with_status.py` | Record all 3 cameras with status endpoint (:8080) |
| `ocr_snapshot.py` | Take snapshots and run OCR |

## Pull Recordings
```bash
# From Mac
scp "motorducky@oakcam1.local:~/recordings/*.h265" ~/Desktop/

# Convert to mp4
ffmpeg -i recording_rgb.h265 -c copy recording.mp4
```

## Service Commands
```bash
sudo systemctl start oakrecord    # Start
sudo systemctl stop oakrecord     # Stop
sudo systemctl status oakrecord   # Check
sudo systemctl restart oakrecord  # Restart
journalctl -u oakrecord -f        # Logs
```

## Troubleshooting

### Camera stuck (lsusb shows f63b instead of 2485)
```bash
sudo systemctl disable oakrecord
sudo reboot
# Wait 60 sec, SSH back
sudo systemctl enable oakrecord
sudo systemctl start oakrecord
```

### Video upside down
Flip in post:
```bash
ffmpeg -i input.mp4 -vf "rotate=PI" output.mp4
```

## Data Rates

- RGB 1080p H.265: ~10 MB/min
- Mono 480p x2: ~4 MB/min
- **Total: ~14 MB/min / 840 MB/hr / 6.7 GB per 8hr shift**

## Requirements

- Raspberry Pi OS Lite (64-bit)
- Python 3.11+
- DepthAI 3.2.1+

## License

MIT License - See LICENSE file

## Author

Corbett Griffith / Kue King Sculpture / Blue Collar Raw
