import sqlite3

from .artists_db_config import db_path
from exceptions.duplicate_artist_error import DuplicateArtistError

db = db_path

class SQLiteArtistsDB():
    
    def __init__(self):
        with sqlite3.connect(db) as con:
            con.execute('create table if not exists artists (name TEXT UNIQUE NOT NULL, email TEXT)')

    def insert(self, name, email):
        try:
            with sqlite3.connect(db) as con:
                rows_mod = con.execute('insert into artists values (?, ?)', (name, email))
            con.close()
            return rows_mod
        except sqlite3.IntegrityError:
            raise DuplicateArtistError(f'Error inserting: Duplicate artist will not be added. Name: {name}') # Duplicate artist

    def search(self, name):
        with sqlite3.connect(db) as con:
            artists_cursor = con.execute('select * from artists where name like ?', name)
            artist = artists_cursor.fetchall()
        con.close()
        return artist