from vision.hand_tracker import HandTracker
from gestures.finger_state import FingerStateDetector
from gestures.gesture_rules import GestureRuleEngine
from control.mouse_windows import WindowsMouseController
from gestures.gesture_buffer import GestureBuffer

def main():
    tracker = HandTracker(enable_visualization=True, detection_confidence=0.8, tracking_confidence=0.8)
    finger_detector = FingerStateDetector()
    gesture_engine = GestureRuleEngine()
    mouse = WindowsMouseController()
    gesture_buffer = GestureBuffer(buffer_size=5)

    try:
        while True:
            data = tracker.process_frame()
            if not data["detected"]:
                continue

            landmarks = data["landmarks"]
            states = finger_detector.get_finger_states(landmarks)
            raw_gesture = gesture_engine.classify_gesture(landmarks,states)
            gesture = gesture_buffer.update(raw_gesture)

            # Advanced cursor tracking: support pointing AND dragging smoothly
            if states["index"]==1:
                # Use index tip for precise pointing
                track_point = landmarks[8]
                mouse.move_cursor(track_point[0],track_point[1])
            elif gesture in ["DRAG_START", "DRAGGING"]:
                # Use index knuckle (MCP) for tracking while the fist is closed
                track_point = landmarks[5]
                mouse.move_cursor(track_point[0],track_point[1])

            if gesture=="CLICK":
                mouse.left_click()
            elif gesture=="DRAG_START":
                mouse.start_drag()
            elif gesture=="DRAG_END":
                mouse.end_drag()
            elif gesture=="PLAY_PAUSE":
                mouse.media_play_pause()
            elif gesture=="VOLUME_UP":
                mouse.volume_up()
            elif gesture=="VOLUME_DOWN":
                mouse.volume_down()

                
               
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        tracker.release()


if __name__ == "__main__":
    main()
