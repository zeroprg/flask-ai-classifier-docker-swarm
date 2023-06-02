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


from io import BytesIO

image_path = './tests/background3.jpg'






class CaptionResNet50():
    def __init__(self,device = 'cpu'):
        self.device = device
        # global vocab
        self.vocab = Vocab_Builder(freq_threshold = 5)
        # Load the pickle dump
        vocab_path = './weights/vocab (1).pickle'

        with open(vocab_path, 'rb') as f:
            self.vocab = pickle.load(f)

        print(len(self.vocab))
        embed_size = 350
        encoder_dim = 1024
        decoder_dim = 512
        attention_dim = 512
        vocab_size = len(self.vocab)
        learning_rate = 4e-5 # Modifed it after 10th epoch
        # resnet_path = './resnet50_captioning.pt'
        resnet_path = './weights/resnet5010.pt'

        self.encoder = EncoderCNN()

        # Load resnet weights
        self.encoder.load_state_dict( torch.load( resnet_path, map_location = 'cpu') )
        self.encoder.to(device)
        self.encoder.eval() # V. important to switch off Dropout and BatchNorm

        # decoder_path = './LastModelResnet50_v2_16.pth.tar'
        decoder_path = './weights/Flickr30k_Decoder_10.pth.tar'
        # global decoder
        self.decoder = Decoder(encoder_dim, decoder_dim, embed_size, vocab_size, attention_dim, device)    

        optimizer = optim.Adam(self.decoder.parameters(), lr = learning_rate)

        checkpoint = torch.load(decoder_path,map_location='cpu')
        self.decoder.load_state_dict(checkpoint["state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        step = checkpoint["step"]

        # return step
        #   step = load_checkpoint(torch.load(decoder_path ,map_location = 'cpu'), decoder, optimizer)

        self.decoder = self.decoder.to(device)
        self.decoder.eval()
    
    @staticmethod
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
    
    def predict_caption(self, image_bytes, expect = 'actor'):    
    
        img_t = self.transform_image(image_bytes)
        caption = ''
        encoded_output = self.encoder(img_t.unsqueeze(0).to(self.device))
        caps = self.decoder.beam_search(encoded_output,1)
        caps = caps[1:-1]
        if expect == 'actor':
            caption = [self.vocab.itos[idx] for idx in caps[:-1]]
        elif self.vocab.itos[caps[-3]] == 'a' or self.vocab.itos[caps[-3]] == 'the':            
            caption = [self.vocab.itos[idx] for idx in caps[-2:-1]]               
        
        return ' '.join(caption)    
        #for i in range(len(captions)):
        #    print("** Beam index " + str(i + 1) + ": " + captions[i] + "**")




if __name__ == "__main__":

    img = PIL.Image.open(image_path) #.convert("RGB")
    img.show()
    captionResNet50 = CaptionResNet50()
    #print(captionResNet50.predict_caption(img,expect="backgrnd")) run when need to populate background
    print(captionResNet50.predict_caption(img))
        
