import requests
from bs4 import BeautifulSoup
import sys
import time
import psycopg2

dbpassword = sys.argv[1]  # send password from command line

conn_text = "dbname=anime_recs user=eango "\
            "host='ec2-18-212-22-176.compute-1.amazonaws.com' "\
            "password='{0}'".format(dbpassword)

conn = psycopg2.connect(conn_text)
conn.autocommit = True  # autocommit any statement to save uh time
curr = conn.cursor()

# make database tables and shit


def init_tables():

    curr.execute("drop table if exists genres cascade;")
    query_text = "CREATE TABLE genres"\
                 "("\
                 "id integer primary key,"\
                 "genre VARCHAR(255)"\
                 ");"
    curr.execute(query_text)


init_tables()

url = 'https://myanimelist.net/anime.php'
page = requests.get(url)

if (page.status_code != 200):
    print("page status: ", page.status_code)
    sys.exit()

soup = BeautifulSoup(page.text, 'html.parser')

genreHTML = soup.find('div',
                      {'class': 'genre-link'}).find_all(
                          'div', {'class': 'genre-list al'})

cnt = 0
for elem in genreHTML:
    cnt += 1
    idx = elem.text.find('(') - 1
    genre = elem.text[:idx]
    query_text = "insert into genres values ({0}, '{1}')".format(cnt, genre)
    curr.execute(query_text)
