from mistyPy.Robot import Robot
import cv2
import numpy as np
import time
from shape_detector import get_colors_shapes 
ip="172.26.232.220"

def begin_stream(rob, port=1935, width=640, height=480):
    rob.enable_av_streaming_service()
    rob.start_av_streaming(url=f"rtspd:{port}", width=width, height=height)
    cap = cv2.VideoCapture(f"rtsp://{ip}:{port}")
    return cap

def get_frame(cap):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return frame


#Colors are Pink, yellow, green, orange
def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    pink_lower = (145,60,50)
    pink_upper = (170,255,200)
    mask = cv2.inRange(frame, pink_lower, pink_upper)
    return mask
if __name__ == "__main__":
    rob = Robot(ip)
    cap = begin_stream(rob)
    get_colors_shapes(get_frame(cap))