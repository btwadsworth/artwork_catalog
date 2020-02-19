from artist_db.artists_database import SQLiteArtistsDB
from artwork_db.artwork_database import SQLiteArtworkDB
from exceptions.artwork_dne_error import ArtworkDNEError
from exceptions.duplicate_artist_error import DuplicateArtistError
from exceptions.duplicate_artwork_error import DuplicateArtworkError

global artist_db
global artwork_db


def main():
    global artist_db, artwork_db
    print('*** ARTWORK CATALOG ***')
    artist_db = SQLiteArtistsDB()
    artwork_db = SQLiteArtworkDB()

    while True:
        menu()
        response = input('Choice: ')
        if response == '1':
            add_artist()
        elif response == '2':
            search_all()
        elif response == '3':
            display()
        elif response == '4':
            add_artwork()
        elif response == '5':
            delete()
        elif response == '6':
            change()
        elif response == '7':
            break
        else:
            print('Invalid Choice')



def menu():
    print('\n***************************************')
    print('1: Add New Artist')
    print('2: Search For All Artwork By Artist')
    print('3: Display Available Artwork By Artist')
    print('4: Add New Artwork')
    print('5: Delete An Artwork')
    print('6: Change Availability Of An Artwork')
    print('7: Exit')
    print('***************************************')


def add_artist():
    name = ''
    email = ''
    while name == '':
        name = input('Enter artist name: ')
    while email == '':
        email = input('Enter email address: ')
    try:
        artist_db.insert(name, email)
    except DuplicateArtistError:
        print(DuplicateArtistError)


def search_all():
    name = ''
    while name == '':
        name = input('Enter artist name: ')
    artwork_db.search(name)


def display():
    name = ''
    while name == '':
        name = input('Enter artist name: ')
    artwork_db.display(name)


def add_artwork():
    name = ''
    artwork_name = ''
    price = ''
    avail = ''
    while name == '':
        name = input('Enter artist name: ')
    while artwork_name == '':
        artwork_name = input('Enter artwork name: ')
    while not price.isdigit():
        price = input('Enter price (Whole Integer): ')
    price = int(price)
    while avail != '0' and avail != '1':
        avail = input('Availability (0 = sold or 1 = available): ')
    avail = int(avail)
    try:
        artwork_db.insert(name, artwork_name, price, avail)
    except DuplicateArtworkError:
        print(DuplicateArtworkError)


def delete():
    artwork_name = ''
    while artwork_name == '':
        artwork_name = input('Enter artwork name: ')
    try:
        artwork_db.delete(artwork_name)
    except ArtworkDNEError:
        print(ArtworkDNEError)


def change():
    artwork_name = ''
    while artwork_name == '':
        artwork_name = input('Enter sold artwork name: ')
    try:
        artwork_db.update(artwork_name)
    except ArtworkDNEError:
        print(ArtworkDNEError)


if __name__ == '__main__':
    main()