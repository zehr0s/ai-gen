import os
import sys
import json
import random
import base64
import datetime
import requests
from io import BytesIO

import datetime

"""
if model_name == 'V08V08':
    prompts = [
        "(masterpiece), best quality, ultra high res, (sharp focus), (photorealistic:1.4), (PureErosFace_V1:0.7), nsfw, POV from behind, hetero, angel face, beautiful, big eyes, cute , vaginal insertion, all fours, lookback, vaginal penetration from behind, ( annakendrick:1.0), (orgasm:1.2), (office lady:1.4), black skirt above ass, wet pussy, stockings, dark hair, skirt, glasses, side light, pureerosface_v1",
        "(NSFW:1.3), looking away, (school uniform, serafuku, thighhighs), ass focus, anal, spread ass, hands spreading ass chicks, open asshole, anal gap, 1 girl, solo , backshot, back view, from behind, (huge breasts:1.5), (curvy, thicc:1.3), (anal gap:1.4), choker, earrings, (ponytail), class room,(finely detailed beautiful eyes: 1.2),beautiful detailed nose, best quality, masterpiece, ultra high res,(photo realistic:1.1),professional lighting, physically-based rendering, <lora:Japanese-doll-likeness:0.7> <lora:Korean-doll-likeness:0.4>, translucent clothes, spread legs, naked ass, bare ass" + random.choice([', sitting dowm, squating', '']),
    ]
    negative = [
        "paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, manboobs, backlight, glasses, panty, anime, cartoon, drawing, illustration, boring,long neck, out of frame, extra fingers, mutated hands, monochrome, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, glitchy, bokeh, (((long neck))), ((flat chested)), red eyes, extra heads, close up, text ,watermarks, logo",
        "(worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)),paintings, sketches,skin spots, acnes, skin blemishes, bad anatomy,facing away, looking away,tilted head, mult multiple girls, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross",
    ]
"""

def send_request(prompt, negative_prompt="", steps=20, width=512, height=512, seed=-1, override_payload = None):
    url = "http://localhost:7860/sdapi/v1/txt2img"
    # base_url = "https://6c023487267674edea.gradio.live"
    # url = f"{base_url}/sdapi/v1/img2img"

    # print(f"[+] Opening: {last_image_path}")
    #with open(last_image_path, "rb") as f:
    #    last_image = base64.b64encode(f.read()).decode("utf-8")

    #with open(current_image_path, "rb") as b:
    #    current_image = base64.b64encode(b.read()).decode("utf-8")

    data = {
        "enable_hr": [True, False][1],
        "denoising_strength": 0,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": "Latent",
        "hr_second_pass_steps": 10,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        # "hr_sampler_name": "Latent",
        "hr_prompt": "",
        "hr_negative_prompt": "",
        #"styles": [
        #    "string"
        #],
        "seed": seed,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        #"sampler_name": "string",
        "batch_size": 1,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": 8,
        "width": width,
        "height": height,
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "eta": 0.16, # 1
        "s_min_uncond": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": False,
        "script_args": [],
        "sampler_index": "Euler a", # "Euler", # "Euler a",
        #"script_name": "string",
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {}
    }
    if override_payload:
        data.update(override_payload)

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


out_folder = 'output'
os.makedirs(out_folder, exist_ok=True)

p = """
((masterpiece)),(((best quality))),highly detailed,illustration, sharp edges, (ultra highres:1.0),
1girl,cute face, perfect face,happy,cowboy shot,
<character>
wide hips,small waist,large breasts,(huge breasts:1.2),thicc,thick body,
happy,looking at viewer,
((simple background, dark background)),
"""

