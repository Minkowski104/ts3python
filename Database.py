from datetime import datetime
import sqlite3

from configuration import DATABASE_NAME
from Client import Client


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(f'{DATABASE_NAME}.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            try:
                self.cursor.execute(f'CREATE TABLE {DATABASE_NAME} '
                                    f'('
                                    f'database_id text,'
                                    f'unique_id text,'
                                    f'b64_uid text,'
                                    f'nickname text,'
                                    f'measurement_start integer,'
                                    f'connected_total real,'
                                    f'connected_afk real'
                                    f')')
            except sqlite3.OperationalError:
                return

    def create_profile(self, client: Client):
        if self.get_profile(client) is not None:
            return

        with self.connection:
            self.cursor.execute(f'INSERT INTO {DATABASE_NAME} VALUES ('
                                f'"{client.db_id}",'
                                f'"{client.uid}",'
                                f'"{client.b64_uid}",'
                                f'"{client.name}",'
                                f'{int(datetime.now().timestamp())},'
                                f'0.0,'
                                f'0.0)')

        return self.get_profile(client)

    def get_profile(self, client: Client):
        if client is None:
            return

        self.cursor.execute(f'SELECT * FROM {DATABASE_NAME} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return self.cursor.fetchone()

    def get_profile_total(self, client: Client):
        if client is None:
            return
        self.cursor.execute(f'SELECT connected_total '
                            f'FROM {DATABASE_NAME} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return self.cursor.fetchone()[0]

    def get_profile_afk(self, client: Client):
        if client is None:
            return
        self.cursor.execute(f'SELECT connected_afk '
                            f'FROM {DATABASE_NAME} '
                            f'WHERE b64_uid="{client.b64_uid}"')
        return self.cursor.fetchone()[0]

    def update_profile_total(self, client: Client, total: float):
        if client is None:
            return

        with self.connection:
            self.cursor.execute(f'UPDATE {DATABASE_NAME} '
                                f'SET connected_total = {total} '
                                f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)

    def update_profile_afk(self, client: Client, afk: float):
        if client is None:
            return

        with self.connection:
            self.cursor.execute(f'UPDATE {DATABASE_NAME} '
                                f'SET connected_afk = {afk} '
                                f'WHERE b64_uid="{client.b64_uid}"')

        return self.get_profile(client)