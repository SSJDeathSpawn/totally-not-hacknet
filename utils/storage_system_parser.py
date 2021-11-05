from game.storage_system.file import File
from game.storage_system.directory import Directory, RootDir


def parse_root(root):
    rt = RootDir([])

    for su in root:
        su.update({'parent': rt})
        if isinstance(su['contents'], list):
            rt.add(parse_dir(su))
        else:
            rt.add(parse_file(su))

    return rt


def parse_dir(dir_dict):
    dir = Directory(dir_dict['name'], [], dir_dict['parent'])

    for su in dir_dict['contents']:
        su.update({'parent': dir})
        if isinstance(su['contents'], list):
            dir.add(parse_dir(su))
        else:
            dir.add(parse_file(su))

    return dir


def parse_file(file_dict):
    fl = File(file_dict['name'], file_dict['contents'], file_dict['parent'])
    return fl
