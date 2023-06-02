import pickle
import PIL
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn.functional as F
import torchvision.models as models
from model import DecoderRNN, CNNtoRNN
from utils import show_image2
from project import db
from project.config import  ProductionConfig as prod
import requests
from io import BytesIO
from PIL import Image

import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
from vocab import Vocab_Builder
device = 'cpu'

mean = [0.485, 0.456, 0.406]

std = [0.229, 0.224, 0.225]

transform = transforms.Compose(
    [transforms.Resize((256,256)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)]
)

def read_by_imdecode(video_url):
    response = requests.get(video_url, stream=True)
    if response.status_code == 200:
        content = bytes()
        for chunk in response.iter_content(chunk_size=4096):
            content += chunk
            a = content.find(b'\xff\xd8')
            b = content.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = content[a:b+2]
                content = content[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                # Convert frame to PIL Image
                image = Image.fromarray(frame)
                return image.convert("RGB")
    else:
        raise ValueError("Failed to read frame from video stream")
    return None 

class EncoderCNN(nn.Module):

    def __init__(self, embed_size=256, train_CNN = False):
        super(EncoderCNN, self).__init__()
        self.train_CNN = train_CNN
        self.resnet50 = models.resnet50(pretrained=True)
        self.resnet_path = './weights/resnet50.pt'
        self.resnet50 = self.resnet50.load_state_dict( torch.load(self.resnet_path, map_location = 'cpu') )
        
        for name, param in self.resnet50.named_parameters():  
            if "fc.weight" in name or "fc.bias" in name:
                param.requires_grad = True
            else:
                param.requires_grad = self.train_CNN
        
        in_features = self.resnet50.fc.in_features
        
        modules = list(self.resnet50.children())[:-1]
        self.resnet50 = nn.Sequential(*modules)
        
        self.fc = nn.Linear(in_features,embed_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        
    def forward(self, images):
        # Fine tuning, we don't want to train 
        features = self.resnet50(images)
        features = features.view(features.size(0), -1)
        features = self.fc(features)
        return features

def load_checkpoint(checkpoint, model, optimizer):
    
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    step = checkpoint["step"]
    return step

def caption(img):
    img_t = transform(img)
    caps = model.caption_image(img_t.unsqueeze(0), vocab)
    # print(caps)
    caps = caps[1:-1]
    return ' '.join(caps)

def caption_of_urls(urls):
    for video in urls:
        url = video['url']
        print(url)
        image = read_by_imdecode(url)
        #show_image2(image,0)
        caption = caption(image)
        print(caption)

#vocab = Vocab_Builder(freq_threshold = 5)

# Load the pickle dump
vocab_path = 'vocab.pickle'

with open(vocab_path, 'rb') as f:
    vocab = pickle.load(f)

load_model = True
embed_size = 256
hidden_size = 256
vocab_size = len(vocab)
num_layers = 2
learning_rate = 3e-4
print(len(vocab))

model_path = './weights/my_checkpoint2.pth.tar'

model = CNNtoRNN(embed_size, hidden_size, vocab_size, num_layers).to(device)

criterion = nn.CrossEntropyLoss(ignore_index = vocab.stoi["<PAD>"])
optimizer = optim.Adam(model.parameters(), lr = learning_rate)
if load_model:
    step = load_checkpoint(torch.load(model_path ,map_location = 'cpu'), model, optimizer)

model.eval()

#image_path = './tests/black_face_girl_make-up_creative_model.jpg'
image_path = './tests/fixer.jpg'
img = PIL.Image.open(image_path)
caption = caption(img.convert('RGB'))
print(caption)

# Loop over images from DB
#videos = db.select_all_urls()
#caption_of_urls(videos)











