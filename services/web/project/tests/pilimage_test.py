from PIL import Image
import base64
import io

# Load the image
image = Image.open('zidane.jpg')

# Convert the image to bytes
image_bytes = io.BytesIO()
image.save(image_bytes, format='JPEG')
image_bytes.seek(0)

# Encode the image as base64 string
image_data = base64.b64encode(image_bytes.read()).decode('utf-8')

# Decode the base64 string back to image data
decoded_data = base64.b64decode(image_data)

# Create a new PIL image from the decoded data
decoded_image = Image.open(io.BytesIO(decoded_data))

# Display the original and decoded images
#image.show()
decoded_image.save('decoded_image.jpg')
