import json
import random
import string

from logging import Logger
from logging_module.custom_logging import get_logger
from typing import Optional


logger: Logger = get_logger(__name__)

GENERATED_IDS_PATH: str = 'data/generated_ids.json'
GENERATED_PIDS_PATH: str = 'data/generated_pids.json'
GENERATED_NETWORK_IDS_PATH: str = 'data/generated_network_ids.json'


def generate_id(length: int = 4) -> Optional[str]:
    """Generates, stores and returns a random ID with the given length (default 4)"""

    # Trying to read the file
    try:
        with open(GENERATED_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, list):
            raise TypeError
    
    # File probably has some issues. Creating a new empty file
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        logger.warning(f'Encountered an error while generating ID. Trying to fix')

        try:
            open(GENERATED_IDS_PATH, 'w')
            
            # Generating ID and setting it as the only generated ID
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))
            generated = [new_id]

        # Directory not found
        except FileNotFoundError:
            logger.error(f'Directory <{"/".join(GENERATED_IDS_PATH.split("/")[:-1])}> not found. The application will continue to run but no ID will be returned')
            return None
        
    # Generating ID
    else:
        while True:
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))

            if new_id not in generated:
                generated.append(new_id)
                break

    # Storing ID
    with open(GENERATED_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2)

    return new_id


def generate_pid(length: int = 4) -> Optional[str]:
    """Generates, stores and returns a random process ID with the given length (default 4)"""

    # Trying to read the file
    try:
        with open(GENERATED_PIDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, list):
            raise TypeError
    
    # File probably has some issues. Creating a new empty file
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        logger.warning(f'Encountered an error while generating PID. Trying to fix')

        try:
            open(GENERATED_PIDS_PATH, 'w')
            
            # Generating PID and setting it as the only generated ID
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))
            generated = [new_id]

        # Directory not found
        except FileNotFoundError:
            logger.error(f'Directory <{"/".join(GENERATED_PIDS_PATH.split("/")[:-1])}> not found. The application will continue to run but no PID will be returned')
            return None
        
    # Generating PID
    else:
        while True:
            new_id = ''.join(random.choices(string.ascii_uppercase, k=length))

            if new_id not in generated:
                generated.append(new_id)
                break

    # Storing PID
    with open(GENERATED_PIDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2)

    return new_id
        
        
def generate_network_id() -> Optional[str]:
    """Generates, stores and returns a random network ID"""
    
    # Trying to read the file
    try:
        with open(GENERATED_NETWORK_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, dict):
            raise TypeError
    
    # File probably has some issues. Creating a new empty file
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        logger.warning(f'Encountered an error while generating ID. Trying to fix')

        try:
            open(GENERATED_NETWORK_IDS_PATH, 'w')
            
            # Generating ID and setting it as the only generated ID
            new_id = '.'.join(list(map(str, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))
            
            generated = {new_id: []}

        # Directory not found
        except FileNotFoundError:
            logger.error(f'Directory <{"/".join(GENERATED_NETWORK_IDS_PATH.split("/")[:-1])}> not found. The application will continue to run but no network ID will be returned')
            return None

    # Generating ID  
    else:  
        while True:
            new_id = '.'.join(list(map(str, (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))))

            if new_id not in generated:
                generated[new_id] = []
                break

    # Storing ID
    with open(GENERATED_NETWORK_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2)

    return new_id


def generate_host_id(network_id: str) -> Optional[str]:
    """Generates, stores and returns a random host ID for a given network ID"""

    # Trying to read the file
    try:
        with open(GENERATED_NETWORK_IDS_PATH, 'r') as f:
            generated = json.load(f)

        if not isinstance(generated, dict):
            raise TypeError

    # File not found
    except FileNotFoundError:
        logger.error(f'File <{GENERATED_NETWORK_IDS_PATH}> not found. The application will continue to run but no host ID will be returned')
        return None

    # File of incorrect format
    except (json.decoder.JSONDecodeError, TypeError):
        logger.error(f'JSON file <{GENERATED_NETWORK_IDS_PATH}> is of incorrect format. The application will continue to run but no host ID will be returned')
        return None

    # Generating ID
    else:

        # Network ID invalid
        if network_id not in generated.keys():
            logger.error(f'Invalid network ID {network_id}. The application will continue to run but no host ID will be returned')
            return None
            
        host_ids = generated.get(network_id)

        while True:
            new_id = str(random.randint(1, 255))

            if new_id not in host_ids:
                generated[network_id].append(new_id)
                break

    # Storing ID
    with open(GENERATED_NETWORK_IDS_PATH, 'w') as f:
        json.dump(generated, f, indent=2) 

    return new_id      
