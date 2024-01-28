import os
import sys
import json
import pprint
import random
import base64
import datetime
from io import BytesIO

import datetime

## Standard for anime
# base_prompt = "((masterpiece)),(((best quality))),highly detailed,illustration,sharp edges,(ultra highres:1),1girl,cute face, perfect face,cowboy shot,full body,(closed mouth):1,3,looking at viewer,"

## Pixar
#base_prompt = "style of Tsutomu Nihei,(incredibly absurdres, (high resolution:1.18), intricate detail, (masterpiece:1.1), (highest quality:1.1), absurdres),(1girl, solo, detailed eyes),"
#base_prompt = "soothing tones,muted colors,high contrast,(natural skin texture, hyperrealism, soft light, sharp),(close-up shot) artistic photoshoot,"
#"movie trailer,cinematic,screencap,still shot,true perception,comfortable,"

## Semi realistic
#base_prompt = "(masterpiece), trending on artstation, ultra high res, (sharp focus), (photorealistic:1.4),(8k, RAW photo, best quality, masterpiece:1.2), ultra-detailed, (AV idol), perfect detail,1girl,best quality,cute face, perfect face,cowboy shot,full body,(closed mouth):1,3,looking at viewer,((nsfw)),"

## Semi realistic
#base_prompt = "(RAW photo:1.2), (photorealistic:1.4),(intricate details:1.2),(masterpiece:1.3),(best quality:1.4), (ultra highres:1.2), cinema light, ultra high res, ultra realistic, (detailed eyes),(detailed facial features),pink nipples, HDR, 8k resolution, (looking at viewer),POV, nsfw, thick, thick body, (extreme detailed illustration), light detailed eyes, 1girl,solo, cute, smile, happy, innocent,((nude,naked,completely nude)),breasts out,"

## High detail realistic clothes off
base_prompt = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4), (ultra highres:1.2), cinema light, ultra high res, ultra realistic, (detailed eyes),(detailed facial features),pink nipples, HDR, 8k resolution, (looking at viewer),POV, nsfw, thick, thick body, (extreme detailed illustration), light detailed eyes, 1girl,solo, cute, smile, happy, innocent,((nude,naked,completely nude)),breasts out,"

## High detail realistic clothes on
# base_prompt = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4), (ultra highres:1.2), cinema light, ultra high res, ultra realistic, (detailed eyes),(detailed facial features), HDR, 8k resolution, (looking at viewer),POV,(extreme detailed illustration), light detailed eyes, 1girl,solo,"

#base_prompt = "(intricate details:1.2),(masterpiece:1.3),(best quality:1.4), (ultra highres:1.2), cinema light, ultra high res, ultra realistic, (detailed eyes),(detailed facial features), HDR, 8k resolution, (looking at viewer),(extreme detailed illustration), light detailed eyes, 1girl,solo,"

