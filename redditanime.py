# get reccomendations from ledit
import requests
import json
import praw
from commentanalyzer import analyzeComment

reddit = praw.Reddit(client_id='kAk3NtbA5iIJRg',
                     client_secret='x9VUTpnE6HeSMK7vJqjx4DN29ZA',
                     user_agent='my user agent')


subreddit = reddit.subreddit('Animesuggest')

#for submission in subreddit.top(limit=1):
    #print(submission.title)

searchRecs = subreddit.search('(flair:"What to Watch?" OR flair:"Request") title:"Fate Zero"', sort='top')

for recs in searchRecs:
    for comment in recs.comments:
        analyzeComment(comment.body, comment.score)
        break
    break


