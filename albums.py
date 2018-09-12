import sqlite3

db = sqlite3.connect('albums.db')
cursor = db.cursor()
cursor.execute('''SELECT artist, album_name FROM items WHERE artist=? AND album_name=?''', ('Alison Moyet', 'Other'))
user = cursor.fetchone()
if user:
    print(user)
else:
    print('not found')
db.close()