characters = {
    "yuki-jujutsu": {
        "base":  {
            "style1": "<lora:YukiTsukumo:0.9>, YukiTsukumo, blonde hair, long hair, (hair split in half):1.3, brown eyes, smile, large breast, thick body, mature woman,clear forehead,big forehead,",
        },
        "clothes": {
            "base1": "black shirt, bare shoulders, belt, jeans, sleeveless, turtleneck, sleeveless turtleneck,",
            "base2": "black shirt, bare shoulders, cargo pants, green pants, sleeveless, turtleneck, sleeveless turtleneck,",
        },
    },
    "Fern": {
        "base":  {
            "style1": "<lora:Fern:0.9>,FernFrieren, very long hair, purple hair, hair ornament, purple eyes, (purple pupils), large breasts, huge breasts,expressionless,serious,thick body,",
        },
        "clothes": {
            "base1": "white dress, black robe",
        },
    },
    "nami": {
        "base":  {
            "style1": "<lora:nami_(one_piece)_v1:0.75>,nami (one piece),orange hair,brown eyes,thick body,small waist,huge breasts,tattoo,arm tattoo,",
        },
        "clothes": {
            "pre-time-skip": "short hair, cleavage, striped shirt, white shirt, short sleeves, bracelet, miniskirt, yellow skirt",
            "post-time-skip": "long hair,earrings, bare shoulders, shoulder tattoo, cleavage, bikini top only, striped bikini, green bikini, bracelet, midriff, belt, jeans, denim.",
            "mink": "long hair,(hair ornament:1.1), brown eyes, (jewelry:1.1), earrings, bare shoulders, shoulder tattoo, cleavage, blue dress, sleeveless, bracelet, pelvic curtain, side slit",
            "wano": "long hair,low ponytail, hair bow, blue bow, brown eyes, collarbone, cleavage, short kimono, blue kimono, sleeveless, bare arms, bracelet, sash, obi",
        },
    },
    "boa-hancock": {
        "base":  {
            "style1": "<lora:boa_hancock_v3:0.8>,hancock1, boa hancock, large breasts, huge breasts, mature woman, long hair, black hair, earrings, jewelry, cape,thick body,small waist,",
        },
        "clothes": {
            "base1": "epaulettes, crop top, cleavage, red dress, red skirt, long sleeves, side slit",
        },
    },
    "nico-robin": {
        "base":  {
            "style1": "<lora:nico_robin_v1:0.8>,nico robin, long hair, black hair,huge breasts,thick body,small waist,hair slicked back, eyewear on head, sunglasses, blue eyes, collarbone,",
            # "style2": "<lora:nico_robin_v1:0.8>,nico robin, long hair, black hair,huge breasts,thick body,small waist,black hair,tan skin,brunette,brown skin,leather jacket,mini skirt,unzipped,",
        },
        "clothes": {
            # "pre-time-skip": "bangs, blue eyes, cleavage, black dress, black jacket, long sleeves, partially unzipped, black thighhighs",
            "post-time-skip": "cleavage, blue jacket, cropped jacket, partially unzipped, short sleeves, midriff, sarong, print sarong",
            # "mink": "bucket hat, white headwear, eyewear on headwear, sunglasses, forehead, blue eyes, collarbone, bare shoulders, cleavage, blue dress, short dress, sleeveless",
        },
    },
    "tsunade": {
        "base":  {
            "style1": "<lora:tsunade by Goofy Ai:0.75>, tsunade, blonde, medium hair, jewelry, large breasts, mature female, huge breasts, closed mouth, smile,",
        },
        "clothes": {
            "base1": "japanese clothes, collarbone, garter straps, cleavage, black thighhighs, black skirt, necklace, green coat,",
        },
    },
    "frieren": {
        "base":  {
            "style1": "<lora:frieren:0.75>, frieren, pointy ears, long hair, twintails, parted bangs, jewelry, elf, earrings,",
        },
        "clothes": {
            "base1": "capelet, white capelet, long sleeves, white dress, belt, thighs, black thighs,",
        },
    },
    "kohaku-dr-stone": {
        "base":  {
            "style1": "<lora:kohaku:0.7>,kohaku,short hair,blonde,blue eyes,spiky hair,fur trim, ((high ponytail)),hair ornament,bangs,hair between eyes,cleavage,collarbone,rope,necklace,white choker,thick body, athletic, navel,",
        },
        "clothes": {
            "blue-dress": "midriff,((blue dress)), mini skirt, open clothes,tube top,cutoffs,sideboob,downblouse",
            # "pink-dress": "midriff,((pink dress)), mini skirt, open clothes,tube top,cutoffs,sideboob,downblouse",
        },
    },
    "humura-dr-stone": {
        "base":  {
            "style1": "<lora:humura:0.7>,hamura,pink eyes,pink hair,red lips,closed mouth,ponytail,high pony tail,thick body, athletic,navel,:o,v-shaped eyebrows",
        },
        "clothes": {
            "base": "pink dress,thigh dress,fur collar,",
        },
    },
    "ramona": {
        "base":  {
            "style1": "<lora:Ramona_Flowers:0.65>,Ramona_Flowers,short hair,black eyes,solo, medium breasts,smile,",
        },
        "clothes": {
            "base": "goggles on head, hoodie,grey jacket,long sleeves,shoulder bag,star (symbol),belt,denim skirt,purple pantyhose,",
            "adult": "black choker,blue shirt, long sleeves,brown belt,shouler bag,white skirt,purple pantyhose, winter, snow,night sky,",
        },
    },
    "anna-shaman-king": {
        "base":  {
            "band": "<lora:kyouyama_anna_v1:0.45>,kaa,yellow hair, yellow eyes, big eyes,round eyes, bead necklace, sleeveless, bracelet, red bandana,",
            # "band": "<lora:kyouyama_anna_v1:0.55>,kaa,yellow hair, yellow eyes, bead necklace, sleeveless, bracelet, red bandana,",
            # "scarf": "<lora:kyouyama_anna_v1:0.75>,kaa,yellow hair, yellow eyes, bead necklace, sleeveless, bracelet, red scarf,",
        },
        "clothes": {
            "base": "black dress,bare shoulders,",
        },
    },
#    "mitsuri": {
#        "base":  {
#            "style1": "<lora:mitsuri_demon_slayer:0.45>,mitsuri,pink hair,green hair,twin tails,long hair,hair gradient,huge breasts,breasts out,green eyes,green tights,happy,smile,",
#        },
#        "clothes": {
#            "base": "uniform,demon slayer uniform,white  jacket,",
#        },
#    },
    "starfire": {
        "base":  {
            "style1": "<lora:StarfireTT:0.8>,starfire, red hair, long hair, green eyes,round eyebrows, orange skin,((thick body, small waist, huge breasts)):1.3,gray collar,green pearl,grey bracelets,",
            # "style1": "<lora:StarfireTT:0.85>,starfire, red hair, long hair, green eyes,round eyebrows, orange skin,thick body, huge breasts,gray collar,green pearl,grey bracelets,",
        },
        "clothes": {
            "base": "thigh boots,crop top, midriff,purple clothes,,  miniskirt, thighhighs,grey belt,",
        },
    },
    "jenny-pokemon-police": {
        "base":  {
            "style1": "<lora:officerjenny-nvwls-v1:0.75>,pkmnJenny, blue hat, white gloves, mature woman, large breasts,spiky hair,teal hair,mini skirt,yellow eyes,smile,happy",
        },
        "clothes": {
            "base": "police uniform, blue shirt, short sleeves, belt, pencil skirt,",
        },
    },
    "rukia": {
        "base":  {
            "style1": "<lora:rukia-nvwls-v1:0.68>,kuchikirukia,black hair, black eyes,short hair, hair bang,small breasts,mature woman,((serious,expresionless))",
        },
        "clothes": {
            "style1": "black robes,white sash,",
            "style2": "bowtie, white shirt, short sleeves, grey skirt, school uniform,red ribbon",
            "style3": "bowtie, grey blazer, grey skirt, school,red ribbon,",
        },
    },
    "yoko": {
        "base":  {
            "style1": "<lora:YokoLi:0.6>,huge breasts,thick body, gloves,  hair ornament, skull ornament, long hair, ponytail, red hair, scarf,  smile, yellow eyes, yoko littner, yokoli,black gloves,",
        },
        "clothes": {
            "base": "bikini, flame print, blue shorts,white belt,  pink tights,",
        },
    },
    "chika": {
        "base":  {
            "style1": "<lora:chara_Kaguya-samaWaKokurasetai_FujiwaraChika_v1:0.5>, fujiwara chika (kaguya-sama),smilepink hair, blue eyes, long hair,pink hair,thick body,huge breasts,red ribbon,",
        },
        "clothes": {
            "base": "school uniform, black dress, hair bow, black bow,",
        },
    },
    "kaguya-sama": {
        "base":  {
            "style1": "<lora:chara_Kaguya-samaWaKokurasetai_ShinomiyaKaguya_v1:0.5>, shinomiya kaguya,light smile,black hair, red eyes, short hair, folded ponytail, hair ribbon,small waist,thick body,((huge breasts)):1.3, mature woman,",
        },
        "clothes": {
            "base": "school uniform, black dress, mini skirt, long sleeves, red ribbon,",
        },
    },
    "maki-zenin": {
        "base":  {
            "pony tail 1": "<lora:zenin_maki:0.55>,zenin_maki,((thick body,huge breasts, mature woman)),glasses,1girl,solo,ponytail,straight bangs,sidelocks,green hair,female focus,",
            # "pony tail 2": "<lora:zenin_maki:0.55>,zenin_maki,thick body,glasses,1girl,solo,ponytail,straight bangs,sidelocks,green hair,female focus,large breasts,",
        },
        "clothes": {
            #"base": "purple jacket, white shorts, black pantyhose",
            "uniform": "uniform, mini skirt,jacket,((black uniform, black jacket)),black tights,",
            #"latex": "purple translucent bunnysuit, see through, heels, standing,",
        },
    },
    "ulti": {
        "base":  {
            "long hair": "<lora:UltiOP_NAI_v1-1:0.75>,mask,UltiOP,onepieceanime,thick body,large breasts,multicolored hair,blue hair,pink hair,bangs, long hair,horns,angry,",
        },
        "clothes": {
            "base": "blue skirt, high-waist skirt, white shirt,",
        },
    },
    "korra": {
        "base":  {
            "long hair": "<lora:thelegendofkorra_korra:0.7>, solo, 1girl, korra, ((dark skin, dark-skinned female)), smile, closed mouth, ponytail, hair tubes, huge breasts,",
            # "long hair thick body": "<lora:thelegendofkorra_korra:0.7>, solo, 1girl, korra, ((dark skin, dark-skinned female)), smile, closed mouth, ponytail, hair tubes, thick body, huge breasts, mature woman,",
            # "short hair": "<lora:thelegendofkorra_korra:0.8>, solo, 1girl, korra, ((dark skin, dark-skinned female)), smile, closed mouth, short hair, bangs, huge breasts,",
        },
        "clothes": {
            "base": "sleeveless,blue shirt, bare shoulders,",
        },
    },
    "katara": {
        "base":  {
            "long hair": "<lora:katara:0.75> ,katara, dark skin, dark-skinned female,long hair, brown hair, dark hair, blue eyes, blue hair ornaments,thick body,huge breasts,",
        },
        "clothes": {
            "base": "winter clothes,blue clothes,pelvic curtain,black thighs,",
        },
    },
    "toph": {
        "base":  {
            "short hair": "<lora:toph_bei_fong:0.75> ,toph_bei_fong, ((white eyes, blind)),short hair,black hair, hair bun,green hair band,small waist,huge breasts,short height,",
        },
        "clothes": {
            "base": "pelvic curtain,green clothes,",
        },
    },
    "power": {
        "base":  {
            "long hair": "<lora:power_chainsawman:0.55>, power_chainsawmanl,orange eyes,symbol-shaped pupils,cross-shaped pupils,((light pink hair)),"
                         "blonde hair, long hair, hair between eyes, horns, red horns, demon horns, (sharp teeth), ((thighs)), evil smile",
        },
        "clothes": {
            "base": "jeans,((blue jacket)),white shirt,black sneakers, sneakers,",
        },
    },
    "bulma": {
        "base":  {
            "young": "<lora:bulma_9:0.7>,dragon ball, blmpony, aqua hair, hair ribbon, braided ponytail, belt, scarf, brown gloves,",
            "mid": "<lora:bulma_9:0.7>,dragon ball, blmmid, aqua hair, medium hair, blunt bangs, red hairband,",
            # "adult": "<lora:bulma_9:0.7>,dragon ball, blmshort, aqua hair, very short hair, earrings, jewelry, yellow scarf,",
        },
        "clothes": {
            "young": "pink shirt,pink skirt, clothes writing",
            "mid": "black tighs,yellow clothes, yellow jacket, yellow skirt,namek,",
            "adult": "red dress, short dress, sleeveless,",
        },
    },
    "milk": {
        "base":  {
            "young": "dragon ball, aachichi, long hair, helmet, pink headwear, black eyes, large breasts, huge breasts, mature, milf, shoulder armor, green cape, pink gloves, navel, <lora:chi-chi_v1:0.7>,",
            "mid": "dragon ball, bbchichi, (low ponytail:1.1), black eyes, sleeveless, wristband, sash, <lora:chi-chi_v1:0.7>, huge breasts, milf,",
            #"adult": "dragon ball, bbchichi, single hair bun, hair bun, blunt bangs, sidelocks, black eyes,earrings,<lora:chi-chi_v1:0.7>,huge breatss, milf,angry,",
        },
        "clothes": {
            "young": "armor,bikini,groin",
            "mid": "boots,pelvic curtain,bare shoulders,purple dress,",
            # "adult": "orange neckerchief, orange scarf, bracelet,boots,pelvic curtain,jewellery,yellow dress,blue pants",
        },
    },
    "shizukazom100": {
        "base":  {
            # navel, nude, naked, breasts, out, pussy, camel toe,
            "short hair": "<lora:shizukazom100 v3:0.7>, intricate details, shizukazom100, 1girl, short hair, dark purple hair, bangs, hair ornament, hairclip, pink eyes, white pupils, medium breasts,",
        },
        "clothes": {
            "base": "collarbone, blue jacket, shorts,",
        },
    },
    'Dawn': {
        'base': {
            'prompt': '<lora:Dawn:0.8>,dawn \\(pokemon\\), beanie, long hair, blue hair, blue eyes, hands on hips, mature, huge breasts, thick body,'
        },
        'clothes': {
            'base': 'bare shoulders,black and pink dress, scarf,'
        }
    },
    'Gwen': {
        'base': {
            'prompt': '<lora:Gwen:0.7>,((orange hair,short hair)),green eyes,Gwendolyn_Tennyson, smirk,hair clip,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'white pants,blue shirt,blue sleeves,cat logo,long sleeves,'
        }
    },
    'Jabami Yumeko': {
        'base': {
            'prompt': '<lora:Kizuki - Kakegurui Jabami Yumeko LoRA:0.75>,long hair,black hair,black eyes,blushing,black tights,'
        },
        'clothes': {
            'base': 'red jacket,uniform,mini skirt,black tighs,'
        }
    },
    'Kochou_Shinobu': {
        'base': {
            'prompt': '<lora:Kochou_Shinobu:0.75>,short hair,bangs,black hair,dark hair,butterfly,thicc, thick body,front view,'
        },
        'clothes': {
            'base': 'uniform,black uniform,demon corps uniform,'
        }
    },
    'Kugisaki_lora': {
        'base': {
            'prompt': '<lora:Kugisaki_lora:0.9>,short hair,brown hair,bangs,thick body,thicc,huge breasts,'
        }, 'clothes': {
            'base': 'uniform,mini skirt,thick tighs,brown tights,crop top,'
        }
    },
    'Misty': {
        'base': {
            'prompt': '<lora:Misty:0.75>,short hair,pony tail,orange hair,blushing,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'shorts,((yellow shirt)),red strips,bare shoulders'
        }
    },
    'Nero': {
        'base': {
            'prompt': '<lora:Nero:0.8>, nero, short hair, black hair, black eyes, black feathers, sexy, thick body, huge breasts,serious,black wings,'
        },
        'clothes': {
            'base': 'dark clothes,black dress,'
        }
    },
    'PeronaLORA': {
        'base': {
            'prompt': '<lora:PeronaLORA:0.85>,long hair,pink hair,twin tails,round eyes,black eyes,makeup,dirty makeup,huge breasts,thick body,'
        },
        'clothes': {
            'base': 'black dress, pink details, halloween,striped tights,'
        }
    },
    'Sarada': {
        'base': {
            'prompt': '<lora:Sarada:0.8>,ninja,head band,glasses,dark hair,short hair,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'white shorts,red shirt,bare shoulders,head band, black sleeves,'
        }
    },
    'Ochakodim8': {
        'base': {
            'prompt': '<lora:Ochakodim8:0.75>,ochako,short hair, brown hair, brown eyes, blush, pink blush,sexy, thick body, huge breasts,smile,'
        },
        'clothes': {
            'ua': 'grey jacket, green skirt, mini skirt, white shirt, red tie,UA uniform,',
            'casual': 'mini skirt,blue skirt,cream sweater,red ribbon,',
        }
    },
    'TogaHimikoLoRA': {
        'base': {
            'prompt': '<lora:TogaHimikoLoRA:0.75>, toga, yellow eyes,twin tails, short hair, thick body, huge breasts, fangs, psycho, crazy,'
        },
        'clothes': {
            'ua': 'grey jacket, green skirt, mini skirt, white shirt, red tie,UA uniform,',
            'casual': 'mini skirt,blue skirt,cream sweater,red ribbon,',
        }
    },
    'Utahime': {
        'base': {
            'prompt': '<lora:Utahime:0.75>, utahime, ((face scar)), scar:1.2, pony tail, medium hair, dark purple hair, black eyes, sexy, thick body, huge breasts, mature,serious, hair ornament, red ribbon,'
        },
        'clothes': {
            'base': 'long skirt,red skirt, kimono,'
        }
    },
    'dark_magician_girl': {
        'base': {
            'prompt': "<lora:dark_magician_girl_offset:0.8>,dark magician girl, blonde hair, blue footwear, blue headwear, breasts, duel monster, hat, hexagram, large breasts, long hair,"
                      "pentacle, pentagram, solo, staff, wand, wizard hat, yu-gi-oh!,"
        },
        'clothes': {
            'base': 'slut custome,magical custome,mini skirt,neckline,'
        }
    },
    'jessie': {
        'base': {
            'prompt': "<lora:jessie v2 by goofy ai:0.75>, jessie pokemon, black gloves, elbow gloves, hair slicked back, long hair, very long hair, purple hair,jewelry,"
                      "navel, thighhighs,thick body, huge breasts, milf,earrings,blue eyes,"
        },
        'clothes': {
            'base': 'team rocket, white clothes, mini skirt, crop top, R,'
        }
    },
    'jolynejojo': {
        'base': {
            'prompt': '<lora:jolynejojo:0.75>,short hair,green hair,yellow hair,twin tails,hair buns,huge breasts'
            #'prompt': '<lora:jolynejojo:0.9>,short hair,green hair,yellow hair,twin tails,hair buns,huge breasts'
        },
        'clothes': {
            'base': 'shorts,shirt,latex,bare shoulders,(clothes,green,black,green)'
        }
    },
    'kagami': {
        'base': {
            'prompt': '<lora:kagami:0.5>,dark hair,short hair,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'white jacket,red skirt, mini skirt, black tighs,'
        }
        # nude:1.2,naked:1.3,nsfw:1.3,
    },
    'marinette': {
        'base': {
            'prompt': '<lora:marinette:0.7>,dark hair,short hair,twin tails,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'jeans,white shirt,black jacket,chinese ornamets,'
        }
        # nude:1.2,naked:1.3,
    },
    'mikasa_ackerman': {
        'base': {
            'prompt': '<lora:mikasa_ackerman_v1:1>,hmmikasa, black hair, short hair, black eyes, scarf, red scarf, huge breasts, thick body,'
        },
        'clothes': {
            'base': 'tactic equipment,uniform,white clothes, brown boots,'
        }
    },
    'neferpitou': {
        'base': {
            'prompt': '<lora:neferpitou:0.85>,short hair,white hair,bangs,cat ears,pale skin,red eyes,huge breasts'
        },
        'clothes': {
            'base': 'shorts, orange shorts,blue jacket,'
        }
    },
    'onepieceYamato': {
        'base': {
            'prompt': '<lora:onepieceYamatoLoraBy_12Epoch364dim:0.9>,long hair,pony tail,horns,green hair,white hair,blushing,huge breasts,'
        },
        'clothes': {
            'base': 'kimono,white and red clothes,bare shouders,'
        }
    },
    'senjougahara_hitagi': {
        'base': {
            'prompt': '<lora:senjougahara_hitagi_v2:0.8>,long hair, bangs,purple hair,purple eyes,'
        },
        'clothes': {
            'base': 'mini skirt,pink shirt,long sleeves,black tighs,'
        }
    },
    'tatsumakiselect': {
        'base': {
            'prompt': '<lora:tatsumakiselect:0.85>,tatsumaki,floating hair,short hair,green hair,bangs,green eyes,nude,naked,thick body, thicc, huge breasts,'
        },
        'clothes': {
            'base': 'black dress,pelvic curtain,'
        }
    },
    'videl': {
        'base': {
            'prompt': '<lora:videl_v3:0.75>,short hair,black hair,twin tails,black eyes,blushing,huge breasts,'
        },
        'clothes': {
            'base': 'shorts,black shorts,white shirt,star pin,'
        }
    },
    'yor': {
        'base': {
            'prompt': '<lora:yor:0.75>,long hair,black hair,head band,earrings,red eyes,round eyes,big eyes,shy,ashamed,blush'
        },
        'clothes': {
            'home': 'red sweater,black tights,',
            'assassin': 'assasin uniform,black dress,hair ornaments,black sleeves,bare shoulders'
        }
    }
}

