# pylint: disable-all
from unittest import TestCase

import kurator.kurator as k
import os
import re
from shutil import rmtree

class UtilsTest(TestCase):
    def setUp(self):
        print(dir(k))
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
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20060730')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20140201')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20160322')))
        self.assertTrue(os.path.isdir(os.path.join(self.library, '20171019')))


