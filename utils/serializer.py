import json

from logging import Logger

from logging_module.custom_logging import get_logger
from game.storage_system.directory import Directory, RootDir
from game.storage_system.file import File
from utils.validator import validate_root_dir_contents

logger: Logger = get_logger(__name__)

def serialize_root_directory(root: RootDir, path: str) -> None:
    """Saves the RootDir object in the given path as a JSON file"""

    if not isinstance(root, RootDir):
        raise TypeError('Given root is not an instance of RootDir. Cannot serialize')
    
    root_dir_contents = []
    
    for su in root.get_contents():
        if isinstance(su, File):
            root_dir_contents.append(__file2dict(su))
        else:
            root_dir_contents.append(__dir2dict(su))

    validate_root_dir_contents(root_dir_contents)

    try:
        with open(path, 'w') as f:
            json.dump(root_dir_contents, f, indent=4)
            
    except FileNotFoundError as e:
        logger.error(f'File \'{path}\' not found. Cannot serialize')


def __file2dict(file_su: File) -> dict[str, str]:
    """Converts a file into a dictionary"""

    return {'name': file_su.get_name(), 'contents': file_su.get_contents()} # FIXME: Decode if bytes


def __dir2dict(dir_su: Directory) -> dict[str, list]:
    """Converts a directory into a dictionary"""

    contents = []

    for content in dir_su.get_contents():
        if isinstance(content, File):
            contents.append(__file2dict(content))
        else:
            contents.append(__dir2dict(content))
    
    return {'name': dir_su.get_name(), 'contents': contents}
