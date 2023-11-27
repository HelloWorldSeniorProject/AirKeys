import cv2
import keyboard
import mediapipe as mp
import numpy as np
from vector import Vector

def detect(images, points, isLeft: bool):
    """
    Detects fingertips from the given image matrices.

    Args:
        images : list of numpy matrices representing undistorted images from recording process.
        points : list of points of fingertips detected from given images
        isLeft : boolean representing if the image is from the left camera.
    """
    
    """Prepare for main process"""
    labels = {
        4: "thumb",
        8: "index",
        12: "middle",
        16: "ring",
        20: "pinky"
    }
    hand = "left_" if isLeft else "right_"

    """Initialize mediapipe solution for hand pose detection"""
    hands = mp.solutions.hands.Hands()

    """Main loop"""
    while True:
        if len(images) > 1:
            """Modification for Mediapipe implementation"""
            mat = np.copy(images[0]) if isLeft else np.copy(images[1])
            img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

            """Mediapipe implementation"""
            results = hands.process(img)
            frame = dict()
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for idx, lm in enumerate(handLms.landmark):
                        if idx in [4, 8, 12, 16, 20]:
                            frame[hand + labels[idx]] = Vector(lm.x, lm.y, lm.z)
            
            """Timestamp (to be implemented)"""
            # frame["timestamp"] =

            points.append(frame)

        """Shutting down"""
        if keyboard.is_pressed('escape'):
            break
