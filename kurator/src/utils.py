"""utils.py

Utility module for kurator

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension
"""

from __future__ import print_function
from hashlib import md5
from os import walk, path, makedirs
import time
import random

import exifread

def find_all_files(source, types):
    """Search for files of type and return list of absolute
    paths.

    source -- path to find files
    types -- tuple of types to search for
    """
    matches = []
    for root, _, files in walk(source):
        for filename in files:
            if filename.lower().endswith(types):
                matches.append(path.join(root, filename))
    return matches

def get_timestamp():
    """Unix-like timestamp"""
    return str(int(time.time()))


def get_file_tags(raw_path):
    """Get all exif tags from a file"""
    with open(raw_path, 'rb') as file_path:
        raw_tags = exifread.process_file(file_path)
        tags = {
            'fileName': raw_path,
            'dateTime': raw_tags['Image DateTime'].printable \
             if 'Image DateTime' in raw_tags \
             else 'NO_DATA_' + get_timestamp() + str(random.randint(1,1000)),
            'model': raw_tags['Image Model'].printable if 'Image Model' in raw_tags else 'unknown',
            'orientation': raw_tags['Image Orientation'].printable \
             if 'Image Orientation' in raw_tags \
             else 'unknown'
        }
        return tags

def generate_filename_from_meta(file_path):
    """Generate a filename from exif data.  Absolute file_path
    and extension included.
    """
    _, extension = path.splitext(file_path)
    return get_file_tags(file_path)['dateTime']\
    .replace(':', '')\
    .replace(' ', '-') + extension.lower()

def generate_foldername_from_meta(file_path):
    """Generate folder name from exif data"""
    return get_file_tags(file_path)['dateTime'].replace(':', '').replace(' ', '-').lower()[:8]

def directory_exists(directory_path):
    """Returns true if directory exists"""
    return path.isdir(directory_path) and path.exists(directory_path)

def create_directory(directory_path):
    """Creates a directory if it does not already exist.
    If "NO_DATA_" is in the path, a "NO_DATA_" directory
    is created instead.
    """
    print(directory_path)
    if "NO_DATA_" in directory_path:
        directory_path = path.dirname(path.join(directory_path, 'NO_DATA_'))
    if not directory_exists(directory_path):
        makedirs(directory_path)

def generate_md5(file_path):
    """Generate hashes"""
    return md5(open(file_path, 'rb').read()).hexdigest()

def get_datestring_or(string):
    """ Returns date string """
    if str(string[:8]).isdigit():
        return '{}-{}-{}'.format(string[:4], string[4:6], string[6:8])
    return time.strftime("%Y-%m-%d")

if __name__ == "__main__":
    pass
