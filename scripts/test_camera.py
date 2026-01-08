#!/usr/bin/env python3
"""Quick test - counts frames for 5 seconds"""
import depthai as dai
import time

with dai.Pipeline() as pipeline:
    cam = pipeline.create(dai.node.Camera).build()
    q = cam.requestOutput((640, 400)).createOutputQueue()
    
    pipeline.start()
    print('Recording 5 seconds...')
    start = time.time()
    frames = 0
    while time.time() - start < 5:
        frame = q.get()
        frames += 1
    print(f'Got {frames} frames in 5 seconds (~{frames//5} FPS)')
