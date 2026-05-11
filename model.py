from transformers import pipeline
from PIL import Image
import torch
from pathlib import Path

classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        classifier = pipeline(
            "image-classification",
            model="google/vit-base-patch16-224",
            device=-1
        )
    return classifier

def classify_image(image_path: str):
    try:
        image = Image.open(image_path)
        cls = get_classifier()
        results = cls(image)
        return results
    except Exception as e:
        raise Exception(f"图像识别失败: {str(e)}")
