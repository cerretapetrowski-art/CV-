import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import sys

model = None
labels = None
transform = None

def get_model():
    global model, labels, transform
    if model is None:
        print("正在加载模型...", file=sys.stderr)
        weights = models.ResNet50_Weights.IMAGENET1K_V2
        model = models.resnet50(weights=weights)
        model.eval()
        labels = weights.meta["categories"]
        transform = weights.transforms()
        print("模型加载完成", file=sys.stderr)
    return model, labels, transform

def classify_image(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"文件不存在: {image_path}")

    file_size = os.path.getsize(image_path)
    if file_size == 0:
        raise ValueError("文件为空")

    try:
        image = Image.open(image_path).convert("RGB")

        m, lbls, trans = get_model()

        input_tensor = trans(image).unsqueeze(0)

        with torch.no_grad():
            outputs = m(input_tensor)
            probs = torch.softmax(outputs, dim=-1)
            top5_probs, top5_indices = torch.topk(probs, k=5, dim=-1)

        results = []
        for i in range(5):
            idx = top5_indices[0][i].item()
            score = top5_probs[0][i].item()
            label = lbls[idx]
            results.append({
                "label": label,
                "score": score
            })

        return results
    except Exception as e:
        raise Exception(f"图像识别失败: {str(e)}")
