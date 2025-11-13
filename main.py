import cv2
import numpy as np

# ---- Video ----
cap = cv2.VideoCapture("soccer-ball.mp4")

# Get input video details
fps = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# ---- Save output video ----
fourcc = cv2.VideoWriter_fourcc()  # Codec
out = cv2.VideoWriter("output-tracking.mp4", fourcc, fps, (width, height))

# ---- Tracker ----
tracker = cv2.legacy.TrackerMOSSE_create()
tracking = False
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    if not tracking or frame_count % 30 == 0:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 0, 110), (180, 40, 255))
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(gray, 50, 150)

        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
                                   param1=100, param2=25,
                                   minRadius=8, maxRadius=80)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0]
            bbox = (x - r, y - r, 2 * r, 2 * r)

            tracker = cv2.legacy.TrackerMOSSE_create()
            tracker.init(frame, bbox)
            tracking = True

            cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (255, 0, 0), 2)
            cv2.putText(frame, "Detection", (x - r, y - r - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        else:
            cv2.putText(frame, "Detecting...", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    else:
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            tracking = False
            cv2.putText(frame, "Tracking Lost", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # --- Save current frame to output video ---
    out.write(frame)

    cv2.imshow("Ball Detection + Tracking", frame)
    if cv2.waitKey(20) & 0xFF == 27:
        break

cap.release()
out.release()  # very important
cv2.destroyAllWindows()
print("✅ Output video saved as 'output-tracking.mp4'")
