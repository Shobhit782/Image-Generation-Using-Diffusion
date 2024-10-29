# AI-Driven Art Generation with Gesture, Voice, and Facial Expression Control

This project is a Flask web application that generates artwork using Stable Diffusion based on user inputs through text, voice, and hand gestures. The system leverages gesture detection using MediaPipe, speech recognition via Google Web Speech API, and the Stable Diffusion model for generating artwork based on custom prompts, color palettes, and art styles.
## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Project Structure](#Project-Structure)
- [Routes](#routes)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)

## Features

- **Art Generation**: Generates art based on text prompts and various artistic styles and color palettes using Stable Diffusion.
- **Voice Recognition**: Converts voice input into text prompts.
- **Gesture Detection**: Detects specific hand gestures to set color palette preferences.
- **Flexible Interaction**: Users can control inputs through text, voice, and hand gestures, enhancing accessibility and user experience.

## Installation

### Prerequisites

- Python 3.8+
- [CUDA](https://developer.nvidia.com/cuda-toolkit) compatible GPU (recommended for optimal performance)
- [Pip](https://pip.pypa.io/en/stable/installation/)

### Step-by-Step Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
2.**Install Dependencies**:

pip install -r requirements.txt

3. **Run the Application**:
Run the app.py file

Open your browser and navigate to http://127.0.0.1:5000.

Enter text prompts, select options, or use voice input for generating artwork.

Initiate gesture detection to control the color palette through specific hand gestures.

## Project-Structure
project-root/
│
├── app.py                 # Main Flask application file
├── templates/
│   └── index.html         # HTML template for the front end
├── static/
│   └── images/            # Folder to store generated images
├── requirements.txt       # List of project dependencies
└── README.md              # Project documentation

## Routes
Main page to input prompts and control settings.
/generate (POST): Generates artwork based on text prompts and selected options.
/recognize_speech (GET): Captures and processes speech input.
/start_gesture_detection (POST): Starts gesture detection, enabling color palette selection through hand gestures.

## Technologies Used
Flask: Web framework for Python
Stable Diffusion: AI model for generating artwork
SpeechRecognition: Library for speech-to-text conversion
MediaPipe: For hand gesture detection and recognition
NLTK: Natural Language Toolkit for tokenizing and refining text

## Future Enhancements
WebSocket Integration: Real-time feedback from gesture detection to the front end.
Additional Gestures: Add more hand gestures for extended functionality.
