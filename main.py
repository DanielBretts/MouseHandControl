import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
# Global variables to check the positions with the other fingers
thumb_y = 0
index_y = 0


def position_on_screen(x, y):
    global screen_width, screen_height
    frame_on_screen = [screen_width / frame_width, screen_height / frame_height]
    return [int(frame_on_screen[0] * x), int(frame_on_screen[1] * y)]


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # flip the frame
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 20:
                    pinky_x, pinky_y = position_on_screen(x, y)
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    if abs(thumb_y - pinky_y) < 30:
                        pyautogui.rightClick()
                        pyautogui.sleep(1)  # wait 1 sec for the click
                        print('right')
                if id == 8:  # check position of index
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x, index_y = position_on_screen(x, y)

                    pyautogui.moveTo(index_x, index_y)
                if id == 4:  # check position of thumb
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x, thumb_y = position_on_screen(x, y)
                    if abs(index_y - thumb_y) < 40:
                        print('left')
                        pyautogui.click()
                        pyautogui.sleep(1)  # wait 1 sec for the click

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
