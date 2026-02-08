from vision.hand_tracker import HandTracker
from gestures.finger_state import FingerStateDetector
from gestures.gesture_rules import GestureRuleEngine
from control.mouse_windows import WindowsMouseController

def main():
    tracker = HandTracker(enable_visualization=True)
    finger_detector = FingerStateDetector()
    gesture_engine = GestureRuleEngine()
    mouse = WindowsMouseController()

    try:
        while True:
            data = tracker.process_frame()
            if not data["detected"]:
                continue

            landmarks = data["landmarks"]
            states = finger_detector.get_finger_states(landmarks)
            gesture = gesture_engine.classify_gesture(landmarks,states)

            # Index finger tip controls curosr
            index_tip = landmarks[8]
            mouse.move_cursor(index_tip[0],index_tip[1])

            if gesture=="CLICK":
                mouse.left_click()
            elif gesture=="DRAG_START":
                mouse.start_drag()
            elif gesture=="DRAG_END":
                mouse.end_drag()

                
               
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        tracker.release()


if __name__ == "__main__":
    main()
