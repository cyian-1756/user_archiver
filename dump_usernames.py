import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

main_db = config["dbs"]["db_path"]

db = sqlite3.connect(main_db)
cursor = db.cursor()

cursor.execute("SELECT author FROM userinfo GROUP by author")
data=cursor.fetchall()

for i in data:
    print(i[0])
