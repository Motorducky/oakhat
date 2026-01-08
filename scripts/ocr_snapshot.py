#!/usr/bin/env python3
"""Take snapshots and perform OCR"""
import depthai as dai
import cv2
import os
from datetime import datetime

try:
    import pytesseract
    from PIL import Image
except ImportError:
    print("Install: pip install pytesseract pillow --break-system-packages")
    print("Also: sudo apt install tesseract-ocr")
    exit(1)

os.makedirs(os.path.expanduser('~/snapshots'), exist_ok=True)

print('OCR Snapshot Tool')
print('[Enter] - snapshot + OCR | q - quit')

with dai.Pipeline() as pipeline:
    cam = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_A)
    q = cam.requestOutput((1920, 1080)).createOutputQueue()
    
    pipeline.start()
    for _ in range(10):
        q.get()
    
    while True:
        cmd = input('\n> ')
        if cmd.lower() == 'q':
            break
        
        frame = cv2.rotate(q.get().getCvFrame(), cv2.ROTATE_180)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        img_path = os.path.expanduser(f'~/snapshots/{timestamp}.jpg')
        cv2.imwrite(img_path, frame)
        print(f'Saved: {img_path}')
        
        print('Running OCR...')
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(Image.fromarray(rgb))
        
        if text.strip():
            print('--- OCR Result ---')
            print(text)
            print('------------------')
            with open(os.path.expanduser(f'~/snapshots/{timestamp}.txt'), 'w') as f:
                f.write(text)
        else:
            print('No text detected')
