from bs4 import BeautifulSoup
import requests
import sqlite3
import sys
from datetime import datetime
import json

print('BILLBOARD -- HOT 100\n')
# get the top 100 songs from the web page

# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(baseurl):
  return baseurl

def make_request_using_cache(baseurl):
    unique_ident = get_unique_key(baseurl)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def call_cache():
    baseurl = 'https://www.billboard.com'
    list_url = baseurl + '/charts/hot-100'
    page_text = make_request_using_cache(list_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    #print(page_soup)

    searching_div = page_soup.find(class_ = 'chart-data js-chart-data')
    print(searching_div)
    container_div = searching_div.find(class_ = 'container')
    print(container_div)
    within_cont = container_div.find_all(class_ = 'chart-row__title')
    print(within_cont)


# 5 fields = title, rank, picture, artist, date
class Song:
    def __init__(self, song_title, song_artist, song_rank, song_picture, today_date):
        self.title = song_title
        self.artist = song_artist
        self.rank = song_rank
        self.picture = song_picture
        self.date = today_date

    def __str__(self):
        str_ = self.title + ' by ' + self.artist + ' ranked ' + self.rank + " on " + self.date
        return str_

def init_db():
    #DBNAME = 'music.db'
    music_file = 'music_db.sqlite'
    conn = sqlite3.connect(music_file)
    cur = conn.cursor()

    statement = '''
        CREATE TABLE 'Songs' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'SongTitle' TEXT NOT NULL,
            'SongRank' TEXT NOT NULL,
            'SongPicture' TEXT,
            'SongDate' TEXT,
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Artists' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'SongArtist' TEXT NOT NULL,
                'SongId' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()

    conn.close()

    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        print('Deleting db and starting over from scratch.')
        init_db()
    else:
        print('Leaving the DB alone.')

def insert_stuff():
    music_file = 'music_db.sqlite'
    conn = sqlite3.connect(music_file)
    cur = conn.cursor()
    with open('cache.json') as jsonDataFile:
        readjson = jsonDataFile.read()
        gettingjson = json.loads(readjson)

    for x in cache_file:
        SongTitle = Song['Song_Name']
        SongArtist = Song['Song_Artist']
        SongRank = Song['Song_Rank']
        SongDate = Song['Song_Date']

    for Song in Songs:
        insertion = (None, SongTitle, SongRank, SongDate)
        statement = 'INSERT INTO "Songs" '
        statement += 'VALUES (?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

        insertion2 = (None, SongTitle, SongArtist)
        statement = 'INSERT INTO "Artists" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def query_make():
#queries
    music_file = 'music_db.sqlite'
    conn = sqlite3.connect(music_file)
    cur = conn.cursor()
    cur.execute = ('SELECT SongTitle, SongRank FROM Songs')
    print (cur.fetchall())
    cur.execute('SELECT SongArtist FROM Artists')
