import cv2
import pyautogui
import mediapipe as mp
import pygetwindow as gw

SMOOTHING = 2


def init_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera {camera_id}")
    return cap


def init_hand_tracker():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils
    return hands, mp_hands, mp_draw


def get_hand_landmarks(frame, hands):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        return results.multi_hand_landmarks[0]
    return None


def map_and_smooth_coordinates(lm_x, lm_y, screen_width, screen_height, prev_x, prev_y, smoothing=SMOOTHING):
    left = 0.2
    right = 0.8
    top = 0.2
    bottom = 0.8

    effective_x = max(left, min(right, lm_x))
    effective_y = max(top, min(bottom, lm_y))

    mapped_x = (effective_x - left) / (right - left) * screen_width
    mapped_y = (effective_y - top) / (bottom - top) * screen_height

    curr_x = prev_x + (mapped_x - prev_x) / smoothing
    curr_y = prev_y + (mapped_y - prev_y) / smoothing

    curr_x = max(0, min(screen_width - 1, curr_x))
    curr_y = max(0, min(screen_height - 1, curr_y))

    return curr_x, curr_y


def move_mouse_to(curr_x, curr_y):
    try:
        pyautogui.moveTo(int(curr_x), int(curr_y))
    except Exception:
        pass


def is_click_gesture(landmarks, threshold=0.05):
    lm_index = landmarks.landmark[8]
    lm_thumb = landmarks.landmark[4]

    distance = abs(lm_index.x - lm_thumb.x)
    temp = abs(landmarks.landmark[17].x - landmarks.landmark[5].x)

    return (distance < threshold) and (temp > 0.15)


def fingers_up(hand_landmarks):
    tips = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
    dips = {"thumb": 3, "index": 7, "middle": 11, "ring": 15, "pinky": 19}
    states = {}
    for name in tips:
        tip_y = hand_landmarks.landmark[tips[name]].y
        dip_y = hand_landmarks.landmark[dips[name]].y
        states[name] = tip_y < dip_y
    return states


def scroll_down(x):
    pyautogui.scroll(int(-5000 * x))


def scroll_up(x):
    pyautogui.scroll(int(5000 * x))


def minimize_all_windows():
    for w in gw.getAllWindows():
        if w.visible and not w.isMinimized:
            w.minimize()


def get_all_windows():
    pyautogui.keyDown('winleft')
    pyautogui.press('tab')
    pyautogui.keyUp('winleft')


def main():
    cap = init_camera()
    hands, mp_hands, mp_draw = init_hand_tracker()
    screen_width, screen_height = pyautogui.size()
    prev_x, prev_y = 0, 0
    was_clicking = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape

        hand_landmarks = get_hand_landmarks(frame, hands)
        if hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_states = fingers_up(hand_landmarks)

            if (finger_states['index'] and finger_states['middle'] and not finger_states['ring']
                    and not finger_states['pinky']):
                index_bottom = hand_landmarks.landmark[5]
                index_top = hand_landmarks.landmark[8]
                diff = index_bottom.x - index_top.x
                if abs(diff) > 0.05 and diff > 0:
                    scroll_down(abs(diff))

            elif (finger_states['index'] and finger_states['middle'] and finger_states['ring']
                  and not finger_states['pinky']):
                index_bottom = hand_landmarks.landmark[5]
                index_top = hand_landmarks.landmark[8]
                diff = index_bottom.x - index_top.x
                if abs(diff) > 0.05 and diff > 0:
                    scroll_up(abs(diff))

            if (finger_states['index'] and not finger_states['middle'] and not finger_states['ring']
                    and not finger_states['pinky']):
                lm_index = hand_landmarks.landmark[8]
                curr_x, curr_y = map_and_smooth_coordinates(lm_index.x, lm_index.y, screen_width, screen_height, prev_x,
                                                            prev_y)
                move_mouse_to(curr_x, curr_y)
                prev_x, prev_y = curr_x, curr_y

                if is_click_gesture(hand_landmarks):
                    if not was_clicking:
                        try:
                            pyautogui.click()
                        except Exception:
                            pass
                    was_clicking = True
                else:
                    was_clicking = False

            if (not finger_states['index'] and not finger_states['middle'] and not finger_states['ring']
                    and not finger_states['pinky']):
                minimize_all_windows()

            if (not finger_states['index'] and not finger_states['middle'] and not finger_states['ring']
                    and finger_states['pinky']):
                get_all_windows()

        cv2.imshow('Live Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