print("[+] Available characters:")
for character in characters.keys():
    print(f"    '{character}',")
print()

themes = [
    # base
    # 'squatting,spread legs,pussy hair,bush,front view,camel toe,',
    "((completely nude))",
    "((school uniform)), (mini skirt):1.2,",

    ## sometimes ok
    '<lora:public_v3.0-locon:1>,public, photographers,streets,',
    '<lora:aftersex:0.8>,nude,naked,on bed,lying,spread legs,cum,blushing,',
    #'<lora:folded_anal_sex:1.2>,folded anal sex,teeth, sweat, @_@, large breasts, open mouth, upper teeth only, ahoge, sex, pussy, penis, ((completely naked, nude)), indoors, 1boy:1.2, penis:1.2, penis in ass, blush, hetero,anal, tongue, smile, full nelson, testicles,<lora:blacked_v4.23:0.4>,',
    #'<lora:public_v3.0-locon:1>,public, photographers,streets, <lora:add_detail:1.2>,',
    #"<lora:suspendedcongressms:1.4>,((sex)),spread legs,1boy,1girl,moaning,sex,1penis,insertion,",
    #'<lora:undressing_panties_v0.1:1.4>, panty pull, undressing, self pull,',
    #'<lora:multiple_insertions_v0.2:0.8>,spread legs,anal,(anal_object_insertion:1.2),Anal Dildo,Dildo,multiple insertions,',

    ## good with most models

    "((cute face, perfect face)):1.2,<lora:pose mirror:1>, ass,  looking at viewer, ((mirror, reflection)),  sitting, (indoors, bathroom:1.3),",
    "((cute face, perfect face)):1.2,<lora:pose mirror:1.45>, ass,  looking at viewer, ((mirror, reflection)),  sitting, (indoors, bathroom:1.3),",

    "<lora:pose glass:1>, 1girl, against glass, huge breasts, sex from behind, overflow. dripping cum, moaning, breasts on glass, hand up, cum,panties, train interior,",
    "<lora:pose glass:1>, 1girl, against glass, huge breasts, sex from behind, overflow, breasts on glass, hand up, doggystyle, grabbing from behind, thigh sex,penis, cum,panties, train interior,kiss, ",

    'ass, looking back, spread ass ,SpreadAssMS ,<lora:SpreadAssMS:0.75>,anal gap,anus,',
    '1girl,anus, pussy, sidewayassms,spread pussy, <lora:SidewayAssMS:0.75>,anal gap,sexy legs,',
    "1girl,<lora:hentai ass  up:0.8>,ass focus, from behind, spread anus, cum in ass, cumdrip,looking back,anal, anal gap, open anus,",

    "<lora:female ejaculation6:0.8>,female ejaculation,female orgasm with sex, pussy juice ,ahegao, steaming body, full-face blush, fingering, masturbation,",
    "<lora:female ejaculation6:1.1>,female ejaculation,female orgasm,spread legs, pussy, pussy juice ,ahegao, steaming body, full-face blush,fingering, schlick,",
    "<lora:pose standingpussy:0.9> standing, standing on one leg, leg up,1girl,embarrassed, blush,(((completely nude))),(well defined leg):1.3,",

    ## TEST WITH DIFFERENT WEIGHTS
    # "<lora:folded_anal:0.8>,solo folded anal, anal gape, open ass, anus, pussy juice,pussy, clitoris, ass, urethra, folded, female pubic hair, lying, anal,((knees to chest,legs up)),huge ass,shoes:1.3,",
    # "<lora:folded_anal:1>,solo folded anal, anal gape, open ass, anus, pussy juice,pussy, clitoris, ass, urethra, folded, female pubic hair, lying, anal,((knees to chest,legs up)),huge ass,shoes:1.3,",
    # "1thick black penis, missionary anal, from above, very soft large breasts, breasts apart, spreading legs, legs up,  <lora:PovMissionaryAnal-v6:1.1>, large insertion, hands behind head, embarrassed, ((completely nude, naked)),feet:1.3,",
    ## TEST WITH DIFFERENT WEIGHTS

    ## bad for some models
    #'<lora:GilElvgren:0.7>,woman posing for a picture,sexy pose,80s,', # 0.8
    #"perfect lighting, 1girl, ((1boy, 1dick, black penis)), lickingoral, licking penis, cum on female face, saliva, <lora:LickingOralLoRA:1.4>,breasts out,",
    #'1girl,<lora:pose jinjuli:1.4>,sex, huge penis,vaginal object insertion, vaginal, imminent vaginal, interracial, imminent penetration, <lora:blacked_v4.23:0.4>',
    #"multiple views, <lora:concept-pov-multiple_views-v1:0.45>,sex from behind, fellatio, missionary position, multiple views, pov, Beautiful character design, perfect eyes, perfect face,perfect eyes,",
]

