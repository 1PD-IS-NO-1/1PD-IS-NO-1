import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def get_frame(self, as_numpy=False):
        success, frame = self.camera.read()
        if not success:
            return None
        if as_numpy:
            return frame
        ret, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()
