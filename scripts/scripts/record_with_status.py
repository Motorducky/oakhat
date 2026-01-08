#!/usr/bin/env python3
"""
Record all 3 cameras to H.265 video files
Saves to ~/recordings/ with timestamp
Status at http://oakcam1.local:8080
"""
import depthai as dai
import time
import os
from datetime import datetime
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

os.makedirs(os.path.expanduser('~/recordings'), exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
start_time = time.time()

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        elapsed = time.time() - start_time
        size_mb = sum(os.path.getsize(f'/home/motorducky/recordings/{timestamp}_{c}.h265') 
                      for c in ['rgb','left','right'] if os.path.exists(f'/home/motorducky/recordings/{timestamp}_{c}.h265')) / 1024 / 1024
        status = f"RECORDING\nTime: {elapsed:.0f}s\nSize: {size_mb:.1f}MB\nFile: {timestamp}"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(status.encode())
    def log_message(self, format, *args):
        pass

def run_status_server():
    HTTPServer(('0.0.0.0', 8080), StatusHandler).serve_forever()

Thread(target=run_status_server, daemon=True).start()
print(f'Status at http://oakcam1.local:8080')
print(f'Starting recording: {timestamp}')

with dai.Pipeline() as pipeline:
    cam_rgb = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
    enc_rgb = pipeline.create(dai.node.VideoEncoder)
    enc_rgb.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)
    cam_rgb.requestOutput((1920, 1080), dai.ImgFrame.Type.NV12).link(enc_rgb.input)
    q_rgb = enc_rgb.bitstream.createOutputQueue()
    
    cam_left = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    enc_left = pipeline.create(dai.node.VideoEncoder)
    enc_left.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)
    cam_left.requestOutput((640, 480)).link(enc_left.input)
    q_left = enc_left.bitstream.createOutputQueue()
    
    cam_right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    enc_right = pipeline.create(dai.node.VideoEncoder)
    enc_right.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H265_MAIN)
    cam_right.requestOutput((640, 480)).link(enc_right.input)
    q_right = enc_right.bitstream.createOutputQueue()
    
    pipeline.start()
    
    rgb_file = open(os.path.expanduser(f'~/recordings/{timestamp}_rgb.h265'), 'wb')
    left_file = open(os.path.expanduser(f'~/recordings/{timestamp}_left.h265'), 'wb')
    right_file = open(os.path.expanduser(f'~/recordings/{timestamp}_right.h265'), 'wb')
    
    try:
        while pipeline.isRunning():
            if q_rgb.has():
                rgb_file.write(q_rgb.get().getData())
            if q_left.has():
                left_file.write(q_left.get().getData())
            if q_right.has():
                right_file.write(q_right.get().getData())
    except KeyboardInterrupt:
        pass
    finally:
        rgb_file.close()
        left_file.close()
        right_file.close()
        print(f'Saved to ~/recordings/{timestamp}_*.h265')
