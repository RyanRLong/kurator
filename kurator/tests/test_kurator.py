# pylint: disable-all
from unittest import TestCase

import kurator.kurator as k
import os
import re
from shutil import rmtree
from distutils.dir_util import copy_tree

class ImportMedia(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.test_file = os.path.join(self.fixtures, 'IMG_0234.jpg')

        self.library = os.path.join(self.dir_path, 'library')
        if not os.path.isdir(self.library):
            os.mkdir(self.library)
        k.import_media(self.dir_path, self.library)

    def tearDown(self):
        if os.path.isdir(self.library):
            rmtree(self.library)


    def test_import_media_imports_created_all_folders(self):
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20140201')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20160322')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20171019')))

    def test_import_media_recognizes_files_with_no_meta_data(self):
        self.assertTrue(os.path.isdir(os.path.join(self.library, 'no_data_')))


class FixNames(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.test_file = os.path.join(self.fixtures, 'IMG_0234.jpg')
        self.library = os.path.join(self.dir_path, 'library_fix_name_test')

        if not os.path.isdir(self.library):
            print("making lib")
            os.mkdir(self.library)
        copy_tree(self.fixtures, self.library)
        k.fix_names(self.library)

    def tearDown(self):
        if os.path.isdir(self.library):
            rmtree(self.library)

    def test_fix_names_creates_correct_directories(self):
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20140201')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20160322')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20171019')))

    def test_fix_names_recognizes_files_with_no_meta_data(self):
        self.assertTrue(os.path.isdir(os.path.join(self.library, 'no_data_')))




