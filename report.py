import sqlite3
import sys
import argparse
import configparser
import re
from datetime import datetime
import operator
parser = argparse.ArgumentParser(description='Report generator')
parser.add_argument("-u", help="Username")
parser.add_argument("--detailed-links", help="Generate a detailed report on links the user has posted")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read("./config.ini")

def print_links(site, cursor, sitename, username, regex="[a-zA-Z0-9_#/-\?=]*"):
    cursor.execute("SELECT body, subreddit, comment_id, subreddit_id FROM userinfo WHERE author = ? AND body glob ?", (username, "[a-z]*://*{}/*".format(site)))
    rows = cursor.fetchall()
    if len(rows) != 0:
        print("###### {} links".format(sitename))
        print("Total {} links: {}".format(sitename, get_links_count(site, cursor, username, regex)))
        for row in rows:
            links = re.findall("[https|http|irc]*?[://]*?[www\\.]*?{}/{}".format(site, regex), row[0])
            for i in links:
                print("* {}".format(i))

def print_links_detailed(site, cursor, sitename, username, regex="[a-zA-Z0-9_#/-\?=]*"):
    cursor.execute("SELECT body, subreddit, comment_id, subreddit_id FROM userinfo WHERE author = ? AND body glob ?", (username, "[a-z]*://*{}/*".format(site)))
    rows = cursor.fetchall()
    if len(rows) != 0:
        print("###### {} details".format(sitename))
        print("<table style=\"width:100%\"> \
         <tr> \
           <th>Links</th> \
           <th>Body</th> \
           <th>Subreddit</th> \
           <th>Comment_id</th> \
           <th>Subreddit_id</th> \
         </tr>")
        for row in rows:
            links = re.findall("[https|http|irc]*?[://]*?[www\\.]*?{}/{}".format(site, regex), row[0])
            print("<tr>\
               <td>{links}</td>\
               <td>{body}</td>\
               <td>{subreddit}</td>\
               <td>{comment_id}</td>\
               <td>{subreddit_id}</td>\
             </tr>".format(links=links, body=row[0].replace("\n", "<br>"), subreddit=row[1], comment_id=row[2], subreddit_id=row[3]))
        print("</table>")

def get_links_count(site, cursor, username, regex="[a-zA-Z0-9_#/-\?=]*"):
    cursor.execute("SELECT body FROM userinfo WHERE author = ? AND body glob ?", (username, "[a-z]*://*{}/*".format(site)))
    rows = cursor.fetchall()
    if len(rows) != 0:
        return len(rows)

def get_comments_by_score(cursor, username):
     cursor.execute("select * from userinfo where author = ? order by score", (username,))
     rows = cursor.fetchall()
     return rows

def get_all_links(cursor, username):
    cursor.execute("SELECT body FROM userinfo WHERE author = ? AND body glob '[a-z]*://*[a-zA-Z0-9-]*/*'", (username,))
    rows = cursor.fetchall()
    if len(rows) != 0:
        print("###### All links")
        for row in rows:
            links = re.findall("[a-zA-Z]*?[://]*?[www\\.]*?[a-zA-Z0-9-\\.]*\\.[a-z0-9A-Z]\S*", row[0])
            for i in links:
                print("* {}".format(i))

def get_tor_links(cursor, username):
    cursor.execute("SELECT body FROM userinfo WHERE author = ? AND body glob ?", (username, "[a-z]*://*.onion/*"))
    rows = cursor.fetchall()
    if len(rows) != 0:
        print("###### Onion links")
        for row in rows:
            links = re.findall("[https|http|irc]*?[://]*?[www\\.]*?\S*\\.onion\S".format(site, regex), row[0])
            for i in links:
                print("* {}".format(i))


def comments_per_sub(cursor, username):
    cursor.execute("SELECT subreddit FROM userinfo WHERE author = ?", (username,))
    data=cursor.fetchall()
    d = {}
    for i in data:
        if i[0] not in d:
            d[i[0]] = 1
        else:
            d[i[0]] += 1
    return d

def number_of_subreddits_posted_in(cursor, username):
    cursor.execute("SELECT subreddit FROM userinfo WHERE author = ?", (username,))
    data=cursor.fetchall()
    return len(set(data))

def karma_per_sub(cursor, username):
    cursor.execute("SELECT subreddit, score FROM userinfo WHERE author = ?", (username,))
    data=cursor.fetchall()
    d = {}
    for i in data:
        if i[0] not in d:
            d[i[0]] = i[1]
        else:
            d[i[0]] += i[1]
    return d

def total_recorded_comments(cursor, username):
    cursor.execute("SELECT comment_id FROM userinfo WHERE author = ?", (username,))
    data=cursor.fetchall()
    return len(data)



db = sqlite3.connect(args.db)
cursor = db.cursor()

username = args.u

print("# Report for {0}".format(username))
print("Generated on {0}".format(str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))))
print("\n")
print("---------")
print("\n")
print("Number of subreddits posted in: {}".format(number_of_subreddits_posted_in(cursor, username)))
print("\n")
print("Total recorded comments: {}".format(total_recorded_comments(cursor, username)))
print("\n")
print("###### Karma breakdown by subreddit")
karma_d = karma_per_sub(cursor, username)
sorted_karma = sorted(karma_d.items(), key=operator.itemgetter(1))
# [::1] reverses lists for some strange magic reason
for i in sorted_karma[::-1]:
    print("* {}: {}".format(i[0], i[1]))
print("\n")
print("###### Number of comments per subreddit")
comment_d = comments_per_sub(cursor, username)
sorted_comment = sorted(comment_d.items(), key=operator.itemgetter(1))
for i in sorted_comment[::-1]:
    print("* {}: {}".format(i[0], i[1]))

print_links(site="facebook.com", cursor=cursor, sitename="Facebook", username=args.u)
print_links(site="linkedin.com", cursor=cursor, sitename="Linkedin", username=args.u)
print_links(site="youtube.com", cursor=cursor, sitename="Youtube", username=args.u)
print_links(site="pornhub.com", cursor=cursor, sitename="Pornhub", username=args.u, regex="\S*")
print_links(site="github.com", cursor=cursor, sitename="Github", username=args.u)
print_links(site="gitlab.com", cursor=cursor, sitename="Gitlab", username=args.u)
print_links(site="twitter.com", cursor=cursor, sitename="Twitter", username=args.u)
print_links(site="imgur.com", cursor=cursor, sitename="Imgur", username=args.u)
print_links(site="wikileaks.org", cursor=cursor, sitename="Wikileaks", username=args.u)

if args.detailed_links:
    print_links_detailed(site="facebook.com", cursor=cursor, sitename="Facebook", username=args.u)
    print_links_detailed(site="linkedin.com", cursor=cursor, sitename="Linkedin", username=args.u)
    print_links_detailed(site="youtube.com", cursor=cursor, sitename="Youtube", username=args.u)
    print_links_detailed(site="pornhub.com", cursor=cursor, sitename="Pornhub", username=args.u, regex="\S*")
    print_links_detailed(site="github.com", cursor=cursor, sitename="Github", username=args.u)
    print_links_detailed(site="gitlab.com", cursor=cursor, sitename="Gitlab", username=args.u)
    print_links_detailed(site="twitter.com", cursor=cursor, sitename="Twitter", username=args.u)
    print_links_detailed(site="imgur.com", cursor=cursor, sitename="Imgur", username=args.u)
    print_links_detailed(site="wikileaks.org", cursor=cursor, sitename="Wikileaks", username=args.u)

get_tor_links(cursor, username)
get_all_links(cursor, username)
