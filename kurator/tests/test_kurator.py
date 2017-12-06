# pylint: disable-all
from unittest import TestCase

import kurator.kurator as k
import os
import re
import glob
from shutil import rmtree
from distutils.dir_util import copy_tree

class ImportMedia(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.library = os.path.join(self.dir_path, 'import_media_test')

        if not os.path.isdir(self.library):
            os.mkdir(self.library)
        k.import_media(self.dir_path, self.library)

    def tearDown(self):
        if os.path.isdir(self.library):
            rmtree(self.library)

    def test_import_media_imports_created_all_folders_and_files(self):
        self.assertTrue(os.path.exists(os.path.join(self.library, '20140201', '20140201-165116.jpg')))
        self.assertTrue(os.path.exists(os.path.join(self.library, '20160322', '20160322-120505.jpg')))
        self.assertTrue(os.path.exists(os.path.join(self.library, '20171019', '20171019-125142.jpg')))

    def test_import_media_recognizes_files_with_no_meta_data(self):
        test = [file for file in glob.glob(os.path.join(self.library, 'no_data_', 'NO_DATA_*'))]
        self.assertEqual(len(test), 1)


class FixNames(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.library = os.path.join(self.dir_path, 'fix_name_test')

        if not os.path.isdir(self.library):
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

    def test_fix_names_puts_dups_alongside_originals(self):
        # Should have one DUP returned
        test = [file for file in glob.glob(os.path.join(self.library, '*', '*DUP*'))]
        self.assertEqual(len(test), 1)

class Prune(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.library = os.path.join(self.dir_path, 'prune_test')

        if not os.path.isdir(self.library):
            os.mkdir(self.library)
        copy_tree(self.fixtures, self.library)
        k.prune(self.library)

    def tearDown(self):
        if os.path.isdir(self.library):
            rmtree(self.library)

    def test_prune_removes_only_duplicate_files(self):
        self.assertTrue(not os.path.exists(os.path.join(self.library, 'prune_test', 'IMG_0234.jpg')))
        self.assertTrue(os.path.exists(os.path.join(self.library, 'IMG_0625 - Copy.JPG')))
        self.assertTrue(os.path.exists(os.path.join(self.library, 'IMG_0234.jpg')))




