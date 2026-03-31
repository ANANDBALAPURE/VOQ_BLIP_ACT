"""
Quick Start Demo for Visual Question Answering
==============================================
This script provides a simple demonstration of the VQA system.
Run this script to quickly test the system with a sample image.

Usage:
    python quick_start.py [image_path]
    
If no image path is provided, it will use a sample image.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.vqa_blip import VQABlip
from utils.helpers import load_image, print_result, create_sample_questions


def main():
    """Run a quick demo of the VQA system."""
    print("="*60)
    print("Visual Question Answering - Quick Start Demo")
    print("="*60)
    
    # Get image path
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Default sample images to try
        default_paths = [
            "images/sample.jpg",
            "images/sample.png",
            "../images/sample.jpg",
        ]
        image_path = None
        for path in default_paths:
            if os.path.exists(path):
                image_path = path
                break
        
        if image_path is None:
            print("\nNo sample image found. Please provide an image path:")
            print("Usage: python quick_start.py <image_path>")
            print("\nExample:")
            print("  python quick_start.py path/to/your/image.jpg")
            return
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"\nError: Image not found at {image_path}")
        return
    
    print(f"\nUsing image: {image_path}")
    
    # Initialize VQA model
    print("\nInitializing BLIP VQA model...")
    print("(This may take a moment on first run)")
    
    try:
        vqa = VQABlip()
    except Exception as e:
        print(f"Error initializing model: {e}")
        return
    
    # Sample questions
    questions = create_sample_questions()
    
    print("\n" + "="*60)
    print("Running Sample Questions")
    print("="*60)
    
    # Ask sample questions
    for i, question in enumerate(questions[:5], 1):  # Limit to first 5
        print(f"\n[{i}/{5}] Processing...")
        try:
            answer = vqa.answer_question(image_path, question)
            print_result(question, answer, image_path)
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)
    print("\nFor more options, try:")
    print("  python scripts/vqa_blip.py --help")
    print("  python scripts/gradio_demo.py")
    print("\nOr open the Jupyter notebook:")
    print("  jupyter notebook notebooks/VQA_Tutorial.ipynb")


if __name__ == "__main__":
    main()