themes = [
    #"((completely nude, naked)), <lora:female ejaculation6:1.2>,female ejaculation,female orgasm,spread legs, pussy, pussy juice ,ahegao, steaming body, full-face blush,fingering, schlick,",
    # base
    "((black suit,tie)),sexy pose, standing,skirt,office lady,",
    "((black suit,tie)),sexy pose, skirt,office lady, open legs, squatting,spreading pussy,presenting pussy,breasts out,nsfw:1.3,",
    #"((completely nude)),squatting,spread legs,pussy hair,bush,front view,camel toe,",
    #"((completely nude))",
    "((school uniform)), (mini skirt):1.2,",
    "((school uniform)), (mini skirt):1.2,open legs,squatting,spreading pussy,presenting pussy,breasts out,nsfw:1.3,",
    'squatting,spread legs,<lora:FemBush-V4:0.35>,pussy hair,bush,hairy pussy,bare,bare pussy, no panties,closed mouth,((nude,naked)),',

    ## sometimes ok
    '<lora:aftersex:0.8>,nude,naked,on bed,lying,spread legs,cum,blushing,',
    '<lora:undressing_panties_v0.1:1.4>, panty pull, undressing, self pull,',

    ## good with most models
    "standing, <lora:fishnet:0.7>, (fishnets:1.2)",
    "<lora:fishnet:0.7>, (fishnets:1.2),squatting, spread legs, presenting pussy,",
    "<lora:pose glass:1>, 1girl, against glass, huge breasts, sex from behind, overflow. dripping cum, moaning, breasts on glass, hand up, cum,panties, train interior,",

    'ass, looking back, spread ass ,SpreadAssMS ,<lora:SpreadAssMS:0.75>,anal gap,anus,',
    "1girl,<lora:hentai ass  up:0.8>,ass focus, from behind, spread anus, cum in ass, cumdrip,looking back,anal, anal gap, open anus,",

    '<lora:multiple_insertions_v0.2:0.8>,spread legs,anal,(anal_object_insertion:1.2),Anal Dildo,Dildo,multiple insertions,',

]

