#!/usr/bin/python3

import sqlite3
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

conn = sqlite3.connect(config["dbs"]["db_path"])
cursor = conn.cursor()

for i in os.listdir("{}/".format(config["dbs"]["tmp_db_path"])):
    print("[*] Combining {} and comments.db".format(i))
    cursor.execute("attach '{}/{}' as t".format(config["dbs"]["tmp_db_path"], i))
    cursor.execute("insert into userinfo(author, subreddit, subreddit_id, comment_id, link_title, author_flair_text, body, created, score) select author, subreddit, subreddit_id, comment_id, link_title, author_flair_text, body, created, score from t.userinfo")
    cursor.execute("detach t")
    print("[*] Deleting {}".format(i))
    os.remove("{}/{}".format(config["dbs"]["tmp_db_path"], i))
