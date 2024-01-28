from PIL import Image
import PIL.ImageOps
from io import BytesIO
import os

base = './src/sk'
base_out = './src/bw'

for file in os.listdir(base):
    file_name = file.split('/')[-1].split('.')[0]
    img_path = os.path.join(base, file)
    image_file = Image.open(img_path)

    if image_file.mode == 'RGBA':
        # Create a blank white image with the same size
        white_background = Image.new('RGBA', image_file.size, (250, 250, 250, 250))
        # Paste the PNG image onto the white background, using itself as the mask
        white_background.paste(image_file, (0, 0), image_file)
        # Convert to RGB to discard the alpha channel
        image_file = white_background.convert('RGB')

    # image_file.thumbnail((768, 768))
    image_file.thumbnail((512, 512))
    image_file = image_file.convert('L')

    # Define the threshold (you can adjust this)
    threshold = 240
    # Apply the threshold to each pixel
    image_file_bw = image_file.point(lambda x: 0 if x > threshold else 255)
    # Save or show the image
    image_file_bw.save(os.path.join( base_out, f'{file_name}_bw.png' ))
