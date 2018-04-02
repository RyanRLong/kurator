"""
Module containing sqlite abstract and concrete classes.
"""
import sqlite3
import os
import datetime

class SqliteRecord():
    """
    Represents a Sqlite Database of updates
    """

    DATABASE_PATH = os.path.join(os.getenv('LOCALAPPDATA'), 'Kurator')
    DATABASE_NAME = 'kurator.db'
    TABLE_NAME = 'photos'

    def __init__(self, db_path=None):
        """
        Opens the database in sqlite3 database in db_path
        :param db_path: optional; specify the absolute path  of the database
        you want to use
        """
        self.db_path = self.create_database_if_not_exist(db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_updates_table()

    @staticmethod
    def create_database_if_not_exist(db_path):
        """
        Open or creates database in AppData/Local unless a
        db_path is specified
        :param db_path:
        :return: absolute path of the database
        """
        if not db_path or db_path is None:
            db_dir = SqliteRecord.DATABASE_PATH
            if not os.path.exists(db_dir): # pragma: no cover
                os.makedirs(db_dir)
            db_path = os.path.join(db_dir, SqliteRecord.DATABASE_NAME)
        return db_path

    def close(self):
        """
        Closes the database connection
        :return:
        """
        self.cursor.close()
        self.connection.close()

    def create_updates_table(self):
        """
        Creates the Updates table
        :return:
        """
        sql = """
        CREATE TABLE if not exists {} (
        `id` TEXT NOT NULL PRIMARY KEY,
        `created_date` TEXT,
        `model` TEXT,
        `orientation` TEXT,
        `path` TEXT,
        `imported_date` TEXT,
        `tags` TEXT 
        );
        """.format(SqliteRecord.TABLE_NAME)
        self.cursor.execute(sql)
        self.connection.commit()

    def record_exists(self, media_id):
        """
        Returns true if record exists
        :param media_id:
        :return:
        """
        sql = """
        SELECT id FROM {} WHERE id = '{}' LIMIT 1;
        """.format(SqliteRecord.TABLE_NAME, media_id)
        self.cursor.execute(sql)
        return self.cursor.fetchone() is not None


    def create_record(self, data):
        """
        Creates a record in the database
        :param data: dictionary of data
        :return:
        """
        sql = """
        INSERT INTO {} (
            'id',
            'created_date',
            'model',
            'orientation',
            'path',
            'imported_date'
        ) VALUES (
            '{id}',
            '{created_date}',
            '{model}',
            '{orientation}',
            '{path}',
            '{imported_date}'
        );
        """.format(
            SqliteRecord.TABLE_NAME,
            id=data['id'],
            created_date=data['created_date'],
            model=data['model'],
            orientation=data['orientation'],
            path=data['file_path'],
            imported_date=datetime.datetime.now(),
        )
        self.cursor.execute(sql)
        self.connection.commit()
