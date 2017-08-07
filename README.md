# User history archiver for reddit

## Installation

* Install sqlite3
* Install the sqlite3 lib for python3
* Install configparser lib for python3

## Set up

* Create your main database `touch database.db; sqlite3 database.db < make_database.sql`
* Create a dir for your tmp databases `mkdir ./tmp_dbs`
* Create your config file with the name "config.ini" and the following format

[dbs]

db_path = The path to your main database

tmp_db_path = The path to your tmp DB dir. This should not have a trailing / and should be empty of anything but your temporary databases

[creds_1]

username = Your username

client_id = Your client ID

client_secret = Your client secret

user_agent = Your user_agent

There is an example config file in this repo

## Speeding up

By default this install will be very slow if you try to retrieve data from your main DB, if you wish to speed it up you should index
the author, subreddit, link_title, created and score columns

# Tools

There are several tools in this repo for maintaining and retrieving information from your database

* dedupe_db.py will remove duplicate entries from your database
* dump_usernames.py will print every username in your database
* report.py will generate a simple report on a user using infomation from your database
* history_ripper.py will rip various users histories. It's usage is `python3 history_ripper.py -u $username_list --creds $creds_entry --db $tmp_database_name`, where creds_entry is the name of the section where you put your creds in config.ini
