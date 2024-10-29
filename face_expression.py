import cv2
from deepface import DeepFace
import time
#from mouse_pointer_control import close_camera, center_logic
#from hand_gesture_detection import center_logic_gesture
detected_emotion = "No Emotion Detected"

def detect_emotion(frame):
    # Analyze the frame for emotions using DeepFace
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

    # Initialize an empty string for the detected emotion
    global detected_emotion  # Access the global variable

    # Check for dominant emotions
    for res in result:
        dominant_emotion = res['dominant_emotion']
        if dominant_emotion == 'happy':
            detected_emotion = "Pop Art"
        elif dominant_emotion == 'sad':
            detected_emotion = "Digital"
        elif dominant_emotion == 'surprised':
            detected_emotion = "Minimalism"
        else:
            detected_emotion = "No Emotion Detected"  # Default case
        return detected_emotion  # Return the detected emotion immediately

def main():
    #close_camera()
    global detected_emotion
    # Initialize webcam
    cap2 = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    while True:
        ret, frame = cap2.read()
        if not ret:
            break

        # Flip the frame for a mirror effect
        frame = cv2.flip(frame, 1)

        # Detect emotion
        emotion_text = detect_emotion(frame)

        # Put the detected emotion text on the frame
        cv2.putText(frame, emotion_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Emotion Detection', frame)

        # Break the loop if 'q' is pressed or an emotion is detected
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if emotion_text != "No Emotion Detected":  # If an emotion is detected
            time.sleep(1)  # Display for 1 second
            break  # Exit the loop

    # Release the webcam and close the window
    cap2.release()
    cv2.destroyAllWindows()

    return detected_emotion

if __name__ == "__main__":
#center_logic()
    main()
    print(detected_emotion)
