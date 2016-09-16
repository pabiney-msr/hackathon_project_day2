import cv2
import numpy as np

def nothing(x):
    pass

def trackbar(name,image):
    # get current positions of trackbars
    h_low = cv2.getTrackbarPos('H_low',name)
    s_low = cv2.getTrackbarPos('S_low',name)
    v_low = cv2.getTrackbarPos('V_low',name)

    # get current positions of trackbars
    h_hi = cv2.getTrackbarPos('H_high',name)
    s_hi = cv2.getTrackbarPos('S_high',name)
    v_hi = cv2.getTrackbarPos('V_high',name)

    return [h_low, s_low, v_low, h_hi, s_hi, v_hi]

if __name__ == "__main__":
    trackbar(name,image)
