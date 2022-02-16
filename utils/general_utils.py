import json
import random
import string

from logging_module.custom_logging import get_logger


logger = get_logger(__name__)

GENERATED_IDS_PATH = 'data/generated_ids.json'
GENERATED_NETWORK_IDS_PATH = 'data/generated_network_ids.json'


def generate_id(length: int = 4) -> str:
    """Generates, stores and returns a random ID with the given length (default 4)"""

    try:
        with open(GENERATED_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, list):
            raise TypeError
    
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        logger.warning(f'Encountered an error while generating ID. Trying to fix')

        try:
            with open(GENERATED_IDS_PATH, 'w'):
                pass
            
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))
            generated = [new_id]

        except FileNotFoundError:
            logger.error(f'Directory <{"/".join(GENERATED_IDS_PATH.split("/")[:-1])}> not found. The application will continue to run but no ID will be returned')
            return None
        
    else:
        while True:
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))

            if new_id not in generated:
                generated.append(new_id)
                break

    with open(GENERATED_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2)

    return new_id
        
        
def generate_network_id():
    """Generates, stores and returns a random network ID"""
    
    try:
        with open(GENERATED_NETWORK_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, dict):
            raise TypeError
    
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        logger.warning(f'Encountered an error while generating ID. Trying to fix')

        try:
            with open(GENERATED_NETWORK_IDS_PATH, 'w'):
                pass
            
            new_id = '.'.join(list(map(str, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
            
            generated = {new_id: []}

        except FileNotFoundError:
            logger.error(f'Directory <{"/".join(GENERATED_NETWORK_IDS_PATH.split("/")[:-1])}> not found. The application will continue to run but no network ID will be returned')
            return None
        
    else:  
        while True:
            new_id = '.'.join(list(map(str, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))

            if new_id not in generated:
                generated[new_id] = []
                break

    with open(GENERATED_NETWORK_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2)

    return new_id


def generate_host_id(network_id: str):
    """Generates, stores and returns a random host ID for a given network ID"""

    try:
        with open(GENERATED_NETWORK_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, dict):
            raise TypeError

    except FileNotFoundError:
        logger.error(f'File <{GENERATED_NETWORK_IDS_PATH}> not found. The application will continue to run but no host ID will be returned')
        return None

    except (json.decoder.JSONDecodeError, TypeError):
        logger.error(f'JSON file <{GENERATED_NETWORK_IDS_PATH}> is of incorrect format. The application will continue to run but no host ID will be returned')
        return None

    else:
        if network_id not in generated.keys():
            logger.error(f'Invalid network ID {network_id}. The application will continue to run but no host ID will be returned')
            return None
            
        host_ids = generated.get(network_id)

        while True:
            new_id = str(random.randint(1, 255))

            if new_id not in host_ids:
                generated[network_id].append(new_id)
                break

    with open(GENERATED_NETWORK_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2) 

    return new_id      