themes = [
    #"",
    #"((nude, naked, completely nude)),",

    #"((school uniform)), (mini skirt):1.2,",
    "((school uniform)), (mini skirt):1.2,squatting,spread legs,presenting pussy,pussy,bare pussy,bush,pantyless,",
    #"nurse,nurse uniform,white clothes red cross,head band,sexy,",
    "nurse,nurse uniform,white clothes, red cross,head band,sexy,((sitting)),spread legs,pussy,bare pussy,bush,presenting pussy,((front view))",
    #"teacher,teacher uniform,black tighs,tie,office lady,sexy,",
    "teacher,teacher uniform,black tighs,tie,office lady,sexy,((sitting, closed legs)),bare legs, teasing,",
    #"police,police uniform,leather skirt, mini skirt,black tighs,head band,sexy,",
    "police,police uniform,leather skirt, mini skirt,black tighs,head band,sexy,squatting,spread legs, pantyless,pussy, bare pussy,bush,presenting pussy,",

    #'((nude, naked, completely nude)),<lora:female ejaculation6:1.2>,thick body,mature,female ejaculation,female orgasm,spread legs,pussy,pussy juice,ahegao,steaming body,full-face blush,fingering,schlick,'
    #'((nude, naked, completely nude)),squatting,spread legs,<lora:FemBush-V4:0.35>,pussy hair,bush,hairy pussy,bare,camel toe,',
]

