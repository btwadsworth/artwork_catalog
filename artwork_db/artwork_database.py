# Manage the artwork database
import sqlite3

from .artwork_db_config import db_path
from exceptions.duplicate_artwork_error import DuplicateArtworkError
from exceptions.artwork_dne_error import ArtworkDNEError
from artist_db import artists_database

db = db_path

class SQLiteArtworkDB():

    def __init__(self):
        with sqlite3.connect(db) as con:
            con.execute('create table if not exists all_artwork (artist TEXT, artwork TEXT, price INTEGER, availability INTEGER)')
    

    def insert(self, artist, artwork, price, availability):
        artists_DB = artists_database.SQLiteArtistsDB()
        artist_exists = artists_DB.search(artist)
        if artist_exists is None:
            print('Artist does not exist.\nNeed to add artist first.')
            email = input('Enter artist email: ')
            artists_DB.insert(artist, email)

        with sqlite3.connect(db) as con:
            artwork_cursor = con.execute('select * from all_artwork where artwork like ?', artwork)
            artworks = artwork_cursor.fetchall()
        con.close()

        if artworks is not None:
            raise DuplicateArtworkError(f'An artwork named {artwork} already exists in the table.')

        with sqlite3.connect(db) as con:
            con.execute('insert into all_artwork values (?, ?, ?, ?)')
        con.close()
        return 'Artwork successfully added to table.'


    def search(self, artist):
        with sqlite3.connect(db) as con:
            artwork_cursor = con.execute('select * from all_artwork where artist like ?', artist)
            artwork = artwork_cursor.fetchall()
        con.close()
        print('All artwork by: ', artist)
        for art in artwork:
            print(art)
        
        
    def display(self, artist):
        with sqlite3.connect(db) as con:
            artwork_cursor = con.execute('select * from all_artwork where artist like ? and availability == 1', artist)
            artwork = artwork_cursor.fetchall()
        con.close()
        print('Available artwork by: ', artist)
        for art in artwork:
            print(art)
    

    def delete(self, artwork):
        with sqlite3.connect(db) as con:
            artwork_cursor = con.execute('select * from all_artwork where artwork like ?', artwork)
            art = artwork_cursor.fetchall()
            if art is not None:
                con.execute('delete * from all_artwork where artwork like ?', artwork)
            else:
                raise ArtworkDNEError('Artwork does not exist in database.')
        con.close()
        

    def update(self, artwork):
        try:
            with sqlite3.connect(db) as con:
                rows_mod = con.execute('update all_artwork set availability = 0 where artwork like ?', artwork)
            con.close()
            return rows_mod
        except Exception:
            raise ArtworkDNEError('Artwork does not exist')
        
    
