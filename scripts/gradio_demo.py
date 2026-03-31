"""
Gradio Web Interface for Visual Question Answering
===================================================
This script provides a user-friendly web interface for the VQA system
using Gradio. It allows users to upload images and ask questions through
a browser-based interface.

Run this script and open the provided URL in your browser.

Author: TA Activity
Date: 2024
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering


class VQAGradioApp:
    """
    Gradio-based Web Application for Visual Question Answering.
    
    This class creates an interactive web interface where users can:
    - Upload images (drag and drop or click to upload)
    - Type questions about the image
    - Get instant answers from the BLIP model
    """
    
    def __init__(self, model_name="Salesforce/blip-vqa-base"):
        """
        Initialize the Gradio application.
        
        Args:
            model_name (str): Name of the BLIP model to use
        """
        self.model_name = model_name
        self.processor = None
        self.model = None
        self.device = None
        
    def load_model(self):
        """Load the BLIP model (lazy loading for faster startup)."""
        if self.model is not None:
            return
            
        print(f"Loading model: {self.model_name}")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        
        self.processor = BlipProcessor.from_pretrained(self.model_name)
        self.model = BlipForQuestionAnswering.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()
        print("Model loaded!")
    
    def answer_question(self, image, question):
        """
        Answer a question about an image.
        
        Args:
            image: PIL Image or numpy array from Gradio
            question (str): Question to answer
            
        Returns:
            str: Answer to the question
        """
        if image is None:
            return "Please upload an image first!"
        
        if not question or question.strip() == "":
            return "Please enter a question!"
        
        # Ensure model is loaded
        self.load_model()
        
        # Convert to PIL Image if needed
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Process and generate
        inputs = self.processor(image, question, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=50)
        
        answer = self.processor.decode(outputs[0], skip_special_tokens=True)
        return answer
    
    def create_interface(self):
        """
        Create the Gradio interface.
        
        Returns:
            gr.Interface: Gradio interface object
        """
        # Define example questions
        example_questions = [
            "What is in the image?",
            "How many objects are there?",
            "Describe the scene.",
            "What colors can you see?",
            "Is there a person in the image?",
            "What is the main subject?",
        ]
        
        # Create the interface
        with gr.Blocks(
            title="Visual Question Answering",
            theme=gr.themes.Soft()
        ) as interface:
            gr.Markdown(
                """
                # 🔍 Visual Question Answering with BLIP
                
                Upload an image and ask questions about it! This demo uses the BLIP 
                (Bootstrapping Language-Image Pre-training) model from Salesforce.
                
                **How to use:**
                1. Upload an image (drag & drop or click)
                2. Type your question in the text box
                3. Click "Get Answer" to see the result
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    image_input = gr.Image(
                        label="Upload Image",
                        type="pil",
                        height=400
                    )
                    question_input = gr.Textbox(
                        label="Your Question",
                        placeholder="What would you like to know about this image?",
                        lines=2
                    )
                    submit_btn = gr.Button("Get Answer", variant="primary")
                    clear_btn = gr.Button("Clear", variant="secondary")
                
                with gr.Column(scale=1):
                    output_text = gr.Textbox(
                        label="Answer",
                        lines=3,
                        interactive=False
                    )
                    gr.Markdown("### 💡 Example Questions")
                    for q in example_questions:
                        gr.Button(q, size="sm").click(
                            lambda x=q: x,
                            outputs=question_input
                        )
            
            # Event handlers
            submit_btn.click(
                fn=self.answer_question,
                inputs=[image_input, question_input],
                outputs=output_text
            )
            
            question_input.submit(
                fn=self.answer_question,
                inputs=[image_input, question_input],
                outputs=output_text
            )
            
            clear_btn.click(
                fn=lambda: (None, "", ""),
                outputs=[image_input, question_input, output_text]
            )
            
            gr.Markdown(
                """
                ---
                **Note:** The model will be loaded on first use, which may take a few moments.
                
                **Model:** Salesforce BLIP VQA Base
                """
            )
        
        return interface
    
    def launch(self, share=False, server_name="0.0.0.0", server_port=7860):
        """
        Launch the Gradio application.
        
        Args:
            share (bool): Whether to create a public link
            server_name (str): Server name to bind to
            server_port (int): Port to run on
        """
        interface = self.create_interface()
        interface.launch(
            share=share,
            server_name=server_name,
            server_port=server_port
        )


def main():
    """Main entry point for the Gradio application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Launch Gradio Web Interface for VQA"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public shareable link"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the server on"
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["base", "large"],
        default="base",
        help="Model size to use"
    )
    
    args = parser.parse_args()
    
    model_name = "Salesforce/blip-vqa-base" if args.model == "base" else "Salesforce/blip-vqa-capfilt-large"
    
    print("="*60)
    print("Starting Visual Question Answering Web Interface")
    print("="*60)
    
    app = VQAGradioApp(model_name=model_name)
    app.launch(share=args.share, server_port=args.port)


if __name__ == "__main__":
    main()