themes_v08 = [ # steps:32,hires:15(x3),steps:15,w:240,h:360 | steps:32,hires:15(x3),steps:20,w:240,h:360
    #"((school uniform)),squatting,spread legs,presenting pussy,pussy,bush,((front view)),hidden hands,",
    #"((maid, maiden)),hair band,squatting,spread legs,presenting pussy,pussy,bare pussy,bush,dripping cum,((hands behind back)):1.2,",
    #"nurse,nurse uniform,((white clothes, white uniform)):1.2,red cross,head band,squatting,spread legs,pussy,bush,presenting pussy,dripping cum,hidden hands,",
    #"teacher,teacher uniform,black tighs,tie,office lady,sexy,squatting,bare legs, teasing,presenting pussy,",
    #"police,police uniform,leather skirt, mini skirt,black tighs,head band,sexy,squatting,spread legs, pantyless,pussy, bare pussy,bush,presenting pussy,",
    "((portrait)):1.2,upper body,clothes,",
    "sexy pose, ((nude, naked, completely nude)),",
]


themes_demo = [
    "<lora:glory_wall:1>, glory wall, photo(object), poster of girl, wood divider, ass, bent over, from behind, anal gape, open anus, dripping cum, facing wall, wall, pov ass, stuck in wall, cut in half, glory hole, poster above ass, facing ass, pussy, anus, wet pussy, torso facing viewer, stuck in hole in wall, wood paneling, centered, beautiful face",
    "<lora:multiple_penises_v0.4:1.2>,(1girl, kneeling, arms behind back, happy, joyful), (solo focus, focus on face, from above, uncensored:1.3), ejaculation, shooting cum, multiple penises, multiple boys, (boys have huge penises, penis tips:1.1), (ejaculating, facial, bukkake, cum, cum on face:1.2),((nude, naked, completely nude)),small nipples,",
    "<lora:multiple_penises_v0.4:1.2>,(1girl, kneeling, arms behind back, happy, joyful), (solo focus, focus on face, from above, uncensored:1.3), ejaculation, shooting cum, multiple penises, multiple boys, (boys have huge penises, penis tips:1.1), (closed eyes):1.2, (ejaculating, facial, bukkake, cum, cum on face:1.2),((nude, naked, completely nude)),small nipples,",
    #"<lora:fellatiogesture:1.4>,1girl, open mouth, tongue, solo, looking at viewer, one hand, tongue out, fellatio gesture, oral invitation,",
    #"<lora:fellatiogesture:1.2>,open mouth, tongue, solo, looking at viewer, one hand, tongue out, fellatio gesture, oral invitation",
    "<lora:female pubic hair3:1>,((nude, naked, completely nude)),cute,pubic hair,",
    #"<lora:female pubic hair3:1>,((nude, naked, completely nude)),pubic hair,(from_behind),sweat,(ass_focus:1.2), covered anal,curvy ass,curvy legs, (hip focus), (ass shake), (leaning over:1.3),",
    "<lora:Pose_ClothesLift:1>,1girl, shirt lift, undressing, surprised, doorway, huge breasts, thighs, looking at viewer, side braid, panty pull, no panties",
    "<lora:skirt lift pov by Goofy Ai:1>,huge breasts,skirt lift pov,lifted by self,from below,panties,cameltoe,depth of field,",
    "<lora:skirt lift pov by Goofy Ai:0.85>, skirt lift pov,1girl,solo, large breasts, horny, steaming body,heavy breathing,looking down, mature female,((nude, no panties, bare pussy)), cumdrip, excessive cum, female pubic hair,",
    "<lora:fishnet:0.7>, (fishnets:1.2),squatting, spread legs, presenting pussy,((happy,joyful,seductive smile))",
]

