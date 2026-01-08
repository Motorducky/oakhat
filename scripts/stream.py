#!/usr/bin/env python3
"""
Stream all 3 OAK-D Lite cameras to browser via MJPEG
Access at http://oakcam1.local:5000
"""
import depthai as dai
from flask import Flask, Response
import cv2
import numpy as np

app = Flask(__name__)

def gen_frames():
    with dai.Pipeline() as pipeline:
        cam = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
        left = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
        right = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
        
        q_rgb = cam.requestOutput((640, 400)).createOutputQueue()
        q_left = left.requestOutput((320, 200)).createOutputQueue()
        q_right = right.requestOutput((320, 200)).createOutputQueue()
        
        pipeline.start()
        while pipeline.isRunning():
            rgb = cv2.rotate(q_rgb.get().getCvFrame(), cv2.ROTATE_180)
            l = cv2.rotate(q_left.get().getCvFrame(), cv2.ROTATE_180)
            r = cv2.rotate(q_right.get().getCvFrame(), cv2.ROTATE_180)
            
            if len(l.shape) == 2:
                l = cv2.cvtColor(l, cv2.COLOR_GRAY2BGR)
            if len(r.shape) == 2:
                r = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)
            
            stereo = np.hstack([l, r])
            stereo = cv2.resize(stereo, (640, 200))
            combined = np.vstack([rgb, stereo])
            
            _, jpg = cv2.imencode('.jpg', combined)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpg.tobytes() + b'\r\n')

@app.route('/')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
