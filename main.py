import cv2
import numpy as np

# Open video
cap = cv2.VideoCapture("soccer-ball.mp4")

# Tracker
tracker = cv2.TrackerCSRT_create()
tracking = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if not tracking:
        # ----- Ball Detection (using HoughCircles) -----
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                                   param1=100, param2=30,
                                   minRadius=10, maxRadius=80)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0]  # first circle
            bbox = (x - r, y - r, 2 * r, 2 * r)

            # Initialize tracker with detection
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, bbox)
            tracking = True

            # Draw detection box (BLUE)
            cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (255, 0, 0), 2)
            cv2.putText(frame, "Detection", (x - r, y - r - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    else:
        # ----- Tracking -----
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, " ", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            tracking = False
            cv2.putText(frame, "Tracking Lost", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Detection + Tracking", frame)
    if cv2.waitKey(30) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