themes_vanilla = [
    #'looking at viewer, POV,(from below:1.2), gaping pussy, cum dripping from pussy, cum, (spread legs:0.7), erected nipples, pubic hair, pussy juice, perfect face, (shiny skin), silky skin, (horny:1.2), blush, (steam), sweat, body steam, ass focus, cleavage, sexy pose, standing,',
    #'(pantyhose):1.2, looking at viewer, POV,(from below:1.3), gaping pussy, cum dripping from pussy, cum, (spread legs:0.7), erected nipples, pubic hair, pussy juice, perfect face, (shiny skin), silky skin, (horny:1.2), blush, (steam), sweat, body steam, ass focus, cleavage, sexy pose, standing,',
    '(pantyhose):1.2, looking at viewer, POV,from below, gaping pussy, cum dripping from pussy, cum, (spread legs:0.7), pubic hair, pussy juice, (shiny skin), silky skin, (horny:1.2), blush, (steam), sweat, body steam, ass focus, cleavage, sexy pose, standing,',
    '(pantyhose):1.2, sexy pose, standing, leaning forward, ((shy, blushing, steam,sweat,naked)),',
    # '1girl, sitting, on toilet, ((bondage, rope)), black thighhighs, no panties, ((torn clothes)), two side up, cum on body, cum on clothes, bathroom, blue tile wall',
    '1girl, sitting, on toilet, ((bondage, rope)), black thighhighs, no panties, ((torn clothes)), cum on body, cum on clothes, bathroom, blue tile wall,',
    '1girl,1boy,nude,hetero,nipples,large breasts,(paizuri:1.4),hands on own chest,breasts squeezed together,(facial:1.3),from above,pov,penis,sweat,cum,cum on breasts,(solo focus,steaming body,ahegao:1.3),',    # '1girl, 1boy, vaginal, sex from behind, standing on one leg, leg lift, mature female, huge breasts, black pleated skirt, black thighhighs, office, window, desk',
    #'pov crotch, from above, 1girl, 1boy,vaginal sex,on back,legs up, large breasts, cleavage,nsfw,completely nude, naked,',
    # 'folded anal,anal,anus, anal fluid, suggestive fluid, paddle, 1 woman, large breast,torogao, forehead,  sweat, pussy juice,anal focus,close up,',
    'folded anal,anal,anus, anal fluid, suggestive fluid, paddle, 1 woman, torogao, sweat, pussy juice,anal focus,((defecation, shitting)),',
    '1girl, lying, on back, on floor, gaping anus, large breasts, sleeping, nude, cum on body, wet, cumdrip, alley, ((trash, used condom, used tissue)),', # mash kyrielight
    '((spreading legs)), (spread legs), seductive, (huge breasts), sweating, lovely, ((smile)), ((laying down)), full body, sexy, ((erotic)), seductive eyes,(female orgasm:1.4), cum,((masturbation:1.4)),mature body, (heavy breathing, open mouth:1.4), wet body, rejoice, crying, (face blush), bedroom, ((lying on bed)),naked breasts, (fingering,masturbation), wet pussy, good vagina, ahegao, dripping cum,presenting pussy,', # creampie

    #"sexy,((standing)),((front view)),leaning forward",
    #"office lady,sexy,((sitting, closed legs)),bare legs, teasing,",
    # "((school uniform)), (mini skirt):1.2,",
    #"((school uniform)), (mini skirt):1.2,squatting,spread legs,presenting pussy,pussy,bare pussy,bush,pantyless,",
    #"nurse,nurse uniform,white clothes red cross,head band,sexy,",
    #"nurse,((nurse uniform,white clothes)), white uniform, red cross,head band,sexy,((standing)),((front view)),",
    #"teacher,teacher uniform,black tighs,tie,office lady,sexy,",
    #"teacher,teacher uniform,black tighs,tie,office lady,sexy,((sitting, closed legs)),bare legs, teasing,",
    #"police,police uniform,leather skirt, mini skirt,black tighs,head band,sexy,",
    #"police,police uniform,leather skirt, mini skirt,black tighs,head band,sexy,squatting,spread legs, pantyless,pussy, bare pussy,bush,presenting pussy,",
]

themes_clothing = [
    # '((portrait)),close up,looking at viewer,'
    # '((portrait)):1.3,((face focus)),close up,((ahegao)),going crazy,((open mouth)),tongue out,saliva,eyes wide open,disperse look,body steam,((nsfw)),',
    '((portrait)):1.3,((face focus)),((close up)),((ahegao)),((open mouth)),breath steam,tongue out,saliva,((crying,tears)),((sfw)),',

    '((standing)),looking at viewer,hands behind back,',
    '((on kneees)),((begging)),((from above)),submissive,shy, blusing,looking up,',
    # '((from above)),((begging)),submissive,shy, blusing,looking up,',
    # '((standing)),((from below)),leaning forward,((disgusted look,superiority complex,looking down)),thick tighs,',

    '((squatting)), spread legs, open legs, sexy pose,',
    #'((squatting)), spread legs, ((open legs, showing panties)), presenting panties, sexy pose,',
    '((squatting)), spread legs, ((open legs, showing pussy)), bare pussy, breasts out, ((puvic hair)), pussy, dripping cum, cameltoe, body steam, blushing,((nsfw)),cum on body, wet, cumdrip, ((trash, used condom, used tissue)),',

    '((sitting, crossed legs)), sexy, shy, blushing,',
    # '((sitting, open legs)), spread legs, shy, blushing, ((presenting panties,panties)),',
    '((sitting, open legs)), spread legs, shy, blushing, ((breasts out)), ((showing pussy, bare pussy, puvic hair)), pussy, dripping cum, cameltoe, body steam,((nsfw)),cum on body, wet, cumdrip, ((trash, used condom, used tissue)),',

]

#themes = themes_demo
themes = themes_vanilla
#themes = themes_clothing

bgs = [
    #'<lora:public_v3.0-locon:1>,public, photographers,streets,', # <lora:add_detail:1.2>,

    #'(simple background, black background)',
    #'(simple background, white background)',

    '(simple background, black background):1.3',
    #'(simple background, white background):1.3',

    #'',
]

