# Virtual Mouse Control Using Hand Gestures

A computer vision-based system that allows users to control their mouse cursor using hand gestures. This project uses MediaPipe for hand tracking and implements various mouse control gestures.

## 🛠️ Technologies Used

- **Python 3.x**
- **OpenCV** (cv2): For video capture and image processing
- **MediaPipe**: For hand landmark detection and tracking
- **PyAutoGUI**: For mouse control and system interactions
- **NumPy**: For numerical operations and calculations

## 🔧 Installation

1. Clone the repository: bash : 
git clone https://github.com/deepak-dobbala/Hand_Gesture_Recognition

2. Install required packages:bash :
pip install opencv-python mediapipe pyautogui numpy


## ✨ Features

### Mouse Control
- Real-time hand tracking
- Smooth cursor movement using palm center
- Exponential smoothing for stable cursor control
- Multiple gesture recognition

### Supported Gestures

1. **Cursor Movement**
   - Tracks palm center for precise cursor control
   - Continuous movement tracking
   - Smoothing algorithm for stability

2. **Left Click**
   - Trigger: Thumb tip touches index finger's middle joint
   - Visual feedback: Blue dots show contact points

3. **Right Click**
   - Trigger: Index fingertip touches middle fingertip
   - Visual feedback: Green dots show contact points

4. **Scrolling**
   - Requires: Three main fingers open (thumb, index, middle)
   - Scroll Up: Thumb-index pinch
   - Scroll Down: Index-middle pinch
   - Other fingers must be closed

5. **Zooming**
   - Trigger: Only thumb and pinky fingers extended
   - Zoom In: Increase distance between thumb and pinky
   - Zoom Out: Decrease distance between thumb and pinky
   - Visual feedback: Yellow line shows zoom distance

6. **Terminate Program**
   - Requires: Three main fingers open
   - Trigger: Thumb tip touches middle fingertip
   - Safely closes the application

## 🎯 Performance Features

- 60 FPS camera capture
- Optimized resolution (640x480)
- Real-time FPS display
- Single hand tracking for better performance
- Gesture priority system
- Smoothing algorithms for stable control

## 🚀 Usage

1. Run the main script:
bash:Readme.md
python src/main.py


2. Position your hand in front of the camera
3. Use the gestures described above to control your mouse
4. To exit, either:
   - Use the terminate gesture
   - Press 'q' on keyboard

## 📝 Notes

- Ensure good lighting conditions
- Keep hand within camera frame
- Maintain appropriate distance from camera
- Allow time to familiarize with gestures
- Adjust gesture thresholds if needed

## ⚙️ Configuration

Key parameters can be adjusted in the code:
- Gesture detection thresholds
- Smoothing factors
- Scroll sensitivity
- Zoom sensitivity
- Click delay timings

## 🤝 Contributing

Feel free to fork, submit PRs, or report issues. All contributions are welcome!

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.