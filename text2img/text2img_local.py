from diffusers import DiffusionPipeline
import torch
import os

HOME = os.environ.get('HOME')
MODEL_PATH = "Github/.downloaded/stable-diffusion-webui/models/HuggingFace/meinamix_meinaV9/"
FULL_MODEL_PATH = os.path.join(HOME, MODEL_PATH)

print(f'[+] Model path: {FULL_MODEL_PATH}')

pipe = DiffusionPipeline.from_pretrained(
    FULL_MODEL_PATH,
    custom_pipeline="lpw_stable_diffusion",
    torch_dtype=torch.float32,
    cache_dir="./.cache",
)
pipe=pipe.to("cpu")


prompt = "best_quality (1girl:1.3) bow bride brown_hair closed_mouth frilled_bow frilled_hair_tubes frills (full_body:1.3) fox_ear hair_bow hair_tubes happy hood japanese_clothes kimono long_sleeves red_bow smile solo tabi uchikake white_kimono wide_sleeves cherry_blossoms"

negative_prompt = "lowres, bad_anatomy, error_body, error_hair, error_arm, error_hands, bad_hands, error_fingers, bad_fingers, missing_fingers, error_legs, bad_legs, multiple_legs, missing_legs, error_lighting, error_shadow, error_reflection, text, error, extra_digit, fewer_digits, cropped, worst_quality, low_quality, normal_quality, jpeg_artifacts, signature, watermark, username, blurry"

out = pipe.text2img(
    prompt,
    negative_prompt=negative_prompt,
    width=512, height=512,
    max_embeddings_multiples=3
).images[0]


out.save('./out.png')
