from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from PIL import Image
import torch
import os

# from controlnet_aux import HEDdetector
from diffusers.utils import load_image

controlnet = ControlNetModel.from_pretrained(
    # "lllyasviel/sd-controlnet-scribble",
    './models/ControlNet/sd-controlnet-scribble',
    torch_dtype=torch.float32,
    # low_cpu_mem_usage=False,
    ignore_mismatched_sizes=True,
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "./models/meinamix_meinaV9",
    controlnet=controlnet,
    safety_checker=None,
    torch_dtype=torch.float32
)

pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

character = input('Prompt: ')

if character == '':
    character = '1girl,cute,huge breasts,short hair,black hair,squatting,side view,white shirt,mini skirt,black skirt,bare legs,black shoes,'

prompt = f"(masterpiece, best quality, high quality, highresolution:1.4),{character},((simple background, white background)):1.3"
negative_prompt = "(worst quality, low quality, normal quality), bad-artist,blurry, ugly,((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face)),clothes,logo,watermark,muscles:1.3,elf,elf ears,headphones,"
base = './src/bw'
for image_bw in os.listdir(base):
    image_path = os.path.join(base, image_bw)
    out_file = f'./out/cl_{image_bw}'
    print(f"{image_path} -> {out_file}")
    image = pipe(
        prompt
        , Image.open(image_path)
        , num_inference_steps=22
        , negative_prompt = negative_prompt
    ).images[0]
    image.save(out_file)
