# pylint: disable-all
from unittest import TestCase

import kurator.lib.utils as utils
import os
import re

class UtilsTest(TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.fixtures = os.path.join(self.dir_path, './fixtures')
        self.test_file = os.path.join(self.fixtures, 'IMG_0234.jpg')

    def test_find_all_files_finds_all_jpgs(self):
        print(self.fixtures)
        test = len(utils.find_all_files(self.fixtures, ('jpg')))
        expect = 4
        self.assertEqual(test, expect)

    def test_get_time_stamp_returns_string(self):
        test = bool(re.search('\d{10}', utils.get_time_stamp()))
        expect = True
        self.assertEquals(test, expect)

    def test_get_file_tags_returns_all_tags(self):
        test = utils.get_file_tags(self.test_file)
        expect = {
            'dateTime': '2017:10:19 12:51:42',
            'model': 'SM-G935V', 'orientation': 'Horizontal (normal)'
        }
        self.assertEquals(test['dateTime'], expect['dateTime'])
        self.assertEquals(test['model'], expect['model'])

    def test_generate_filename_from_meta_generates_correct_filename(self):
        test = utils.generate_filename_from_meta(self.test_file)
        expect = '20171019-125142.jpg'
        self.assertEquals(test, expect)

    def test_generate_foldername_from_meta_generates_correct_foldername(self):
        test = utils.generate_foldername_from_meta(self.test_file)
        expect = '20171019'
        self.assertEquals(test, expect)

    def test_create_directory_creates_directory(self):
        utils.create_directory(os.path.join(self.fixtures, 'test'))
        test = os.path.isdir(os.path.join(self.fixtures, 'test'))
        self.assertTrue(test)
        os.rmdir(os.path.join(self.fixtures, 'test'))

    def test_generate_md5_gives_correct_hash(self):
        test = utils.generate_md5(self.test_file)
        expect ='8c63d25bf96df5c22d4ae93c741a1906'
        self.assertEqual(test, expect)

    def test_get_date_string_or_returns_date_string(self):
        test = utils.get_date_string_or('20170101ABCD')
        expect = '2017-01-01'
        self.assertEqual(test, expect)

    def test_get_date_string_or_returns_default_date_string(self):
        test = bool(re.search('\d{4}-\d{2}-\d{2}', utils.get_date_string_or('XYZ')))
        self.assertTrue(test)


