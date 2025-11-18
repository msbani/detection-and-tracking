# Detection and Tracking

This project demonstrates a simple and efficient method to **detect and track a soccer ball in a video** using classic computer vision techniques color filtering, Hough Circle Transform, and OpenCV’s MOSSE tracker.
![{643A1C2B-589A-46B5-852F-D0844101C795}](https://github.com/msbani/detection-and-tracking/blob/main/output-tracking.gif)



## Overview
This implementation uses a combination of **color-based circle detection and object tracking** for smooth and real time ball tracking in video frames.
- **Detection:** The ball is detected using HSV color masking and Hough Circle Transform.
- **Tracking:** Once detected, OpenCV’s lightweight **MOSSE tracker** follows the ball in subsequent     frames for faster processing.
- **Re-detection:** Every few frames (or when tracking fails), the system redetects the ball to maintain robustness.

## Key Features
- Lightweight and efficient — suitable for real time tracking.
  ```bash
  tracker = cv2.legacy.TrackerMOSSE_create()
  ```
- Automatic re-detection if tracking fails.
  ```bash
  if not tracking or frame_count % 30 == 0:
  ```
- Bounding box visualization:
  - Blue — during detection
  ```bash
  cv2.rectangle(frame, (x - r, y - r), (x + r, y + r), (255, 0, 0), 2)
  ```
  - Green — during tracking
  ```bash
  cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
  ```
  - Red — when tracking is lost
  ```bash
  cv2.putText(frame, "Tracking Lost", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
  ```
- Saves the processed output video as `output-tracking.mp4`.
  ```bash
  out.write(frame)
  ```
## Requirements
Ensure the following dependencies are installed:

- Python 3.x
- OpenCV

To install the required libraries:
```bash
pip install opencv-python opencv-contrib-python
```

## How It Works
1. **Video Input**: The script reads the video file (`soccer-ball.mp4`).
2. **Initial Detection**:
   - Converts each frame to HSV color space.
  - Applies a color mask to isolate the ball.
  - Uses the **Hough Circle Transform** to detect circular shapes representing the ball.
3. **Tracker Initialization**: A **MOSSE tracker** is initialized with the detected bounding box.
4. **Frame Processing**:
   - The tracker predicts the ball’s location frame by frame.
   - Every 30 frames (or if tracking fails), re-detection is performed for correction.
5. **Visualization & Output**: 
  - Bounding boxes and status text are drawn on each frame.
  - The processed video is written to `output-tracking.mp4`.

## Usage
Run the script with:
```bash
python ball_tracking.py
```

### Input Video
- Place `soccer-ball.mp4` in the same directory as the script.
- You can change the input file by modifying:
```bash
cap = cv2.VideoCapture("your_video.mp4")
```
### Output
- The resulting video will be saved as:
```bash
output-tracking.mp4
```
- A real-time preview window shows tracking progress. Press **Esc** to exit.

## Customization
- **Color Range:** Adjust HSV lower and upper bounds in the line:
```bash
mask = cv2.inRange(hsv, (0, 0, 110), (180, 40, 255))
```
to suit different ball colors or lighting conditions.
- **Tracker Type:** You can replace `TrackerMOSSE_create()` with other OpenCV trackers such as `TrackerCSRT_create()` or `TrackerKCF_create()` for different performance.

## Limitations
- Accuracy may drop under low lighting or when the ball color blends with the background.
- Hough circle detection may detect false positives if objects have similar shapes.
- The script is optimized for relatively simple scenes with a clear view of the ball.

