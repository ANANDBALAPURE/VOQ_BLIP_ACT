"""
Visual Question Answering using BLIP Model
==========================================
This script implements a Visual Question Answering system using the BLIP 
(Bootstrapping Language-Image Pre-training) model from Salesforce.

Author: TA Activity
Date: 2024
"""

import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering
import argparse
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_image, print_result, save_result


class VQABlip:
    """
    Visual Question Answering class using BLIP model.
    
    BLIP is a powerful vision-language model that can understand images
    and answer questions about them. It uses a unified architecture for
    both image understanding and language generation.
    """
    
    def __init__(self, model_name="Salesforce/blip-vqa-base", device=None):
        """
        Initialize the VQA model.
        
        Args:
            model_name (str): Name of the BLIP model to use
                - "Salesforce/blip-vqa-base": Base model (faster, less memory)
                - "Salesforce/blip-vqa-capfilt-large": Large model (more accurate)
            device (str): Device to run the model on ('cuda', 'cpu', or None for auto)
        """
        print(f"Loading BLIP VQA model: {model_name}")
        print("This may take a few minutes on first run...")
        
        # Set device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        print(f"Using device: {self.device}")
        
        # Load processor and model
        try:
            self.processor = BlipProcessor.from_pretrained(model_name)
            self.model = BlipForQuestionAnswering.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def answer_question(self, image_path, question, return_confidence=False):
        """
        Answer a question about an image.
        
        Args:
            image_path (str): Path to the image file
            question (str): Question to ask about the image
            return_confidence (bool): Whether to return confidence scores
            
        Returns:
            str: Answer to the question
            float (optional): Confidence score if return_confidence is True
        """
        # Load and validate image
        try:
            image = load_image(image_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            raise
        
        # Process inputs
        inputs = self.processor(image, question, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate answer
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=20)
        
        # Decode answer
        answer = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        return answer
    
    def batch_qa(self, image_path, questions):
        """
        Answer multiple questions about a single image.
        
        Args:
            image_path (str): Path to the image file
            questions (list): List of questions to answer
            
        Returns:
            list: List of (question, answer) tuples
        """
        results = []
        for question in questions:
            answer = self.answer_question(image_path, question)
            results.append((question, answer))
        return results


def interactive_mode(vqa_model):
    """
    Run the VQA model in interactive mode.
    Users can input image paths and questions interactively.
    """
    print("\n" + "="*60)
    print("Interactive Visual Question Answering Mode")
    print("="*60)
    print("Enter 'quit' or 'exit' to stop")
    print("Enter 'new' to load a new image")
    print("="*60 + "\n")
    
    current_image = None
    
    while True:
        try:
            # Get image path if not set
            if current_image is None:
                image_path = input("Enter image path: ").strip()
                if image_path.lower() in ['quit', 'exit']:
                    break
                if not os.path.exists(image_path):
                    print(f"Error: Image not found at {image_path}")
                    continue
                current_image = image_path
                print(f"Image loaded: {current_image}")
            
            # Get question
            question = input("\nEnter your question (or 'new'/'quit'): ").strip()
            
            if question.lower() in ['quit', 'exit']:
                break
            elif question.lower() == 'new':
                current_image = None
                continue
            
            if not question:
                print("Please enter a question.")
                continue
            
            # Get answer
            answer = vqa_model.answer_question(current_image, question)
            print_result(question, answer, current_image)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Visual Question Answering using BLIP Model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single question about an image
  python vqa_blip.py --image path/to/image.jpg --question "What is in the image?"
  
  # Interactive mode
  python vqa_blip.py --interactive
  
  # Multiple questions from file
  python vqa_blip.py --image path/to/image.jpg --questions questions.txt
  
  # Use large model for better accuracy
  python vqa_blip.py --image path/to/image.jpg --question "Describe the scene" --model large
        """
    )
    
    parser.add_argument(
        "--image", "-i",
        type=str,
        help="Path to the image file"
    )
    parser.add_argument(
        "--question", "-q",
        type=str,
        help="Question to ask about the image"
    )
    parser.add_argument(
        "--questions", "-Q",
        type=str,
        help="Path to a file containing questions (one per line)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        choices=["base", "large"],
        default="base",
        help="Model size to use (default: base)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file to save results"
    )
    parser.add_argument(
        "--device", "-d",
        type=str,
        choices=["cuda", "cpu"],
        help="Device to run on (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Select model
    model_name = "Salesforce/blip-vqa-base" if args.model == "base" else "Salesforce/blip-vqa-capfilt-large"
    
    # Initialize model
    vqa = VQABlip(model_name=model_name, device=args.device)
    
    # Run based on mode
    if args.interactive:
        interactive_mode(vqa)
    elif args.image and args.question:
        answer = vqa.answer_question(args.image, args.question)
        print_result(args.question, answer, args.image)
        if args.output:
            save_result(args.question, answer, args.image, args.output)
    elif args.image and args.questions:
        # Load questions from file
        with open(args.questions, 'r') as f:
            questions = [line.strip() for line in f if line.strip()]
        results = vqa.batch_qa(args.image, questions)
        for q, a in results:
            print_result(q, a, args.image)
        if args.output:
            with open(args.output, 'w') as f:
                for q, a in results:
                    f.write(f"Q: {q}\nA: {a}\n\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
