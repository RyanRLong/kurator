import os
import sqlite3

import pytest

from kurator.lib.record import SqliteRecord

DB_NAME = 'test_mesh_records.db'


class Test_Record:

    @pytest.fixture(autouse=True)
    def setup(self, tmpdir):
        self.record = SqliteRecord(os.path.join(tmpdir, DB_NAME))
        self.connection = sqlite3.connect(os.path.join(tmpdir, DB_NAME))
        self.cursor = self.connection.cursor()

        yield self.record
        self.connection.close()
        os.remove(os.path.join(tmpdir, DB_NAME))

    @pytest.fixture
    def add_records(self):
        self.cursor.execute("""
        INSERT OR REPLACE INTO Updates (
            'update_id',
            'ticket_key',
            'ticket_id',
            'file_name',
            'author',
            'size',
            'created',
            'status',
            'executed'
        ) VALUES 
            ("43462","AN-5443","65733","file1.sql","Chris","299","2018-03-07T10:51:15.237-0500","Done",0),
            ("43428","AN-5403","65646","file2.sql","Sean","117","2018-03-05T13:10:46.215-0500","Review",0),
            ("43299","AN-5388","65623","file3.sql","Chris","21","2018-02-23T09:58:18.837-0500","Doing",0),
            ("43235","AN-5360","65567","file4.sql","Michael","1336","2018-02-16T15:50:11.462-0500","Done",1),
            ("43210","AN-5351","65551","file5.sql","Michael","1334","2018-02-15T16:17:55.255-0500","Done",1)
        """)
        self.connection.commit()

    @pytest.mark.skip(reason="not implemented")
    def test_create_photos_table(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name={};".format(SqliteRecord.DATABASE_NAME))
        assert len(self.cursor.fetchall()) == 1
        self.record.close()

    @pytest.mark.skip(reason="not implemented")
    def test_create_record(self):
        self.record.create_record({
            'file_id': 1234,
            'ticket_key': 'AN-1234',
            'ticket_id': 4567,
            'file_name': 'file_name',
            'author': 'name',
            'size': 500,
            'created': '2018-01-01',
            'ticket_status': 'Done',
        })
        self.cursor.execute("SELECT count(*) from Updates")
        assert self.cursor.fetchone()[0] == 1
        self.record.close()

