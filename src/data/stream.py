import cv2
import mediapipe as mp
from time import time

class InputStream:
    def __init__(self):
        # Initialize camera constants
        self.CAP_BUFFER_SIZE = 2
        self.CAMERA_WIDTH = 640
        self.CAMERA_HEIGHT = 480
        
        #Initialize MediaPipe tools 
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        
        #Tracking for FPS calculation
        self.old_frame_time = 0

    def setVideoCaptureAttributes(self, cap):
        # Returns True if camera attributes are successful
        try:
            # Sets buffer size and resolution for the camera capture.
            # Reduces buffer size to 2 which reduces latency and improves  
            # capture speed due to frames being processed more immediately.
            cap.set(cv2.CAP_PROP_BUFFERSIZE, self.CAP_BUFFER_SIZE)
            
            # Sets capture resolution to low-res.
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
            
            return True
        except:
            return False

    def setupCameras(self, numCameras):
        # Initializes a specified number of cameras(usually 2) along with 
        # there attributes and returns a list of VideoCapture objects.
        cameras = []
        for i in range(numCameras):
            cap = cv2.VideoCapture(i)
            if self.setVideoCaptureAttributes(cap):
                cameras.append(cap)
            else:
                print(f"Failed to set up camera {i}")
        return cameras

    def process_frame(self, frame):
        # Process a single frame for hand tracking, including recoloring and landmark drawing.
        # Recolors frame because MediaPipe requires RGB format.
        frame_rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        # Detects hand landmarks with MediaPipe. 
        results = self.hands.process(frame_rgb)
        # Converts back to BGR for OpenCV.
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        # Draws hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame_bgr, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
        return frame_bgr  
      
    def getFrameData(self, captures):
        # Retrieves each captured frame from each camera 
        # and returns a list of frame data.
        frames = []
        for cap in captures:
            ret, frame = cap.read()
            if ret:
                processed_frame = self.process_frame(frame)
                frames.append(processed_frame.tolist())  
        return frames

    
    def calculate_fps(self):
        # Calculate and return the current frames per second.
        new_frame_time = time()
        fps = int(1 / (new_frame_time - self.old_frame_time))
        self.old_frame_time = new_frame_time
        return str(fps)

    def teardownCameras(self, captures):
        # Releases initialized cameras and destroys OpenCV windows.
        for cap in captures:
            cap.release()
        cv2.destroyAllWindows()

    def run(self):
        cameras = self.setupCameras(2)  # Assumes 2 cameras
        try:
            while True:
                frames = self.getFrameData(cameras)
                # Goes over each frame.
                for idx, frame in enumerate(frames):
                    fps = self.calculate_fps()
                    
                    # Adjusts parameters and puts fps over the image.
                    cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 255, 0), 2, cv2.LINE_AA)
                    # Displays the frame
                    cv2.imshow(f"Camera {idx}", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.teardownCameras(cameras)

if __name__ == "__main__":
    input_stream = InputStream()
    input_stream.run()
