from flask import Flask, flash, request, redirect, url_for
import os
import torch
from torch import nn
from torchvision import transforms, models
from glob import glob
from PIL import Image

app = Flask(__name__)

fruits = ["Apple","Banana","Guava","Lime","Orange","Pomegranate"]
qualities = ["Bad","Good","Mixed"]

@app.route("/api")
def evaluate(): # input is a list of PIL Images
    raw_pics = []
    for i in glob("./*.jpg"):
        print(i)
        raw_pics.append(Image.open(i))
        break
    val_x_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((256,256),antialias=True),
        transforms.CenterCrop((224,224)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    pics = []
    for i in raw_pics:
        pics.append(val_x_transform(i))
    pics = torch.stack(pics)

    model = models.vgg16()
    model.classifier[6] = nn.Linear(in_features=4096,out_features=18)
    model.load_state_dict(torch.load("./model.pt",weights_only=True))

    with torch.no_grad():
        output = model(pics.float())
        sum = output.sum(dim=0)
        result = sum.argmax(dim=0).item()
        return f"{qualities[result%3]}_{fruits[int(result/3)]}"

    
