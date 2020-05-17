# Setup a empty DB with the needed rows
from dotenv import load_dotenv
import sqlite3, os

QUERYS = [  'CREATE TABLE "tournaments" ' +
                '("id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"idDiscord"  TEXT(30) NOT NULL,"league"  TEXT(100),"tournament"  TEXT(100),"goblinValue"  TEXT(100));',
            'CREATE TABLE "coaches" ' +
                '( "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "idDiscord"  TEXT NOT NULL, "coachName"  TEXT, "discordName"  TEXT, CONSTRAINT "idDiscord");'
        ]





load_dotenv()
connect = sqlite3.connect(os.getenv('SQLITE_CONNECTION'))
cursor = connect.cursor()
for query in QUERYS: 
    cursor.execute(query)

connect.commit()
cursor.close()