from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import os
import sys
import torch

model = None
processor = None

def get_model_and_processor():
    global model, processor
    if model is None:
        print("正在加载模型...", file=sys.stderr)
        model_name = "google/vit-base-patch16-224"
        processor = ViTImageProcessor.from_pretrained(model_name)
        model = ViTForImageClassification.from_pretrained(model_name)
        model.eval()
        print("模型加载完成", file=sys.stderr)
    return model, processor

def classify_image(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件不存在: {image_path}")

    file_size = os.path.getsize(image_path)
    if file_size == 0:
        raise ValueError("文件为空")

    try:
        image = Image.open(image_path)
        image = image.convert("RGB")
        image = image.resize((224, 224), Image.Resampling.BILINEAR)

        model_obj, proc = get_model_and_processor()

        inputs = proc(images=[image], return_tensors="pt", do_resize=False)

        with torch.no_grad():
            outputs = model_obj(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            top5_probs, top5_indices = torch.topk(probs, k=5, dim=-1)

        results = []
        for i in range(5):
            label_id = top5_indices[0][i].item()
            score = top5_probs[0][i].item()
            label = model_obj.config.id2label[label_id]
            results.append({
                "label": label,
                "score": score
            })

        return results
    except Exception as e:
        raise Exception(f"图像识别失败: {str(e)}")
