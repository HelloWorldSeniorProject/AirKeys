import cv2
from typing import List

class DataStream:
    def __init__(self):
        """Initializes the data stream with camera settings."""
        self.CAP_BUFFER_SIZE = 2  # Integer
        self.CAMERA_WIDTH = 640    # Integer
        self.CAMERA_HEIGHT = 480   # Integer

    def setup_cameras(self, num_cameras: int) -> List[cv2.VideoCapture]:
        """
        Initializes the specified number of cameras and returns their captures.

        Args:
            num_cameras: The number of cameras to initialize.

        Returns:
            A list of initialized camera capture objects.
        """
        cameras = []
        for i in range(num_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_BUFFERSIZE, self.CAP_BUFFER_SIZE)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
                cameras.append(cap)
            else:
                print(f"Failed to set up camera {i}")
        return cameras

    def get_frame_data(self, captures: List[cv2.VideoCapture]) -> List[List[List[int]]]:
        """
        Retrieves frames from each camera capture object in a list.

        Args:
            captures: A list of cv2.VideoCapture objects.

        Returns:
            A list of frame data from each camera, with each frame being a list of lists of integers.
        """
        frames = []
        for cap in captures:
            ret, frame = cap.read()
            if ret:
                frames.append(frame.tolist())  # Convert to list of lists for JSON serialization
        return frames

    def display_frame(self, frame: List[List[int]]):
        """
        Displays a single frame.

        Args:
            frame: A list of lists of integers representing the frame to display.
        """
        # Assumes frame is a list of lists, converts to a numpy array to display
        frame_array = np.array(frame, dtype=np.uint8)
        cv2.imshow('Frame', frame_array)
        cv2.waitKey(1)  # You might need to adjust this for proper display timing

    def create_video_writer(self, save_path: str) -> cv2.VideoWriter:
        """
        Creates a video writer object to save video to a file.

        Args:
            save_path: The path to save the video file.

        Returns:
            A cv2.VideoWriter object.
        """
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(save_path, fourcc, 20.0, (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
        return out

    def save_frame_to_video(self, frame: List[List[int]], out: cv2.VideoWriter):
        """
        Writes a frame to the video file.

        Args:
            frame: A list of lists of integers representing the frame to write to the video.
            out: The cv2.VideoWriter object to write the frame to.
        """
        # Assumes frame is a list of lists, converts to a numpy array to write to video
        frame_array = np.array(frame, dtype=np.uint8)
        out.write(frame_array)

    def save_video(self, out: cv2.VideoWriter):
        """
        Finalizes the video file saving process.

        Args:
            out: The cv2.VideoWriter object to finalize.
        """
        out.release()

    def teardown_cameras(self, captures: List[cv2.VideoCapture]):
        """
        Releases all initialized camera captures and destroys all OpenCV windows.

        Args:
            captures: A list of cv2.VideoCapture objects to release.
        """
        for cap in captures:
            cap.release()
        cv2.destroyAllWindows()
