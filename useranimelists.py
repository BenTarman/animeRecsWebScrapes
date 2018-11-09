import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import psycopg2

# user format will be in big table...
# (user, anime_id, score)
# then from other tables you can get more info about anime from the anime_id
# maybe expand to user table later if you want easier integration of accounts


dbpassword = sys.argv[1]  # send password from command line


conn_text = "dbname=anime_recs user=eango "\
            "host='ec2-18-212-22-176.compute-1.amazonaws.com' "\
            "password='{0}'".format(dbpassword)

conn = psycopg2.connect(conn_text)
conn.autocommit = True  # autocommit any statement to save uh time
curr = conn.cursor()


# make database tables and shit
def init_tables():
    # sql bullshit here
    curr.execute("drop table if exists user_ratings;")
    query_text = "CREATE TABLE user_ratings"\
                 "("\
                 "user_name VARCHAR(255),"\
                 "anime_id integer,"\
                 "score integer" \
                 ");"
    curr.execute(query_text)


init_tables()


def get_user_list(url, user):

    page = requests.get(url)
    anime_id = re.findall(r'anime_id&quot;:\d+,&quot', page.text)
    anime_id = [int(re.findall(r'\d+', elem)[0]) for elem in anime_id]

    score = re.findall(r'score&quot;:\d+,&quot', page.text)
    score = [int(re.findall(r'\d+', elem)[0]) for elem in score]
    result = [(user, x, y) for x, y in zip(anime_id, score)]
    if result == []:
        print('invalid for user ', user)
    else:
        for x in result:
            query_text = "insert into user_ratings values"\
                         " ('{0}', {1}, {2})".format(x[0], x[1], x[2])

            curr.execute(query_text)


for i in range(0, 240 + 1, 24):
    url = 'https://myanimelist.net/users.php?'
    'q=&loc=&agelow=0&agehigh=0&g=1&show=' + str(i)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    usersTable = soup.findAll('td', {'class', 'borderClass'})

    for userentry in usersTable:
        user = userentry.find('a').text

        url = 'https://myanimelist.net/animelist/' + user + '?status=2'
        get_user_list(url, user)
        time.sleep(2)
