import requests
from bs4 import BeautifulSoup
import sqlite3


def write_output(file):
    with open('new.html', 'a') as fout:
        with open(file, 'r') as fin:
            content = fin.read()
            fout.write(content)


def get_html_from_web(page):
    page = page + 1
    url = 'http://www.hdtracks.com/new?p=' + str(page)
    response = requests.get(url)
    return response.text


def get_artist_info_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    ret_str = ''

    db = sqlite3.connect('albums.db')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY, artist TEXT, album_name TEXT, sample_rate TEXT
        )'''
                   )
    db.commit()
    # the div w/ class 'item' has each new album
    for item in soup.select('.item'):

        img = item.find('img')

        # the h2 has the album name
        h2 = item.find('h2')
        album_name = h2.text

        # grab the 'a href' text for the artist name
        div = item.find('div', {'class': 'detail-item artist-name'})
        a = div.find('a')

        # empty 'a' tags cause a crash
        if a is None:
            artist_name = ':: no artist listed ::'
        else:
            artist_name = a.text

        sample_rate_div = item.find('div', {'class': 'detail-item'})
        sample_string = sample_rate_div.text
        sample_string = sample_string.replace('Sample rate(s):', '')
        sample_string = sample_string.strip()
        # if we have made it this far we should have the three pieces of
        # info we are looking for ...
        #
        # query the database to see if this item already exists
        # if so .... continue
        # else add to db and
        # put a ret_str together

        # print(f'{artist_name} : {album_name} : {sample_string}')

        cursor.execute('''SELECT artist, album_name FROM items WHERE artist=? AND album_name=?''',
                       (artist_name, album_name))
        album = cursor.fetchone()
        if album:
            # already have seen this as it is already in the database
            continue
        else:
            # not seen, so put it in the database then move on to construct the output string
            cursor.execute('''INSERT INTO items(artist, album_name, sample_rate) VALUES(?,?,?)''',
                (artist_name, album_name, sample_string))
            db.commit()

        if sample_string == '44.1kHz/16bit':
            # but we are going to skip this one anyway if it
            # is merely CD quality
            continue
        else:
            # 2019.02.21
            # https://www.amazon.com/s?k=al+stewart+early + years
            ret_str = ret_str + str(img) + '<p class="artist">' + artist_name + '</p>' + \
                      '<p class="album"><a href="https://www.amazon.com/s?k=' + artist_name + ' ' + album_name + '">' + album_name + '</a></p>' + \
                      '<p class="encoding">' + sample_string + '</p>' + \
                      '<hr />'
    db.close()
    return ret_str
