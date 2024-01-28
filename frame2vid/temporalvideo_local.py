import os
import glob
import requests
import json
import random
from pprint import pprint
import base64
from io import BytesIO


# Replace with the actual path to your image file and folder
x_path = "./init.png"
y_folder = "./input"
seed = int(random.random()*1000)

output_folder = "outputlocal"
os.makedirs(output_folder, exist_ok=True)

def get_image_paths(folder):
    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    files = []
    for ext in image_extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)

y_paths = get_image_paths(y_folder)

p = """
((masterpiece)),(((best quality))),highly detailed,illustration, sharp edges, (ultra highres:1.0),
1girl,cute face, perfect face,happy,solo,
lora:hinataHyuugaLora_hinata:1>,long hair,dark hair,purple clothes,crop top, white eyes,blind, huge ass, (huge breasts:1.1),head band,ninja band,
thicc,thick body,
((simple background, pink background)),
"""

n = """
(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, inaccurate eyes, extra digit, fewer digits, (extra arms:1.2),accessories,loli,muscles,muscular,nipples,cat ears,nsfw,transparent clothes,
"""
# (low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, accessories,loli,muscles,muscular,

# (ugly:1.3), (fused fingers), (too many fingers), (bad anatomy:1.5), (watermark:1.5), (words), letters, untracked eyes, asymmetric eyes, floating head, (logo:1.5), (bad hands:1.3), (mangled hands:1.2), (missing hands), (missing arms), backward hands, floating jewelry, unattached jewelry, floating head, doubled head, unattached head, doubled head, head in body, (misshapen body:1.1), (badly fitted headwear:1.2), floating arms, (too many arms:1.5), limbs fused with body, (facial blemish:1.5), badly fitted clothes, imperfect eyes, untracked eyes, crossed eyes, hair growing from clothes, partial faces, hair not attached to head


def send_request(last_image_path, temp_path,current_image_path):
    url = "http://localhost:7860/sdapi/v1/img2img"
    # base_url = "https://6c023487267674edea.gradio.live"
    # url = f"{base_url}/sdapi/v1/img2img"

    # print(f"[+] Opening: {last_image_path}")
    with open(last_image_path, "rb") as f:
        last_image = base64.b64encode(f.read()).decode("utf-8")

    with open(current_image_path, "rb") as b:
        current_image = base64.b64encode(b.read()).decode("utf-8")

    data = {
        "init_images": [current_image],
        "inpainting_fill": 0,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 1,
        "inpainting_mask_invert": 1,
        "resize_mode": 0,
        "denoising_strength": 0.45,
        "prompt": p,
        "negative_prompt": n,
        "alwayson_scripts": {
            "ControlNet":{
                "args": [
                    #{
                    #        "input_image": current_image,
                    #        "module": "canny",
                    #        "model": "control_canny-fp16 [e3fe7712]",
                    #        "weight": 0.6,
                    #        "mask": "",
                    #        "resize_mode": "Scale to Fit (Inner Fit)",
                    #        # "lowvram": False,
                    #        "processor_res": 512,
                    #        "threshold_a": 100.0,
                    #        "threshold_b": 255.0,
                    #        "guidance": 0.6,
                    #        "guidance_start": 0.0,
                    #        "guidance_end": 1.0,
                    #        # "guessmode": False
                    #},
                    #{
                    #    # control_v11p_sd15_canny
                    #    "input_image": current_image,
                    #    "module": "hed",
                    #    "model": "control_hed-fp16 [13fee50b]",
                    #    "weight": 1.5,
                    #    "guidance": 1,
                    #\},
                    {
                        "input_image": last_image,
                        "model": "diff_control_sd15_temporalnet_fp16 [adc6bd97]",
                        "module": "none",
                        "weight": 0.6,
                        "guidance": 1,
                    }
                ]
            }
        },
        "seed": 401, # seed,
        "subseed": -1,
        "subseed_strength": -1,
        "sampler_index": "Euler a",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 45,
        "cfg_scale": 7,
        "width": 512, # 254, # 512
        "height": 904, # 456, # 904
        "restore_faces": False,
        "include_init_images": True,
        "override_settings": {},
        "override_settings_restore_afterwards": True
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.content
    else:
        try:
            error_data = response.json()
            print("Error:")
            print(str(error_data))
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON error data.")
        return None

output_images = []
output_paths = []
total = len(y_paths)

for i, ref_image in enumerate(y_paths):
    if i != 0:
        x_path = output_paths[-1]
    print(f"[+] Processing {x_path} with seed {seed}: {i+1}/{total} ({(i+1/total)*100:.1f}%)")
    output_images.append(send_request(x_path, y_folder, ref_image))
    data = json.loads(output_images[-1])
    encoded_image = data["images"][0]
    current_output = os.path.join(output_folder, f"{i+1:04d}.png")
    output_paths.append(current_output)
    with open(current_output, "wb") as f:
        f.write(base64.b64decode(encoded_image))

#for i in range(total):
#    n = i+1
#    result_image = output_images[i-1]
#    temp_image_path = os.path.join(output_folder, f"{i:04d}.png")
#    data = json.loads(result_image)
#    encoded_image = data["images"][0]
#    with open(temp_image_path, "wb") as f:
#        f.write(base64.b64decode(encoded_image))
#    output_paths.append(temp_image_path)
#    result = send_request(temp_image_path, y_folder, y_paths[i])
#    output_images.append(result)
#    print(f"[!] Seed {seed}: {n}/{total} ({(n/total)*100:.2f}%)")
