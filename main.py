from vision.hand_tracker import HandTracker

def main():
    tracker = HandTracker(enable_visualization=True)

    try:
        while True:
            data = tracker.process_frame()
            if data["detected"]:
                print("Right hand detected | First landmark:", data["landmarks"][0])
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        tracker.release()


if __name__ == "__main__":
    main()
