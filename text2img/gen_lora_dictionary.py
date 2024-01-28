#! /usr/bin/env python3

# Author:       Author
# Date:         August 12 2023 at 11:20:04 PM
# Description:  <>

import os
import json

config_path_root = '.'
config_path = os.path.join(config_path_root, 'config.json')

HOME = os.environ.get('HOME')
path_to_lora = os.path.join(HOME, 'Github/.downloaded/stable-diffusion-webui/models/Lora')

def loadDefaultConfig(path_to_lora):
    lora_models = os.listdir(path_to_lora)
    lora_configs = {}

    for lora in lora_models:
        lora_configs[lora] = {
            'description': lora,
            'activator': 'tbd',
            'prompts': {},
        }

    return lora_configs

if os.path.isfile(config_path):
    print(f'[+] Lora models path: {path_to_lora}')
    print(f'[+] Config path: {config_path}')

    # load lora config
    with open(config_path) as f:
        data = f.read()
    lora_json = json.loads(data)
    lora_default_json = loadDefaultConfig(path_to_lora)

    # lora config status
    ## model count
    print(f"[+] Lora models: {len(lora_json)}")
    ## deleted/new models
    configured_models = list( lora_json.keys() )
    current_models = list( lora_default_json.keys() )
    new_models = current_models.copy()
    deleted_models = []

    for model_name in configured_models:
        if model_name not in current_models:
            deleted_models.append(model_name)
        else:
            new_models.remove(model_name)
    print(f'[+] New models: {len(new_models)}')
    print(f'[+] Deleted models: {len(deleted_models)}')

    ## no promt models
    for model_name, config in lora_json.items():
        description = config['description']
        prompts = config['prompts']
        promt_count = len(prompts)
        # if promt_count == 0:
        #     print(f'\t[!] {model_name}: {promt_count}')
else:
    lora_configs = loadDefaultConfig(path_to_lora)
    with open(config_path, 'w') as f:
        f.write( json.dumps(lora_configs) )
