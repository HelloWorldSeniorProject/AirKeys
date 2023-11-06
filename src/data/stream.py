import cv2
import mediapipe as mp
from time import time

# mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# constants
cap_buffer_size = 2
cam_width = 640
cam_height = 480

# fps tracking
old_frame_t = 0
new_frame_t = 0


def main(left, right, hands, old_frame_t, new_frame_t):
    while True:
        _, lf = left.read()
        _, rf = right.read()

        # Remove mediapipe processing by commenting from here ---->

        # recolor frame; required for mediapipe proc.
        lf = cv2.cvtColor(cv2.flip(lf, 1), cv2.COLOR_BGR2RGB)
        rf = cv2.cvtColor(cv2.flip(rf, 1), cv2.COLOR_BGR2RGB)

        # detect hands
        l_res = hands.process(lf)
        r_res = hands.process(rf)

        # return to og color to handle display
        lf = cv2.cvtColor(lf, cv2.COLOR_RGB2BGR)
        rf = cv2.cvtColor(rf, cv2.COLOR_RGB2BGR)

        # add outline to hand
        if l_res.multi_hand_landmarks and r_res.multi_hand_landmarks:
            for hand_landmarks in l_res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(lf, hand_landmarks, mphands.HAND_CONNECTIONS)
            for hand_landmarks in r_res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(rf, hand_landmarks, mphands.HAND_CONNECTIONS)

        # to here ------>

        # FPS tracking
        new_frame_t = time()
        fps = str(int(1 / (new_frame_t - old_frame_t)))
        old_frame_t = new_frame_t

        # uncomment for cli testing.
        # print(f"FPS: {fps}")

        # add fps counter to left frame.
        cv2.putText(lf, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (100, 255, 0), 2, cv2.LINE_AA)

        # show frames in separate windows. Purely for setup and debugging. We won't need to show any of
        # images we capture during actual runtime.
        cv2.imshow("left", lf)
        cv2.imshow("right", rf)

        # press q to exit.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def setup():
    def set_video_cap_attrs(cap):
        # only keep two frames in buffer. Supposedly improves speed.
        cap.set(cv2.CAP_PROP_BUFFERSIZE, cap_buffer_size)

        # set capture resolution (low-res).
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)

    # opencv setup
    left = cv2.VideoCapture(0)
    right = cv2.VideoCapture(1)
    set_video_cap_attrs(left)
    set_video_cap_attrs(right)

    # more mediapipe setup
    hands = mphands.Hands()

    # verify attributes as expected.
    def test_video_cap_attrs(cap):
        res = (
            int(cap.get(cv2.CAP_PROP_BUFFERSIZE)) == cap_buffer_size
            and int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) == cam_width
            and int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) == cam_height
        )
        return res

    assert (test_video_cap_attrs(left) and test_video_cap_attrs(right)) == True

    return left, right, hands


def teardown(left, right):
    left.release()
    right.release()

    cv2.destroyAllWindows()


def run():
    left, right, hands = setup()

    main(left, right, hands, old_frame_t, new_frame_t)

    teardown(left, right)


if __name__ == "__main__":
    run()
