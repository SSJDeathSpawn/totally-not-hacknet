from typing import Union

from exceptions.ser_des import DeserializationError
from game.storage_system.storage_unit import StorageUnit


def validate_root_dir_contents(root_dir_contents: list[StorageUnit]) -> None:
    """Checks if a root directory dictionary is valid"""

    if not isinstance(root_dir_contents, list):
        raise DeserializationError('Root directory not given as a list. Cannot deserialize')
        
    for content in root_dir_contents:
        validate_su(content)

    
def validate_su(su_dict: dict[str, Union[str, list]]) -> None:
    """Checks if a storage unit dictionary is valid"""

    if not ('name' in su_dict and 'contents' in su_dict):
        raise DeserializationError('Invalid dictionary. Cannot deserialize')
        
    name = su_dict.get('name')
    contents = su_dict.get('contents')

    if not isinstance(name, str):
        raise DeserializationError('Name needs to be of type string. Cannot deserialize')

    if not (isinstance(contents, str) or isinstance(contents, list)):
        raise DeserializationError('Contents are of invalid type. Cannot deserialize')

    if isinstance(contents, list):
        for content in contents:
            validate_su(content)
