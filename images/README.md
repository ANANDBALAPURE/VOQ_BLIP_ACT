# Sample Images

This directory should contain sample images for testing the VQA system.

## Adding Your Own Images

1. Copy your images to this directory
2. Use them with the VQA system:

```bash
# Command line
python scripts/vqa_blip.py --image images/your_image.jpg --question "What is in the image?"

# Or with the web interface
python scripts/gradio_demo.py
```

## Recommended Image Types

For best results, use:
- Clear, well-lit images
- Common formats: JPG, PNG
- Resolution: 224x224 to 1024x1024 pixels

## Example Images to Try

1. **Objects**: Photos of everyday objects (cars, furniture, electronics)
2. **Scenes**: Indoor/outdoor scenes (rooms, streets, nature)
3. **People**: Photos with people doing activities
4. **Animals**: Photos of pets, wildlife
5. **Text**: Images containing text (signs, documents)

## Sample Image Sources

You can download sample images from:
- [Unsplash](https://unsplash.com/) - Free high-quality photos
- [Pexels](https://pexels.com/) - Free stock photos
- [COCO Dataset](https://cocodataset.org/) - Research dataset
