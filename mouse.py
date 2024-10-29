import cv2
import mediapipe as mp
import pyautogui
import time
# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

color_palette1 = "Vibrant"

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize webcam
cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)

def close_camera():
    """Release the webcam and close all OpenCV windows."""
    cap1.release()
    cv2.destroyAllWindows()
# Helper function to check if a finger is extended
def is_finger_extended(landmarks, finger_tip, finger_dip):
    return landmarks.landmark[finger_tip].y < landmarks.landmark[finger_dip].y

# Gesture Detection Functions
def is_thumbs_up(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]

    # Check if the thumb is extended and pointing upwards
    return (thumb_tip.y < thumb_ip.y < thumb_mcp.y < thumb_cmc.y) and (thumb_tip.y < landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)

def is_thumbs_down(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]

    # Check if the thumb is pointing downwards
    return (thumb_tip.y > thumb_ip.y > thumb_mcp.y > thumb_cmc.y)

def is_peace_sign(landmarks):
    # Get the positions of the fingertips and knuckles
    index_tip_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_tip_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    thumb_tip_y = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    ring_tip_y = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip_y = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

    index_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y

    # Conditions for peace sign
    index_finger_condition = index_tip_y < index_knuckle_y
    middle_finger_condition = middle_tip_y < middle_knuckle_y
    thumb_condition = thumb_tip_y > middle_knuckle_y
    ring_condition = ring_tip_y > middle_knuckle_y
    pinky_condition = pinky_tip_y > middle_knuckle_y

    return index_finger_condition and middle_finger_condition and thumb_condition and ring_condition and pinky_condition

def is_open_hand(landmarks):
    # Check if all fingers are extended
    index_extended = is_finger_extended(landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_DIP)
    middle_extended = is_finger_extended(landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP)
    ring_extended = is_finger_extended(landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_DIP)
    pinky_extended = is_finger_extended(landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_DIP)

    # Thumb can be extended or not based on your requirement
    thumb_extended = is_finger_extended(landmarks, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP)

    return index_extended and middle_extended and ring_extended and pinky_extended and thumb_extended


def is_rock_on(landmarks):
    # Get the positions of the fingertips and knuckles
    index_tip_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_tip_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_tip_y = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip_y = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    thumb_tip_y = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

    index_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    #ring_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    #pinky_knuckle_y = landmarks.landmark[mp_hands.HandLandmark.PINKY_FINGER_PIP].y

    # Conditions for rock on gesture
    index_finger_condition = index_tip_y < index_knuckle_y
    pinky_finger_condition = pinky_tip_y < middle_knuckle_y
    middle_finger_condition = middle_tip_y > middle_knuckle_y
    ring_finger_condition = ring_tip_y > middle_knuckle_y
    thumb_condition = thumb_tip_y > middle_knuckle_y

    # Return true if index and pinky are extended, and middle and ring are bent
    return index_finger_condition and pinky_finger_condition and middle_finger_condition and ring_finger_condition and thumb_condition


# Main loop for webcam capture and gesture recognition
def center_logic():
    global color_palette1
    gesture_start_time = None
    detected_gesture = None
    while cap1.isOpened():
        ret, frame = cap1.read()
        if not ret:
            break

    # Mirror the image
        frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_hands = hands.process(rgb_frame)

    # If hand landmarks are detected
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                handedness = \
                results_hands.multi_handedness[results_hands.multi_hand_landmarks.index(hand_landmarks)].classification[
                    0].label
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw landmarks on frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger tip landmarks for controlling the mouse
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mid = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

            # If Left hand detected, control the mouse
                if handedness == "Left":
                    mcp_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
                    mcp_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y

                    cursor_x = int(mcp_x * screen_width)
                    cursor_y = int(mcp_y * screen_height)

                # Move the mouse to the calculated position
                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                # If index finger is touching the screen (index_tip.y >= index_mid.y), perform click
                    if index_tip.y >= index_mid.y:
                        pyautogui.click()

            # If Right hand detected, detect gestures

                '''if handedness == "Right":
                    detected_gesture = None
                    if is_thumbs_up(hand_landmarks):
                        #cv2.putText(frame, "Thumbs Up Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        detected_gesture = "Pastel"

                    elif is_thumbs_down(hand_landmarks):
                        #cv2.putText(frame, "Thumbs Down Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        detected_gesture = "Monochrome"

                    elif is_peace_sign(hand_landmarks):
                        #cv2.putText(frame, "Peace Sign Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                        detected_gesture = "Warm"

                    elif is_open_hand(hand_landmarks):
                        #cv2.putText(frame, "Open Hand Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
                        detected_gesture = "Cool"

                    elif is_rock_on(hand_landmarks):
                        #cv2.putText(frame, "Rock On Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
                        detected_gesture = "Bright"

                    # If a gesture is detected, record the time
                    if detected_gesture and gesture_start_time is None:
                        gesture_start_time = time.time()
                    elif detected_gesture and gesture_start_time is not None:
                    # Check if gesture has been held for at least 1 second
                        if time.time() - gesture_start_time >= 1:
                            color_palette1 = detected_gesture
                            break
                    else:
                        # Reset gesture state if no gesture is detected
                        gesture_start_time = None'''

    # Display the frame with landmarks and gesture detection
        cv2.imshow("Mouse pointer control", frame)

    # Break the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        #if color_palette1 != "Vibrant":  # Assuming "Vibrant" is the initial state
            #break

    close_camera()
    return color_palette1

# Release the webcam and close the window
center_logic()
#print(color_palette1)

