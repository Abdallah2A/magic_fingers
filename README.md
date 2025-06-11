# 🖐️ Magic Fingers

<p align="center">
  <img src="assets/logo.png" alt="Hand Gesture Control Logo" width="180" align="right">
</p>

**Magic Fingers** is a real-time, camera-based system that uses MediaPipe for hand tracking and PyAutoGUI for desktop control via natural gestures.

---

## 🚀 Features

- 🎥 Real-time hand tracking with **MediaPipe**  
- 🖱️ Cursor movement via index finger  
- 👆 Touch gesture for left-click  
- 🤏 Pinch for click  
- 🖐️ Fist to minimize all windows  
- 📌 Open window switcher with pinky finger  
- 🔄 Smooth scrolling with two-finger swipe  

---

## 📁 Project Structure

```
magic_fingers/
├── assets/
│   └── logo.png      # Project logo image
├── main.py           # Main application script
├── requirements.txt          # Python package dependencies
└── README.md                 # This file
```

---

## 🔧 Installation

Install dependencies:

```bash
pip install opencv-python mediapipe pyautogui pygetwindow numpy
```

---

## ⚙️ Usage

Start the application:

```bash
python main.py
```

Controls:

- Point with your **index finger** to move the cursor  
- **Pinch** (index + thumb) to click  
- **Swipe** two fingers for scrolling  
- Form a **fist** to minimize all windows  
- Raise your **pinky** to open the window switcher  

Exit by pressing `q` in the video window.

---

## 📜 License

This project is licensed under the MIT License.

---

Enjoy desktop control with natural hand gestures! 🖐️
