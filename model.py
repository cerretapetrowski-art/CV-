from transformers import pipeline
from PIL import Image
import os
import sys

classifier = None

def get_classifier():
    global classifier
    if classifier is None:
        print("正在加载模型...", file=sys.stderr)
        classifier = pipeline(
            "image-classification",
            model="google/vit-base-patch16-224",
            device=-1
        )
        print("模型加载完成", file=sys.stderr)
    return classifier

def classify_image(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件不存在: {image_path}")

    file_size = os.path.getsize(image_path)
    if file_size == 0:
        raise ValueError("文件为空")

    try:
        image = Image.open(image_path)
        image = image.convert("RGB")

        target_size = (224, 224)
        image = image.resize(target_size, Image.Resampling.BILINEAR)

        cls = get_classifier()
        results = cls(image)

        return results
    except Exception as e:
        raise Exception(f"图像识别失败: {str(e)}")