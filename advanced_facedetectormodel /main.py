import math
import time

import cv2
from ultralytics import YOLO

confidence = 0.6

cap = cv2.VideoCapture(0)  # For Webcam
cap.set(3, 640)
cap.set(4, 480)

model = YOLO('yolov5s.pt')

classNames = ["fake", "real"]  # Make sure this list is defined properly

prev_frame_time = 0
new_frame_time = 0

while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img)
    for r in results.pred:
        boxes = r[:, :4]
        confs = r[:, 4]
        cls_ids = r[:, 5].int()

        for box, conf, cls_id in zip(boxes, confs, cls_ids):
            # Bounding Box
            x1, y1, x2, y2 = box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            if conf > confidence:
                color = (0, 255, 0) if cls_id == 0 else (0, 0, 255)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f'{classNames[cls_id]} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
