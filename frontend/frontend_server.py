"""
VQA Web Frontend Server
=======================
A simple Flask server that serves the VQA web interface and handles API requests.

This server integrates the beautiful gradient frontend with the BLIP VQA backend.

Usage:
    python frontend_server.py
    
Then open http://localhost:5000 in your browser.
"""

import os
import sys
import base64
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import VQA module
try:
    from scripts.vqa_blip import VQABlip
    vqa_model = None  # Lazy load
except ImportError:
    vqa_model = None
    print("Warning: Could not import VQA module. Make sure you're in the project directory.")

app = Flask(__name__, static_folder='static')
CORS(app)

# Global model instance
_model = None

def get_model():
    """Get or create the VQA model instance."""
    global _model
    if _model is None:
        print("Loading BLIP VQA model...")
        _model = VQABlip()
        print("Model loaded!")
    return _model


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')


@app.route('/api/vqa', methods=['POST'])
def process_vqa():
    """Process a VQA request."""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data or 'question' not in data:
            return jsonify({'error': 'Image and question are required'}), 400
        
        image_data = data['image']
        question = data['question']
        
        # Handle base64 image data
        if image_data.startswith('data:image'):
            # Extract the base64 part after the comma
            image_data = image_data.split(',')[1]
        
        # Decode base64 to image
        image_bytes = base64.b64decode(image_data)
        
        # Save to temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(image_bytes)
            temp_path = f.name
        
        try:
            # Get answer from model
            model = get_model()
            answer = model.answer_question(temp_path, question)
            
            return jsonify({'answer': answer})
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'model': 'BLIP VQA'})


if __name__ == '__main__':
    print("="*60)
    print("VQA Web Frontend Server")
    print("="*60)
    print("\nStarting server on http://localhost:5000")
    print("Open this URL in your browser to use the VQA interface.")
    print("\nPress Ctrl+C to stop the server.")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
