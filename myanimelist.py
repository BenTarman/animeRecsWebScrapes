"""
this ugly program makes a really big database using data
from myanimelist. This ugly program will re-run once in a while to 
update data for animes to be as recent as possible
"""
import requests
from bs4 import BeautifulSoup
import sys
import time
import psycopg2

dbpassword = sys.argv[1] #send password from command line
conn = psycopg2.connect("dbname=anime_recs user=eango host='ec2-18-212-22-176.compute-1.amazonaws.com' password='{0}'"\
                        .format(dbpassword))

conn.autocommit = True # autocommit any statement to save uh time
curr = conn.cursor()

# make database tables and shit
def initTables():

    #sql bullshit here

    #make anime table
    curr.execute("drop table if exists anime cascade;");
    queryText =  "CREATE TABLE Anime"\
                 "("\
                 "anime_id integer primary key,"\
                 "name VARCHAR(255),"\
                 "score double precision" \
                 ");"
    curr.execute(queryText);

    #make anime rec table
    curr.execute("drop table if exists recommended_anime;");
    queryText =  "CREATE TABLE recommended_anime ("\
                 "rec_anime_id integer,"\
                 "anime_id integer not null references anime(anime_id),"\
                 "perc_recs decimal(18, 4),"\
                 "rec_text text"\
                 ");"
    curr.execute(queryText);

initTables()

def ParseAnimeShow(url):
    #from the link we can get the unique id for db to use
    parsed_link = url.split('/')
    anime_id = parsed_link[len(parsed_link) - 2]
    page = requests.get(url)

    if (page.status_code != 200):
        print("page status: ", page.status_code)
        sys.exit()

    soup = BeautifulSoup(page.text, 'html.parser')

    # replace single quote with double so database no fail insert
    anime_name = soup.find('span', {'itemprop' : 'name'}).text
    anime_name = anime_name.replace("'", "''")

    anime_score = float(soup.find('div', {'class' : 'fl-l score'}).text.strip())

    queryText = "insert into anime values ({0}, '{1}', {2})".format(anime_id,
                                                            anime_name, anime_score)
    curr.execute(queryText);

    time.sleep(5)
    url += '/userrecs'
    page = requests.get(url)

    if (page.status_code != 200):
        print("page status: ", page.status_code)
        sys.exit()

    soup = BeautifulSoup(page.text, 'html.parser')

    #store total recs to calculate percentages make sure to clear each iteration
    num_recs_arr = []

    for elem in soup.find_all('div', {'class', 'borderClass'}):

        animeRecName = elem.find('strong')
        link = elem.find('a', href=True)['href']
        parsed_link = link.split('/')
        animeLinkName = parsed_link[len(parsed_link) -1]

        recs = elem.find('div', {'class', 'spaceit'})
        num_recs = 1
        if recs is not None:
            num_recs = int(recs.find('strong').text)

        rec_text = elem.find('div', {'class' : 'spaceit_pad detail-user-recs-text'}).text.strip()
        rec_text = rec_text.replace("'", "''")

        if animeRecName is not None:
            rec_anime_id = parsed_link[len(parsed_link) - 2]

            queryText = "insert into recommended_anime values ({0},'{1}',{2},'{3}')"\
            .format(
                rec_anime_id, anime_id, 'null', rec_text)
            curr.execute(queryText);
            num_recs_arr.append((num_recs, rec_anime_id))

    # CONVERT NUM_RECS TO PERCENTAGE (more fair to newer animes)
    for recNum, recId in num_recs_arr:
        perc_rec = int(recNum) / sum([x for x,_ in num_recs_arr])
        perc_rec *= 100
        print(recId, perc_rec)


        queryText = "update recommended_anime set perc_recs={0} where rec_anime_id={1}"\
                .format(perc_rec, recId)

        curr.execute(queryText);


# MAIN PROGRAM STARTS HERE

limit = 0
while limit != 14700:
    time.sleep(10)
    #get data from topanime part of site
    url='https://myanimelist.net/topanime.php?limit=' + str(limit)

    page = requests.get(url)

    if (page.status_code != 200):
        print("page status: ", page.status_code)
        sys.exit()

    soup = BeautifulSoup(page.text, 'html.parser')

    # group of html from which we extract further data from
    anime_forms = soup.find_all('td', {'class' : 'title al va-t word-break'})

    for elem in anime_forms:
        link = elem.find('a', href=True)['href']

        #sleep so server isn't spammed with requests
        time.sleep(10)

        # function further parses anime and adds it to database
        ParseAnimeShow(link)
    limit += 50


print("FINISHED MAKING DATABASE DATABASE WOW WOW")

#close db
curr.close()

