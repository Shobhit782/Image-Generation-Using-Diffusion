from flask import Flask, render_template, request, jsonify
import torch
from diffusers import StableDiffusionPipeline
import speech_recognition as sr
import nltk
from nltk.tokenize import TreebankWordTokenizer
import subprocess

# Initialize Flask app
app = Flask(__name__)

# Load the AI model when the Flask app starts
model_id = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

# Initialize speech recognizer and tokenizer
recognizer = sr.Recognizer()
tokenizer = TreebankWordTokenizer()

# Download necessary NLTK data
nltk.download('punkt')

# Function to generate artwork based on the user's input

    
def generate_art(prompt, color, art_style):
    full_prompt = f"{prompt}, with {color} color palette in {art_style} style"
    generated_image = pipe(full_prompt).images[0]
    image_path = f'static\images\generated_img.png'
    generated_image.save(image_path)
    return image_path

# Route for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle artwork generation
@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    color = request.form.get('palette')
    art_style = request.form.get('art_type')

    artwork_url = generate_art(prompt, color, art_style)
    return jsonify({'artwork_url': artwork_url})

# Route to recognize speech from the user and return the text
@app.route('/detect-gesture', methods=['POST'])
def detect_gesture():
    try:
        # Run the gesture detection script and capture the result
        color_palette = subprocess.check_output(['python', 'main.py']).decode('utf-8').strip()

        # Return the detected color palette to the frontend
        return jsonify({'color_palette': color_palette})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-expression-detection', methods=['GET'])
def run_expression_detection():
    try:
        # Run the gesture detection script and capture the result
        detected_emotion = subprocess.check_output(['python', 'face_expression.py']).decode('utf-8').strip()

        # Return the detected color palette to the frontend
        return jsonify({'detected_emotion': detected_emotion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/run-mouse-detection', methods=['GET'])
def run_mouse_detection():
    # Run the 'mouse.py' script
    result = subprocess.run(['python', 'mouse.py'], capture_output=True, text=True)

    # You can return a success message or the output of the script
    return jsonify({'status': 'Mouse detection enabled'})
    
@app.route('/recognize_speech', methods=['GET'])
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for speech...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"Original speech: {text}")

        # Refine the text using NLP
        refined_text = refine_speech_text(text)
        print(f"Refined text: {refined_text}")

        # Return the refined text as JSON
        return jsonify({"recognized_text": refined_text})
    
    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, I could not understand the audio."}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results; {e}"}), 500

def refine_speech_text(text):
    tokens = tokenizer.tokenize(text)
    refined_text = ' '.join(tokens)
    return refined_text

if __name__ == '__main__':
    app.run(debug=True)