negatives = [
    "(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, inaccurate eyes, extra digit, fewer digits,"
    "(extra arms:1.2),accessories,loli,muscles,muscular,(cat ears):1.2,transparent clothes,wet clothes,bad hands,accessories,",

    "bad anatomy, (bad quality, worst quality:1.4), jpeg artifacts, blurry, low resolution, distorted bodies, body contortions, bad finger anatomy, multiple anuses, split images, multiple slides, image grids, (monochrome:1.1), (grayscale:1.2), (text:1.4), watermarks, artist names, more than 2 girls, image frames, more than 5 fingers, less than 5 fingers, (out of frame:1.2), (loli), badhandv4, badquality, ((cropped body)), easynegative, bad-artist-anime, bad-image-v2-39000, bad_prompt_version2, bad_quality, ng_deepnegative_v1_75t, verybadimagenegative_v1.1-6400, vile_prompt3, bad-hands-5, verybadimagenegative_v1.3, EasyNegative, ng_deepnegative_v1_75t, (painting by bad-artist-anime:0.9), (painting by bad-artist:0.9), watermark, text, error, blurry, jpeg artifacts, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, artist name, (worst quality, low quality:1.4), ((bad anatomy)), extra limbs,extra hands, extra arms, extra legs, extra ears, extra fingers, extra anus, extra vagina, child, loli, (censored:1.3), multiple views, blurry, bokeh, depth of field, tilt shift, (easynegative:1.2), (low quality, worst quality:1.3), (monochrome:1.1), (bad_prompt_version2:0.8), (worst quality, low quality:1.4), extra fingers,fewer fingers, extra legs, extra hands, fewer hands, loli, mutant, bad anatomy, mutated hand, mutated leg, error, text, logo, watermark, elf, bad_prompt_version2:0.8, easynegative, low quality, lowres, (bad anatomy, badhandv4,bad proportions), ((asymmetry)), watermark, missing fingers, extra digit, fewer digits, amputee, loli, child, malformed hands, error, jpeg artifacts, cropped, extra fingers, extra legs, (deformation), deformed, (mutilated), text, signature, black and white, logo, (asymmetrical breasts), (cross eyed), ((bad eyes)), (disfigured eyes), speech bubble, (bird_head), (blob), malformed heels, asymmetrical heels, extra limbs,cat ears,animal ears,",
]

"""
negatives = {
    "realistic": [
        "((3d, cartoon, anime, sketches)), (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), bad anatomy, out of view, cut off, ugly, deformed, mutated, ((young)), EasyNegative, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, extra fingers, fewer fingers,(ugly eyes, deformed iris, deformed pupils, fused lips and teeth:1.2), (un-detailed skin, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.2), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck
 (badhandv4), ((emilia clarke:1.4)), ((celebrity))",
        "badhandv4, paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, manboobs, 
ouble navel, muted arms, fused arms, analog, analog effects, bad architecture, watermark, (mole:1.5), EasyNegative"
    ],
    "anime": [
        "(low quality, worst quality:1.4), (bad anatomy), (inaccurate limb:1.2), bad composition, inaccurate eyes, extra digit, fewer digits, (extra arms:1.2),accessories,loli,red eyes,bad hands",
        "easynegative, badhandv4, (worst quality, low quality, normal quality), bad-artist, blurry, ugly, ((bad anatomy)),((bad hands)),((bad proportions)),((duplicate limbs)),((fused limbs)),((interlocking fingers)),((poorly drawn face))"
    ]
}
print(negatives["anime"][1])
"""

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

#charlist = []
#for character, detail in characters.items():
#    charlist.append(character)
#pprint.pprint(charlist)

included_characters = [
    'boa-hancock',
    'nami',
    'nico-robin',
    'yuki-jujutsu',
    'Fern',
    'frieren',
    'tsunade',

#    'dark_magician_girl',
#    'senjougahara_hitagi',
#    # 'power',
#    # 'Jabami Yumeko',
#    'mikasa_ackerman',
#    'shizukazom100',
#
    'starfire',
#    'rukia',
#    'tatsumakiselect',
#    'ramona',
    'Gwen',
    'Sarada',
#    'anna-shaman-king',
#    'kohaku-dr-stone',
#    'humura-dr-stone',
#    'kaguya-sama',
#    'chika',
#    'Kochou_Shinobu',
#    'jolynejojo',
#    'neferpitou',
#
#    'maki-zenin',
#    'Kugisaki_lora',
#    'Utahime',
    'yor',
#    'toph',
#    'korra',
#    # 'katara',
#    'videl',
#    'milk',
#    'bulma',
    'Ochakodim8',
    'TogaHimikoLoRA',
#    #'kagami',
#    #'marinette',
    'onepieceYamato',
#    'PeronaLORA',
#    'yoko',
#    'ulti',
#    #'Nero',
#
#    'jenny-pokemon-police',
#    'Dawn',
#    'Misty',
#    'jessie',

]
#included_characters = included_characters[-2:]

final_prompts = {}
clothes_on = False
amt = 1

for i in range(amt):
    for character, detail in characters.items():
        base_prompts = len(detail['base'])
        if character not in included_characters:
            continue
        #if base_prompts > 1:
        #    continue
        # print(character, len(detail['base']))

        try:
            if not final_prompts[character]:
                final_prompts[character] = []
        except:
            final_prompts[character] = []
        if clothes_on:
            for key, prompt in detail['base'].items():
                # for key, current_clothing in detail['clothes'].items():
                for theme in themes:
                    bg = random.choice(bgs)
                    separator_cl = ','
                    separator_th = ','
                    separator_bg = ','
                    current_clothing = detail['clothes'][random.choice(list(detail['clothes'].keys()))]
                    if prompt[-1] == separator_cl:
                        separator_cl = ''
                    if current_clothing[-1] == separator_th:
                        separator_th = ''
                    if theme[-1] == separator_bg:
                        separator_bg = ''
                    out_prompt = f"{base_prompt},standing,{prompt}{separator_cl}{current_clothing}{separator_th}{theme}{separator_bg}{bg}"
                    final_prompts[character].append(out_prompt)
        else:
            for key, prompt in detail['base'].items():
                for theme in themes:
                    bg = random.choice(bgs)
                    separator_th = ','
                    separator_bg = ','
                    if prompt[-1] == separator_th:
                        separator_th = ''
                    if theme and theme[-1] == separator_bg:
                        separator_bg = ''
                    if not theme:
                        separator_bg = ''
                    out_prompt = f"{base_prompt}{prompt}{separator_th}{theme}{separator_bg}{bg}"
                    final_prompts[character].append(out_prompt)

out_file_content = ""
for character in included_characters:
    current_character = None
    try:
        current_character = final_prompts[character]
    except:
        continue
    for character_prompt in current_character:
        # print(character_prompt)
        out_file_content += f"{character_prompt}\n"

#value_list = [len(value) for value in final_prompts.values()]
print(f"[+] Total characters: {len(final_prompts)}")
for character in included_characters:
    print(f"\t[+] Prompts: {len(final_prompts[character])} [{character}]")
#print(f"[+] Prompts: {sum(value_list)}")

outfile = 'clothing_characters.txt' if clothes_on else 'vanilla_characters.txt'
with open(outfile, 'w') as f:
    f.write( out_file_content )
