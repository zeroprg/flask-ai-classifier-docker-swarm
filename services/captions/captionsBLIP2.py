import torch
from PIL import Image
from transformers import AutoProcessor, Blip2ForConditionalGeneration, AutoTokenizer

# Load the processor, tokenizer, and model

model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")



# Set the device and torch data type
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch_dtype = torch.float32

# Load and preprocess the image
image_path = "C:/Users/zeroprg/Pictures/Saved Pictures/Big Horn 8/DJI_0027.jpg"
image = Image.open(image_path)
image_tensor = processor(image, return_tensors="pt").to(device, dtype=torch_dtype)

# Generate captions
with torch.no_grad():
    model = model.to(device)
    inputs = {"input_ids": image_tensor.input_ids}
    outputs = model.generate(**inputs, max_length=50)

# Decode and print the captions
captions = processor.decode(outputs[0], skip_special_tokens=True).strip()
print("Generated Caption:", captions)
