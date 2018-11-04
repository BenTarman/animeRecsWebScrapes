
# find anime names in the comment
# assumes mentioned animes are reccomended (maybe too big assumption :/)
import re
import psycopg2

conn = psycopg2.connect("dbname=anime_recs user=eango host='localhost' password=Ooleasta222!")

curr = conn.cursor()

def analyzeComment(comment, num_recs):

    #num_recs is currently represented as num upvotes ()

    #set that stores the strings of animes that the user is
    #potentially recommending.
    possible_anime_recs = set()

    # Any links are likely to be links to anime shows
    possibleAnime_links_title = re.findall('\[.*?\]',comment)
    possibleAnime_links = re.findall('\[.*?\]\(.*?\)',comment)

    for possible_anime in possibleAnime_links:
        myanimelist_link = re.findall('myanimelist.net/anime/\d+', possible_anime)
        if myanimelist_link != []:
            possible_anime_id = myanimelist_link[0].split('/')[-1]
            queryText = "select * from anime where anime_id='{0}'"\
                            .format(possible_anime_id)

            curr.execute(queryText);
            result = curr.fetchone()
            if result is not None:
                #result exists so make entry in recommended anime table
                print('query result', result)

                #place shit in (something like this probably)
                """
                queryText = "insert into recommended_anime values ({0},'{1}',{2},'{3}','{4}')"\
                .format(
                    rec_anime_id, anime_id, num_recs, comment, "reddit")
                curr.execute(queryText);
                """








    #curr.execute(queryText);
    #print(possible_anime_recs)






