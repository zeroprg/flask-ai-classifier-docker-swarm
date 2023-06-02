import pickle
from model import  EncoderCNN, Decoder
from vocab import Vocab_Builder
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn.functional as F
import torchvision.models as models
import PIL
from PIL import Image, ImageOps
import io
import time
import requests
import os

from io import BytesIO

image_path = './tests/background3.jpg'


def transform_image(image):
    mean = [0.485, 0.456, 0.406]

    std = [0.229, 0.224, 0.225]

    transform = transforms.Compose(
        [transforms.Resize((256,256)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)]
    )
#     image = Image.open(io.BytesIO(img_bytes) ).convert("RGB")
    return transform(image)
 
def predict_caption(image_bytes, expect = 'actor'):    
    captions = []
    img_t = transform_image(image_bytes)
    caption = ''
    encoded_output = encoder(img_t.unsqueeze(0).to(device))
    caps = decoder.beam_search(encoded_output,1)
    caps = caps[1:-1]
    if expect == 'actor':
        caption = [vocab.itos[idx] for idx in caps[:-1]]
    elif vocab.itos[caps[-3]] == 'a' or vocab.itos[caps[-3]] == 'the':            
        caption = [vocab.itos[idx] for idx in caps[-2:-1]]               
       
    return ' '.join(caption)    
    #for i in range(len(captions)):
    #    print("** Beam index " + str(i + 1) + ": " + captions[i] + "**")



device = 'cpu'
# global vocab
vocab = Vocab_Builder(freq_threshold = 5)

# Load the pickle dump
vocab_path = './weights/vocab (1).pickle'

with open(vocab_path, 'rb') as f:
    vocab = pickle.load(f)

print(len(vocab))
embed_size = 350
encoder_dim = 1024
decoder_dim = 512
attention_dim = 512
vocab_size = len(vocab)
learning_rate = 4e-5 # Modifed it after 10th epoch
# resnet_path = './resnet50_captioning.pt'
resnet_path = './weights/resnet5010.pt'

encoder = EncoderCNN()

# Load resnet weights
encoder.load_state_dict( torch.load( resnet_path, map_location = 'cpu') )
encoder.to(device)
encoder.eval() # V. important to switch off Dropout and BatchNorm

# decoder_path = './LastModelResnet50_v2_16.pth.tar'
decoder_path = './weights/Flickr30k_Decoder_10.pth.tar'
# global decoder
decoder = Decoder(encoder_dim, decoder_dim, embed_size, vocab_size, attention_dim, device)    

optimizer = optim.Adam(decoder.parameters(), lr = learning_rate)

checkpoint = torch.load(decoder_path,map_location='cpu')
decoder.load_state_dict(checkpoint["state_dict"])
optimizer.load_state_dict(checkpoint["optimizer"])
step = checkpoint["step"]

# return step
#   step = load_checkpoint(torch.load(decoder_path ,map_location = 'cpu'), decoder, optimizer)

decoder = decoder.to(device)
decoder.eval()



if __name__ == "__main__":

    img = PIL.Image.open(image_path) #.convert("RGB")
    img.show()

    #print(predict_caption(img,expect="backgrnd"))
    print(predict_caption(img))
        
