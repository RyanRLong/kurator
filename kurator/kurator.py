"""
Kurator.py
"""
# pylint: disable=too-few-public-methods
import filecmp
import logging
import os
import sys
from shutil import copy2 as copy_file

from kurator.lib import utils as u
from kurator.lib.record import SqliteRecord


class NoError(logging.Filter):
    """
    Only reports items not in Warning, Error, and Critical
    """

    def filter(self, record):
        return record.levelname not in ['WARNING', 'ERROR', 'CRITICAL']


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

HANDLER_STDOUT = logging.StreamHandler(sys.stdout)
HANDLER_STDOUT.setLevel(logging.WARNING)
HANDLER_STDOUT.setFormatter(FORMATTER)
HANDLER_STDOUT.addFilter(NoError())

HANDLER_STDERR = logging.StreamHandler()
HANDLER_STDERR.setLevel(logging.INFO)
HANDLER_STDERR.setFormatter(FORMATTER)

LOGGER.addHandler(HANDLER_STDOUT)
LOGGER.addHandler(HANDLER_STDERR)

# Disable exif logging
EXIF_LOGGER = logging.getLogger('exifread')
EXIF_LOGGER.setLevel(logging.ERROR)


def import_media(source, library):
    """ Imports media from source into library """

    files = u.find_all_files(source, ('.jpg', '.mp4', '.mov'))
    print('Processing {} photos'.format(len(files)))
    for idx, file_item in enumerate(files):
        folder_name = os.path.join(library, u.generate_foldername_from_meta(file_item))
        file_name = u.generate_filename_from_meta(file_item)
        u.create_directory(folder_name)

        if os.path.exists(os.path.join(folder_name, file_name)):
            file_name = '{}_DUP_{}{}'.format(file_name, u.get_time_stamp(), idx)
        file_destination = os.path.join(folder_name, file_name)
        media_id = u.generate_md5(file_item)
        if create_record_if_not_exist(media_id, file_destination) is True:
            copy_file(file_item, file_destination)


def create_record_if_not_exist(media_id, file_path):
    """
    Creates a new record in the database
    :param media_id:
    :param file_path: absolute path
    :return:
    """
    record = SqliteRecord()
    if not record.record_exists(media_id):
        record_data = u.get_file_tags(file_path)
        record_data['media_id'] = media_id
        record.create_record(record_data)
        return True
    else:
        return False


def prune(target):
    """
    TODO: Needs to be re-written or may not be necessary
    Removes duplicate files from the target
    :param target:
    :return:
    """

    files = u.find_all_files(target, ('.jpg', '.mp4', '.mov'))
    LOGGER.info('Scanning %s files...', len(files))

    to_remove = []
    for idx, primary_file in enumerate(files):
        for comparing_file in files[idx + 1: len(files)]:
            if filecmp.cmp(primary_file, comparing_file):
                LOGGER.info("duplicates found: %s and %s are equal; slating %s for removal",
                            primary_file, comparing_file, comparing_file)
                to_remove.append(comparing_file)

    LOGGER.info('Removing %s files...', len(to_remove))
    for file_item in to_remove:
        if os.path.isfile(file_item):
            LOGGER.info('removing file_item %s', file_item)
            os.remove(file_item)
        else:
            print('file_item {} previously removed'.format(file_item))


def fix_names(target):
    """
    Checks that the name of the file_item matches the exif data
    contained in the file_item

    :param target:
    :return:
    """
    files = u.find_all_files(target, ('.jpg', '.mp4', '.mov'))
    print('Scanning {} photos'.format(len(files)))
    for idx, file_item in enumerate(files):
        folder_name = os.path.join(target, u.generate_foldername_from_meta(file_item))
        file_name = u.generate_filename_from_meta(file_item)
        u.create_directory(folder_name)
        LOGGER.info('Processing file %s', file_name)

        if os.path.exists(os.path.join(folder_name, file_name)):
            file_name = '{}_DUP_{}{}'.format(file_name, u.get_time_stamp(), idx)
        copy_file(file_item, os.path.join(folder_name, file_name))
        os.remove(file_item)


def import_to_database(target):
    """
    Imports all media data in target to database
    :param target:
    :return:
    """
    files = u.find_all_files(target, ('.jpg', '.mp4', '.mov'))
    print('Scanning {} photos'.format(len(files)))
    for file_item in files:
        folder_name = os.path.join(target, u.generate_foldername_from_meta(file_item))
        file_name = u.generate_filename_from_meta(file_item)
        if os.path.exists(os.path.join(folder_name, file_name)):
            file_path = os.path.join(folder_name, file_name)
            media_id = u.generate_md5(file_path)
            create_record_if_not_exist(media_id, file_path)


if __name__ == "__main__":
    pass
