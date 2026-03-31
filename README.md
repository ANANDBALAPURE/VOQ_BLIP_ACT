# Visual Question Answering using BLIP

## TA Activity - Complete Tutorial Project

This project provides a complete implementation of Visual Question Answering (VQA) using the BLIP (Bootstrapping Language-Image Pre-training) model from Salesforce. The project includes command-line tools, a web interface, and Jupyter notebooks for interactive learning.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Installation Guide](#installation-guide)
4. [Quick Start](#quick-start)
5. [Usage Guide](#usage-guide)
6. [Project Structure](#project-structure)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Project Overview

### What is Visual Question Answering?

Visual Question Answering (VQA) is an AI task that combines computer vision and natural language processing. Given an image and a natural language question about that image, the goal is to produce an accurate natural language answer.

### What is BLIP?

BLIP (Bootstrapping Language-Image Pre-training) is a state-of-the-art vision-language model developed by Salesforce Research. It is pre-trained on large-scale image-text datasets and can perform various vision-language tasks including:

- Visual Question Answering
- Image Captioning
- Image-Text Retrieval

### Key Features of This Project

- **Command-line interface** for quick VQA tasks
- **Gradio web interface** for interactive exploration
- **Beautiful interactive frontend** with gradient colors
- **Jupyter notebooks** for learning and experimentation
- **Support for both CPU and GPU** execution
- **Sample code** for integration into your projects

---

## Prerequisites

Before you begin, ensure you have the following:

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB or more |
| GPU | Not required | NVIDIA GPU with 4GB+ VRAM |
| Storage | 5 GB | 10 GB (for model weights) |

### Software Requirements

- **Python**: Version 3.8 or higher
- **pip**: Latest version
- **Virtual environment** (recommended)

### Operating System Support

- Windows 10/11
- macOS 10.15+
- Ubuntu 18.04+

---

## Installation Guide

### Step 1: Extract the Project

```bash
# Extract the zip file
unzip VQA_BLIP_Activity.zip

# Navigate to the project directory
cd VQA_BLIP_Activity
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

This will install:
- PyTorch (deep learning framework)
- Transformers (Hugging Face library)
- Pillow (image processing)
- Gradio (web interface)
- Jupyter (notebooks)

### Step 4: Verify Installation

```bash
# Test that all packages are installed correctly
python -c "import torch; import transformers; from PIL import Image; print('All packages installed successfully!')"
```

### Step 5: Download Model Weights (Optional Pre-download)

The model weights will be downloaded automatically on first run. If you want to pre-download:

```bash
python -c "from transformers import BlipProcessor, BlipForQuestionAnswering; BlipProcessor.from_pretrained('Salesforce/blip-vqa-base'); BlipForQuestionAnswering.from_pretrained('Salesforce/blip-vqa-base'); print('Model downloaded!')"
```

---

## Quick Start

### Option 1: Interactive Web Interface

```bash
# Launch the Gradio web interface
python scripts/gradio_demo.py
```

Then open your browser to: `http://localhost:7860`

### Option 2: Beautiful Interactive Frontend (NEW!)

The project now includes a beautiful, modern frontend with gradient colors:

#### Method A: Standalone HTML (Demo Mode)

```bash
# Open the standalone HTML frontend directly in browser
open frontend/index.html  # macOS
xdg-open frontend/index.html  # Linux
start frontend/index.html  # Windows
```

**Note:** In standalone mode, the frontend runs in demo mode with simulated answers.

#### Method B: With Backend Server (Full AI Mode)

```bash
# Run the Flask server with BLIP backend
cd frontend
python frontend_server.py

# Then open http://localhost:5000 in your browser
```

**Frontend Features:**
- 🎨 Beautiful gradient UI with animated backgrounds
- 📷 Drag & drop image upload
- 💬 Interactive Q&A with instant AI answers
- 📝 Sample questions for quick testing
- 📜 Q&A history tracking
- ⚡ Modern, responsive design
- 🌙 Dark theme with glass-morphism effects

### Option 3: Command Line

```bash
# Ask a single question
python scripts/vqa_blip.py --image images/sample.jpg --question "What is in the image?"

# Interactive mode
python scripts/vqa_blip.py --interactive
```

### Option 4: Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open notebooks/VQA_Tutorial.ipynb
```

---

## Usage Guide

### Command Line Interface

#### Basic Usage

```bash
# Ask a single question
python scripts/vqa_blip.py --image path/to/image.jpg --question "Your question here"
```

#### Interactive Mode

```bash
# Start interactive mode
python scripts/vqa_blip.py --interactive

# In interactive mode:
# - Enter image path when prompted
# - Type questions about the image
# - Type 'new' to load a different image
# - Type 'quit' or 'exit' to stop
```

#### Batch Questions

```bash
# Create a questions file (one question per line)
echo "What is in the image?" > questions.txt
echo "How many objects are there?" >> questions.txt
echo "Describe the scene." >> questions.txt

# Run with questions file
python scripts/vqa_blip.py --image path/to/image.jpg --questions questions.txt --output results.txt
```

#### Model Selection

```bash
# Use base model (faster, less memory)
python scripts/vqa_blip.py --image image.jpg --question "What is this?" --model base

# Use large model (more accurate, requires more resources)
python scripts/vqa_blip.py --image image.jpg --question "What is this?" --model large
```

### Web Interface (Gradio)

#### Starting the Server

```bash
# Basic launch (local only)
python scripts/gradio_demo.py

# With public share link
python scripts/gradio_demo.py --share

# Custom port
python scripts/gradio_demo.py --port 8080
```

#### Using the Interface

1. **Upload Image**: Click or drag-and-drop an image
2. **Enter Question**: Type your question in the text box
3. **Get Answer**: Click "Get Answer" or press Enter
4. **Clear**: Click "Clear" to start over

### Python API

#### Basic Usage

```python
from scripts.vqa_blip import VQABlip
from PIL import Image

# Initialize the model
vqa = VQABlip()

# Answer a question
answer = vqa.answer_question("path/to/image.jpg", "What is in the image?")
print(answer)
```

#### Batch Processing

```python
from scripts.vqa_blip import VQABlip

vqa = VQABlip()

questions = [
    "What is in the image?",
    "How many objects are there?",
    "Describe the colors."
]

results = vqa.batch_qa("path/to/image.jpg", questions)
for question, answer in results:
    print(f"Q: {question}")
    print(f"A: {answer}")
```

---

## Project Structure

```
VQA_BLIP_Activity/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── verify_setup.py          # Installation verification
├── quick_start.py           # Quick demo script
├── VQA_Activity_Guide.pdf   # Complete tutorial guide
├── frontend/                # Beautiful interactive frontend
│   ├── index.html           # Standalone HTML frontend
│   ├── page.tsx             # React/Next.js page
│   ├── api_vqa_route.ts     # API route template
│   ├── package.json         # Node.js dependencies
│   └── README.md            # Frontend documentation
├── scripts/
│   ├── vqa_blip.py          # Main VQA script
│   └── gradio_demo.py       # Web interface
├── notebooks/
│   └── VQA_Tutorial.ipynb   # Interactive tutorial
├── utils/
│   ├── __init__.py
│   └── helpers.py           # Utility functions
└── images/
    ├── README.md
    └── sample.jpg           # Test image
```

### File Descriptions

| File | Description |
|------|-------------|
| `requirements.txt` | List of Python packages needed |
| `scripts/vqa_blip.py` | Main script with CLI and VQA class |
| `scripts/gradio_demo.py` | Web interface application |
| `frontend/index.html` | Beautiful interactive frontend (standalone) |
| `notebooks/VQA_Tutorial.ipynb` | Step-by-step tutorial |
| `utils/helpers.py` | Image loading and display utilities |
| `VQA_Activity_Guide.pdf` | Complete tutorial guide |

---

## Troubleshooting

### Common Issues and Solutions

#### 1. CUDA Out of Memory

**Problem**: `RuntimeError: CUDA out of memory`

**Solutions**:
```bash
# Use CPU instead
python scripts/vqa_blip.py --image image.jpg --question "What?" --device cpu

# Or use the smaller base model
python scripts/vqa_blip.py --image image.jpg --question "What?" --model base
```

#### 2. Model Download Fails

**Problem**: Connection error when downloading model weights

**Solutions**:
- Check your internet connection
- Use a VPN if needed
- Try downloading manually:
```python
from transformers import BlipProcessor, BlipForQuestionAnswering
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
```

#### 3. Image Loading Error

**Problem**: `PIL.UnidentifiedImageError: cannot identify image file`

**Solutions**:
- Ensure image is in supported format (JPG, PNG, BMP, etc.)
- Check if image file is corrupted
- Convert image to JPG/PNG using an image editor

#### 4. Import Error

**Problem**: `ModuleNotFoundError: No module named 'transformers'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 5. Slow Performance on CPU

**Problem**: Model runs very slowly on CPU

**Solutions**:
- Use GPU if available (automatic detection)
- Use the base model instead of large
- Reduce image size before processing

---

## FAQ

### General Questions

**Q: What types of questions can I ask?**

A: You can ask questions about:
- Objects in the image ("What is this?", "How many cars are there?")
- Colors ("What color is the shirt?")
- Actions ("What is the person doing?")
- Counting ("How many people are in the image?")
- Descriptions ("Describe the scene.")

**Q: What image formats are supported?**

A: All common image formats: JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP

**Q: How accurate is the model?**

A: BLIP achieves state-of-the-art results on VQA benchmarks. Accuracy depends on:
- Image quality
- Question clarity
- Complexity of the visual content

### Technical Questions

**Q: Can I use a different model?**

A: Yes! You can modify the code to use other models like:
- LLaVA
- MiniGPT-4
- GPT-4V (API required)
- Other BLIP variants

**Q: How do I improve performance?**

A: Tips for better results:
1. Use clear, high-quality images
2. Ask specific questions
3. Use the large model for complex scenes
4. Process images in batch for efficiency

**Q: Can I use this commercially?**

A: Check the license of the BLIP model. As of this writing, Salesforce BLIP uses an MIT license for the code and model weights.

---

## Running on Anti-Gravity Platform

If you're using the Anti-Gravity platform:

### Step 1: Upload the Project

Upload the extracted `VQA_BLIP_Activity` folder to your Anti-Gravity workspace.

### Step 2: Open Terminal

Open a terminal in your Anti-Gravity workspace.

### Step 3: Install Dependencies

```bash
cd VQA_BLIP_Activity
pip install -r requirements.txt
```

### Step 4: Run the Activity

```bash
# Option 1: Web Interface (if Anti-Gravity supports it)
python scripts/gradio_demo.py

# Option 2: Command Line
python scripts/vqa_blip.py --image images/sample.jpg --question "What is in the image?"

# Option 3: Jupyter Notebook
jupyter notebook notebooks/VQA_Tutorial.ipynb
```

### Step 5: Follow the Tutorial

Complete the exercises in the Jupyter notebook for the full learning experience.

---

## Learning Objectives

After completing this activity, you will be able to:

1. Understand what Visual Question Answering is and its applications
2. Load and use pre-trained vision-language models
3. Process images for AI model input
4. Generate answers to questions about images
5. Build interactive applications using Gradio
6. Integrate VQA into your own projects

---

## Additional Resources

- [BLIP Paper](https://arxiv.org/abs/2201.12086)
- [Hugging Face BLIP Documentation](https://huggingface.co/docs/transformers/model_doc/blip)
- [VQA Dataset](https://visualqa.org/)
- [Gradio Documentation](https://www.gradio.app/docs/)

---

## Support

If you encounter any issues:

1. Check the Troubleshooting section above
2. Review the FAQ section
3. Consult with your TA
4. Check the Hugging Face forums for model-specific issues

---

**Happy Learning! 🎓**
