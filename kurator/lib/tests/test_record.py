import os
import sqlite3

import pytest

from kurator.lib.record import SqliteRecord

DB_NAME = SqliteRecord.DATABASE_NAME


class Test_Record:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.record = SqliteRecord(os.path.join(tmpdir, DB_NAME))
        self.connection = sqlite3.connect(os.path.join(tmpdir, DB_NAME))
        self.cursor = self.connection.cursor()
        self.tmpdir = tmpdir

        yield self.record
        self.connection.close()
        if os.path.exists(os.path.join(tmpdir, DB_NAME)):
            os.remove(os.path.join(tmpdir, DB_NAME))

    @pytest.fixture
    def add_records(self): # pragma: no cover
        sql = """
        INSERT INTO {} (
            'id',
            'created_date',
            'model',
            'orientation',
            'path',
            'imported_date'
        ) VALUES 
            ("e602f0f61e8d785377d2e7478e3a2131","2014:05:29 14:58:25","iPhone 4S","unknown","x:HomeMedia\Pictures\20140529\20140529-145825.jpg","2018-03-31 21:11:14.321210"),
            ("ec5a49dfb727e695cf098d9ef342c5f1","2017:12:20 09:57:35","iPhone 5s","Rotated 90 CW","x:HomeMedia\Pictures\20171220\20171220-095735.jpg","2018-03-31 21:11:14.417798"),
            ("b02a86a6b2e82b52f46b0a2b4a4c0828","2017:12:20 09:37:14","iPhone 5s","Rotated 90 CW","x:HomeMedia\Pictures\20171220\20171220-093714.jpg","2018-03-31 21:11:14.541881"),
            ("cfbcf0c547f1b916b7007d013a836f06","2017:12:20 09:57:38","iPhone 5s","Rotated 90 CW","x:HomeMedia\Pictures\20171220\20171220-095738.jpg","2018-03-31 21:11:14.662481")
        """.format(SqliteRecord.TABLE_NAME)
        self.cursor.execute(sql)
        self.connection.commit()


    def test_create_photos_table(self):
        # table is created on instantiation
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}';".format(SqliteRecord.TABLE_NAME))
        assert len(self.cursor.fetchall()) == 1
        self.record.close()

    def test_create_photos_does_not_recreate_if_database_exists(self):
        self.record.create_database_if_not_exist(os.path.join(self.tmpdir, DB_NAME))
        expect = os.path.join(self.tmpdir, DB_NAME)
        result = self.record.db_path
        self.record.close()
        assert expect == result

    def test_create_photos_creates_Database_if_None_is_passed(self):
        self.record.create_database_if_not_exist(None)
        expect = os.path.join(self.tmpdir, DB_NAME)
        result = self.record.db_path
        self.record.close()
        assert expect == result

    def test_create_record(self):
        self.cursor.execute("SELECT count(*) from {}".format(SqliteRecord.TABLE_NAME))
        assert self.cursor.fetchone()[0] == 0
        self.record.create_record({
            'id': 'e602f0f61e8d785377d2e7478e3a2131',
            'created_date': '2014:05:29 14:58:25',
            'model': 'iphone 4s',
            'orientation': 'unknown',
            'file_path': 'x:HomeMedia\\Pictures\\20140529\\20140529-145825.jpg',
        })
        self.cursor.execute("SELECT count(*) from {}".format(SqliteRecord.TABLE_NAME))
        assert self.cursor.fetchone()[0] == 1
        self.record.close()

    def test_record_exists(self, add_records):
        results = self.record.record_exists('e602f0f61e8d785377d2e7478e3a2131')
        assert results == 1
        self.record.close()



