import cv2
import keyboard

def record(mtx, dist, images):
    """
    Records the undistorted images as numpy matrices for Detect process.

    Args:
        mtx: Camera matrix gathered from Calibration process
        dist: Distortion coefficients from Calibration process
        images: list of numpy matrices to store images
    """

    # Cameras initialization
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)

    # Main loop
    while True:
        # Record images
        _, img1 = cap1.read()
        _, img2 = cap2.read()

        # Restore images
        mat1 = cv2.undistort(img1, mtx, dist)
        mat2 = cv2.undistort(img2, mtx, dist)

        # Store images for Detect process
        images.append(mat1)
        if len(images) > 2:
            images.pop(0)

        images.append(mat2)
        if len(images) > 2:
            images.pop(0)

        # Shutting down
        if keyboard.is_pressed('escape'):
            break

    # Termination
    cap1.release()
    cap2.release()