characters = [
    '<lora:midnightMHA_NAI_v2-8:1>, midnightmha, boku no hero academia, purple hair, very long hair, blue eyes, large breasts, white bodysuit, domino mask, thighhighs, thigh boots, handcuffs, belt, garter straps',
    '<lora:Nero:1>,secre swallowtail, wings, thighhighs, black wings, black capelet, capelet, cleavage, dress, black thighhighs, see-through, black dress, demon horns, antenna hair, white pupils, bright pupils, feathered wings, black skirt,',
    '<lora:Dawn:1>,dawn \(pokemon\), beanie, long hair, blue hair, blue eyes, black sleeveless shirt, pink scarf, pink skirt, pink boots, hands on hips,',
    '<lora:Gwen:0.7>,orange hair,short hair,Gwendolyn_Tennyson, smirk, long sleeves, white pants,',
    '<lora:gwentennyson:0.6>,gwentennyson,orange hair,thicc,thick body,short hair,blue sweater, gray skirt,',
    'clipboard <lora:JOY-10:1> ,nurse joy, pokemon, blue eyes,  long hair, pink hair, short sleeves, nurse, blush, holding, puffy short sleeves, puffy sleeves, nurse cap,  hat, dress, apron, hair rings,',
    '<lora:mikasa_ackerman_v1:0.7>,hmmikasa, short hair, black eyes, scarf, emblem, belt, thigh strap, red scarf, white pants, brown jacket, long sleeves,',
    '<lora:Mirko:1>,dark skin,white hair,bunny ears,thick body,thicc,white latex,',
]
characters_nude = [
    #'<lora:midnightMHA_NAI_v2-8:1>, midnightmha, boku no hero academia, purple hair, very long hair, blue eyes, domino mask, thighhighs,nude, naked,',
    '<lora:Nero:1>,secre swallowtail, wings, thighhighs, black wings, black thighhighs, see-through, demon horns, antenna hair, white pupils, bright pupils, feathered wings,nude, naked',
    '<lora:Dawn:1>,dawn \(pokemon\), beanie, long hair, blue hair, blue eyes, hands on hips,nude,naked,',
    '<lora:Gwen:0.7>,orange hair,short hair,Gwendolyn_Tennyson, smirk, nude,naked,',
    #'<lora:gwentennyson:0.6>,gwentennyson,orange hair,thicc,thick body,short hair,nude,naked,',
    #'clipboard <lora:JOY-10:1> ,nurse joy, pokemon, blue eyes,  long hair, pink hair, nurse cap,hair rings,nude,naked,',
    '<lora:mikasa_ackerman_v1:0.7>,hmmikasa, short hair, black eyes, scarf, red scarf,nude,naked,',
    #'<lora:Mirko:1>,dark skin,white hair,bunny ears,thick body,thicc,nude,naked,',
]

n = """
(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, inaccurate eyes, extra digit, fewer digits, (extra arms:1.2),accessories,loli,muscles,muscular,cat ears,transparent clothes,wet clothes,bad hands,accessories,
"""

w = 512
h = 768 # 908
k = 12

lora_models = [
    # 'meinamix_meinaV9',
    'meinahentai_v3',
    'camelliamixNSFW_v11',
    'sakushimixFinished_v20',
    'sakushimixFinished_sakushimixFinal',
    # 'ExpMix-004',
    # 'primemix_v2',
    # 'V08_V08',
    # 'neverendingDreamNED_bakedVae',
]
lora_to_iterate = lora_models
# lora_to_iterate = [ 'meinahentai_v3' ]
total_loras = len(lora_to_iterate)

mode = 'onebyone'
# mode = 'random'

if mode == 'onebyone':
    characters = characters_nude
    custom_range = characters
    iteration_total = len(custom_range)
else:
    characters = characters_nude
    custom_range = range(k+1)
    iteration_total = k

print(f"[+] Starting:")
print(f"[+] Mode: {mode}")
print(f"[+] LoRas: {total_loras}")
print(f"[+] Characters: {len(characters)}")

for i, range_value in enumerate(custom_range):
    seed = int(random.random()*910000)
    n = i+1
    if mode == 'onebyone':
        prompt = p.replace('<character>', range_value)
    else:
        prompt = p.replace('<character>', random.choice( characters ))
    for j, lora in enumerate(lora_to_iterate):
        k = j+1
        dt = datetime.datetime.now()
        # TODO: Calculate the progress accounting for the loras as well
        print(f"[+] Seed: {seed} -> {n}/{iteration_total} ({(n/iteration_total)*100:.1f}%) | lora [{lora}]: {k}/{total_loras} | [{dt}]")
        lora_payload = {
            "override_settings": {
                'sd_model_checkpoint': lora
            }
        }
        # print(prompt + '\n')
        t1 = datetime.datetime.now()
        while True:
            try:
                output_image = send_request(
                    prompt,
                    n,
                    width=w,
                    height=h,
                    override_payload=lora_payload,
                    steps=30
                )
                data = json.loads(output_image)
                encoded_image = data["images"]
                out_name = f'{dt.year}-{dt.month}-{dt.year}_{dt.hour}-{dt.minute}-{dt.second}.png'
                with open(os.path.join(out_folder, out_name), "wb") as f:
                    f.write(base64.b64decode(encoded_image[-1]))
            except KeyboardInterrupt as e:
                print(f"[!] KeyboardInterrupt")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {str(e)}")
                continue
            break
        t2 = datetime.datetime.now()
        dt = t2-t1
    
