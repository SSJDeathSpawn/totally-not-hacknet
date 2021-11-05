import random
import json


def generate_ip():
    with open("data/generated_ips.json", "r") as f:
        generated = json.load(f)

    gen = f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'
    
    while gen in generated:
        gen = f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'

    generated.append(gen)
    
    with open("data/generated_ips.json", "w") as f:
        json.dump(generated, f, indent=4)
        
    return gen
    