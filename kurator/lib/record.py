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
            if not os.path.exists(db_dir):
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

    def fetch_not_executed_updates(self):
        """
        Fetches a list of all updates that have not
        been marked as executed
        :return: list of not executed records
        """
        sql = """
        SELECT update_id, ticket_key, file_name, author, size, created, status FROM Updates where executed = 0;
        """
        self.cursor.execute(sql)
        column_names = [i[0] for i in self.cursor.description]
        return [dict(zip(column_names, entry)) for entry in self.cursor.fetchall()]

    def fetch_executed_updates(self):
        """
        Fetches a list of all updates that have been
        marked as executed
        :return: list of executed records
        """
        sql = """
        SELECT update_id, ticket_key, file_name, author, size, created, status FROM Updates where executed = 1;
        """
        self.cursor.execute(sql)
        column_names = [i[0] for i in self.cursor.description]
        return [dict(zip(column_names, entry)) for entry in self.cursor.fetchall()]

    def set_as_executed(self, update_id):
        """
        Sets an update as executed
        :param update_id: the update_id of the record
        :return:
        """
        sql = """
        update Updates
        set executed = 1 where update_id = {};
        """.format(update_id)
        self.cursor.execute(sql)
        self.connection.commit()

    def set_as_not_executed(self, update_id):
        """
        Sets an update as not executed
        :param update_id:
        :return:
        """
        sql = """
        update Updates
        set executed = 0 where update_id = {};
        """.format(update_id)
        self.cursor.execute(sql)
        self.connection.commit()
