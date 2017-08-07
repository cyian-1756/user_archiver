#!/usr/bin/python3

import sqlite3
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

main_db = config["dbs"]["db_path"]

def sql_removeduplicates():
    con = sqlite3.connect(main_db)
    with con:
        cur = con.cursor()
        cur.execute("SELECT comment_id, COUNT(*) c FROM userinfo GROUP BY comment_id HAVING c > 1")
        rows = cur.fetchall()
        con.commit()
        for row in rows:
            cur.execute("SELECT comment_id FROM userinfo WHERE comment_id = ?", (row[0],))
            rows_to_delete = cur.fetchall()
            for num in range(1, len(rows_to_delete)):
                for r in rows_to_delete:
                    cur.execute("DELETE FROM userinfo WHERE comment_id = ? LIMIT 1", (r[0],))
                    print("Deleting row with comment_id {}".format(r[0],))
                    break

sql_removeduplicates()
