import numpy as np
import cv2
import yaml

def calibrate():
    """
    Calibrates both cameras for further processes if necessary.

    Returns:
        mtx: Camera matrix for restoration
        dist: Distortion coefficient for restoration
    """
    
    """Camera initialization"""
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    cap = cv2.VideoCapture(0)

    """Prepare calibration"""
    obj_pos = np.zeros((6 * 7, 3), np.float32)
    obj_pos[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    obj_pts = []
    img_pts = []

    """
    Begin calibration

    This while loop continues until n = 10 images with a chessboard are detected.
    """
    found = 0
    while (found < 10):
        """Read image"""
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        """Detect chessboard for calibration"""
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
        if ret == True:
            obj_pts.append(obj_pos)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            img_pts.append(corners2)

            img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
            found += 1

        """Display image"""
        cv2.imshow('CALIBRATE', img)
        cv2.waitKey(1)

    """
    End calibration
    
    As calibration is finished, terminates camera and window
    and calculates mtx and dist
    """
    cap.release()
    cv2.destroyAllWindows()
    ret, mtx, dist, _, _ = cv2.calibrateCamera(obj_pts, img_pts, gray.shape[::-1], None, None)

    """Save calibration result"""
    data = {
        'camera_matrix': np.asarray(mtx).tolist(),
        'dist_coeff': np.asarray(dist).tolist()
    }
    with open('calibration.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

    """Return calibration result"""
    return mtx, dist
