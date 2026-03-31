"""
Utility functions for VQA Activity
===================================
This module contains helper functions for image processing,
result display, and file operations.
"""

import os
from PIL import Image


def load_image(image_path):
    """
    Load and validate an image file.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        PIL.Image: Loaded image object
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If file is not a valid image
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    try:
        image = Image.open(image_path)
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise ValueError(f"Failed to load image: {e}")


def print_result(question, answer, image_path=None):
    """
    Print the Q&A result in a formatted way.
    
    Args:
        question (str): The question asked
        answer (str): The model's answer
        image_path (str, optional): Path to the image
    """
    print("\n" + "="*60)
    if image_path:
        print(f"Image: {os.path.basename(image_path)}")
    print("-"*60)
    print(f"Question: {question}")
    print(f"Answer:   {answer}")
    print("="*60 + "\n")


def save_result(question, answer, image_path, output_path):
    """
    Save the Q&A result to a file.
    
    Args:
        question (str): The question asked
        answer (str): The model's answer
        image_path (str): Path to the image
        output_path (str): Path to save the result
    """
    with open(output_path, 'a') as f:
        f.write(f"Image: {image_path}\n")
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write("-" * 40 + "\n")


def get_image_info(image_path):
    """
    Get basic information about an image.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        dict: Dictionary with image information
    """
    image = load_image(image_path)
    return {
        'path': image_path,
        'format': image.format,
        'mode': image.mode,
        'size': image.size,
        'width': image.width,
        'height': image.height
    }


def resize_image(image_path, output_path, max_size=512):
    """
    Resize an image while maintaining aspect ratio.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the resized image
        max_size (int): Maximum dimension size
    """
    image = load_image(image_path)
    
    # Calculate new size
    width, height = image.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    image.save(output_path)
    return output_path


def create_sample_questions():
    """
    Create a list of sample questions for testing VQA.
    
    Returns:
        list: Sample questions
    """
    return [
        "What is in the image?",
        "How many objects are there?",
        "What colors can you see?",
        "Describe the scene.",
        "Is there a person in the image?",
        "What is the main subject?",
        "What is the background?",
        "Are there any animals?",
        "What time of day might this be?",
        "What is the mood of this image?"
    ]
