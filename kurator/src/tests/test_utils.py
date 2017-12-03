from unittest import TestCase

from os import path, rmdir
import time

from utils import (find_all_files,
                   get_timestamp, 
                   get_file_tags,
                   generate_filename_from_meta,
                   generate_foldername_from_meta,
                   directory_exists,
                   create_directory,
                   generate_md5,
                   get_datestring_or
                   )

class UtilsTest(TestCase):

    src_path = path.abspath(path.dirname(__file__))
    fixtures_path = path.join(path.abspath(path.dirname(__file__)), 'fixtures')

    def setUp(self):
        """
        set up
        """
        # for file_name in listdir(self.fixtures_path):
        #     copy(path.join(self.fixtures_path, file_name),  path.join(self.src_path, file_name))
        self.file1 = path.join(self.fixtures_path, '1.jpg')
        self.file2 = path.join(self.fixtures_path, '2.jpg')
        self.file3 = path.join(self.fixtures_path, 'xxxx_NO_DATA.jpg')

    def tearDown(self):
        """
        tear down
        """
        pass

    def test_find_all_files(self):
        """
        test find_all_files
        """
        expect = [
            self.file1,
            self.file2,
            self.file3,
        ]
        test = find_all_files(self.fixtures_path, ('.jpg'))
        self.assertEqual(test, expect)

    def test_get_timestamp(self):
        """
        test_get_timestamp
        """
        expect = 10
        test = len(get_timestamp())
        self.assertEqual(test, expect)

    def test_get_file_tags(self):
        """
        test get_file_tags
        """
        test = get_file_tags(self.file1)
        expect = {
            'model': 'Canon EOS DIGITAL REBEL XTi',
            'dateTime': '2008:07:27 17:35:16',
            'orientation': 'Horizontal (normal)',
            'fileName': self.file1
        }
        self.assertEqual(test, expect)

    def test_gen_filename_from_meta(self):
        """
        test generate_filename_from_meta
        """
        test = generate_filename_from_meta(self.file1)
        expect = '20080727-173516.jpg'
        self.assertEqual(test, expect)

    def test_gen_foldername_from_meta(self):
        """
        test generate_foldername_from_meta(self):
        """
        test = generate_foldername_from_meta(self.file1)
        expect = '20080727'
        self.assertEqual(test, expect)

    def test_directory_exists(self):
        """
        test directory_exists
        """
        test = directory_exists(path.dirname(self.file1))
        expect = True
        self.assertEqual(test, expect)

    def test_create_directory(self):
        """
        test create_directory
        """
        dir_path = path.join(self.fixtures_path, 'test')
        create_directory(dir_path)
        test = path.isdir(dir_path)
        expect = True
        rmdir(dir_path)
        self.assertEqual(test, expect)

    def test_create_directory_no_data(self):
        """
        test create_directory
        """
        dir_path = path.join(self.fixtures_path, 'NO_DATA_')
        create_directory(dir_path)
        test = path.isdir(dir_path)
        rmdir(dir_path)
        expect = True
        self.assertEqual(test, expect)

    def test_gen_md5(self):
        """
        test generate md5
        """
        test = generate_md5(self.file1)
        expect = '1a7fda3147a130b7e79a85d5d4481333'
        self.assertEqual(test, expect)

    def test_get_datestring_or_1(self):
        """
        test generate_datestring with 8 digit string
        """
        test = get_datestring_or('20170101')
        expect = '2017-01-01'
        self.assertEqual(test, expect)

    def test_get_datestring_or_valid(self):
        """
        test generate_datestring with 8 digit string
        """
        test = get_datestring_or('20170101')
        expect = '2017-01-01'
        self.assertEqual(test, expect)

    def test_get_datestring_or_invalid(self):
        """
        test generate_datestring with invalid string
        """
        test = get_datestring_or('abcd')
        expect = time.strftime("%Y-%m-%d")
        self.assertEqual(test, expect)




