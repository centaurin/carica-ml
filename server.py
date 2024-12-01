from flask import Flask, request, jsonify, Response
import torch
from torch import nn
from torchvision import transforms, models
from PIL import Image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1000 * 1000  # 25 MB

fruits = ["Apple", "Banana", "Guava", "Lime", "Orange", "Pomegranate"]
qualities = ["Bad", "Good", "Mixed"]
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
val_x_transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Resize((256, 256), antialias=True),
        transforms.Lambda(lambda x: x / 255),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)
model = models.vgg16()
model.classifier[6] = nn.Linear(in_features=4096, out_features=18)
model.load_state_dict(
    torch.load("./model.pt", map_location=torch.device("cpu"))
)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api", methods=["POST"])
def evaluate():  # input is a list of PIL Images
    files = request.files.getlist("file")
    if len(files) == 0:
        return Response("No files provided", status=400)
    pics = []
    for i in files:
        if i.filename is not None and i.filename == "":
            return Response("No files provided", status=400)
        pics.append(val_x_transform(Image.open(i.stream).convert("RGB")))
    pics = torch.stack(pics)
    with torch.no_grad():
        output = model(pics.float())
        sum = output.sum(dim=0)
        result = sum.argmax(dim=0).item()
        return jsonify(type=fruits[int(result / 3)], quality=qualities[result % 3])
