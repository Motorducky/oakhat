# OAK-D Lite Command Reference

## Device: oakcam1.local (192.168.1.126)
## User: motorducky

## SSH Access
```bash
# Mac terminal
ssh motorducky@oakcam1.local
```

## Recording Service
```bash
# oakcam1 terminal
sudo systemctl status oakrecord    # Check
sudo systemctl start oakrecord     # Start
sudo systemctl stop oakrecord      # Stop
sudo systemctl restart oakrecord   # Restart
sudo systemctl enable oakrecord    # Auto-start on boot
sudo systemctl disable oakrecord   # Disable auto-start
journalctl -u oakrecord -f         # View logs
```

## Check Status
```bash
# Mac terminal
curl http://oakcam1.local:8080
```

## Camera Health
```bash
# oakcam1 terminal
lsusb | grep 03e7                      # Should show 2485
python3 ~/oak_scripts/test_camera.py   # 5-second test
```

## Live Stream
```bash
# oakcam1 terminal
sudo systemctl stop oakrecord
python3 ~/oak_scripts/stream.py
# Open http://oakcam1.local:5000
```

## Pull Recordings
```bash
# Mac terminal
ssh motorducky@oakcam1.local "ls -lh ~/recordings/"
scp "motorducky@oakcam1.local:~/recordings/*.h265" ~/Desktop/
ffmpeg -i ~/Desktop/FILE_rgb.h265 -c copy ~/Desktop/rgb.mp4
```

## Troubleshooting - Camera Stuck
```bash
# oakcam1 terminal
sudo systemctl disable oakrecord
sudo reboot
# Wait 60 sec, SSH back
lsusb | grep 03e7    # Should show 2485
sudo systemctl enable oakrecord
sudo systemctl start oakrecord
```

## Storage
- ~14 MB/min total
- ~840 MB/hr
- ~6.7 GB per 8hr shift
