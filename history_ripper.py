#!/usr/bin/python3

import praw
import sqlite3
import sys
import argparse
import string
import random
import configparser
import os
parser = argparse.ArgumentParser(description='Download reddit users history')
parser.add_argument("-u", help="Username file")
parser.add_argument("--creds", help="What creds to use")
parser.add_argument("--db", help="What tmp db to write to")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read("config.ini")

if args.db == None:
    print("DB name need")
    sys.exit()


print("[*] Logging in as {}".format(config[args.creds]["username"]))
r = praw.Reddit(client_id=config[args.creds]["client_id"],
                client_secret=config[args.creds]["client_secret"],
                user_agent=config[args.creds]["user_agent"],
                username=config[args.creds]["username"])

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


look_up_database = sqlite3.connect(config["dbs"]["db_path"])
lookup_cursor = look_up_database.cursor()

temp_file_name = args.db
with open(args.u) as f:
    usernames = f.read().splitlines()
if not os.path.isfile("{0}/{1}.db".format(config["dbs"]["tmp_db_path"], temp_file_name)):
    print("[*] Making database {}.db".format(temp_file_name))
    conn = sqlite3.connect("{}/{}.db".format(config["dbs"]["tmp_db_path"], temp_file_name))
    make_db = open("make_database.sql", "r").read()
    conn.execute(make_db)
    print("[*] Database made")
conn = sqlite3.connect("{}/{}.db".format(config["dbs"]["tmp_db_path"], temp_file_name))
cursor = conn.cursor()

# This x is here for our current user count
x = 1
for username in usernames:
    try:
        user = r.redditor(username)
        cursor.execute('begin')
        print("[*] Archiving user #{} of {}".format(x, len(usernames)))
        for comment in user.comments.new(limit=None):
            lookup_cursor.execute("SELECT comment_id FROM userinfo WHERE comment_id = ?", (comment.id,))
            data=lookup_cursor.fetchall()
            if len(data) != 0:
                print("[*] Comment with ID {} already exists".format(comment.id))
                print("[*] Commiting changes")
                conn.commit()
                break
            print("[*] Adding comment with ID {} from user {}".format(comment.id, comment.author))
            cursor.executemany("INSERT INTO userinfo(author, subreddit, subreddit_id, comment_id, link_title, author_flair_text, body, created, score) VALUES(?,?,?,?,?,?,?,?,?) ", ([str(comment.author), str(comment.subreddit), str(comment.subreddit_id), str(comment.id), str(comment.link_title), str(comment.author_flair_text), str(comment.body), comment.created, comment.score],))
    except:
        print("Account has been deleted")
    x = x + 1
print("[*] Commiting changes")
conn.commit()
