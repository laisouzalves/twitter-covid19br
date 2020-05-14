# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:17:08 2020

@author: Andrei & Lais
"""

print("Running the scrapper")

import os
import pandas as pd
import tweepy
import re
import string
from textblob import TextBlob
import preprocessor as p
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

consumer_key= 'ixYO5kA7i5bXxwiHYFHQuHAPl'
consumer_secret= 'T5viTaE6DbZEWtiFmjMDB0HnxLDi4N1GbmIsGVqWUMsBeCSLim'
access_token= '309289991-ZLKo71IBEATWZiI2JQWAJRbSAHB4D6b8EFF9Msa7'
access_token_secret= 'rni6msscMhhvtzydhUW3DZwec9vQue2jTYPi8vefqroQc'

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth, wait_on_rate_limit=True,
#				   wait_on_rate_limit_notify=True)

# Post a tweet from Python
#api.update_status("Coé, tá funcionando o API?")
# Your tweet has been posted!

############
corona_tweets = "coronaBR.csv"
quarentena_tweets = "quarentenaBR-MAI.csv"

#columns of the csv file
COLS = ['id', 'created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang',
        'favorite_count', 'retweet_count', 'original_author', 'possibly_sensitive', 'hashtags',
        'user_mentions', 'place', 'place_coord_boundaries']

#set two date variables for date range
start_date = '2020-05-01' #seeks tweets from now until start_date
end_date = '2020-04-01' #unecessary - not using

#declare keywords as a query for three categories
corona_keywords = '#covid_19 OR #coronavirusnobrasil OR #CoronaVirus OR #covid19brasil OR #corona OR #covid19 OR #COVID-19 OR #COVID19 OR #coronavírus OR #coronavirus OR #covidbrasil OR #coronabrasil'
quarentena_keywords = '#FiqueEmCasaCaralho OR #stayathome OR #fiqueemcasa OR #stayhome OR #isolamento OR #isolamentosocial OR #trabalhedecasa OR #trabalhardecasa OR #quarentena OR #homeoffice'

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)

#mrhod clean_tweets()
def clean_tweets(tweet):

    stop_words = set(stopwords.words('portuguese'))
    word_tokens = word_tokenize(tweet)

    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    #filter using NLTK library append it to a string
    #filtered_tweet = [w for w in word_tokens if not w in stop_words]
    filtered_tweet = []

    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)


#method write_tweets()
def write_tweets(keyword, file):

    header_switch=True

    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
        header_switch=False
    else:
        df = pd.DataFrame(columns=COLS)

    #page attribute in tweepy.cursor and iteration
    for page in tweepy.Cursor(api.search, q=keyword, lang='pt', include_rts=False, since=start_date, tweet_mode="extended").pages():

        if os.path.exists(file):
            header_switch=False

        df_to_append = pd.DataFrame(columns=COLS)

        for status in page:
            new_entry = []
            status = status._json

            #if status['id'] in df['id'].values:
            #    continue

            ## check whether the tweet is in english or skip to the next tweet
            if status['lang'] != 'pt':
                continue

            #when run the code, below code replaces the retweet amount and
            #no of favorires that are changed since last download.
            if status['created_at'] in df['created_at'].values:
                i = df.loc[df['created_at'] == status['created_at']].index[0]
                if status['favorite_count'] != df.at[i, 'favorite_count'] or status['retweet_count'] != df.at[i, 'retweet_count']:
                    df.at[i, 'favorite_count'] = status['favorite_count']
                    df.at[i, 'retweet_count'] = status['retweet_count']
                continue


            #tweepy preprocessing called for basic preprocessing
            # clean_text = p.clean(status['full_text'])
            clean_text = status['full_text']

            #call clean_tweet method for extra preprocessing
            filtered_tweet = clean_tweets(clean_text)

            #pass textBlob method for sentiment calculations
            blob = TextBlob(filtered_tweet)
            Sentiment = blob.sentiment

            #seperate polarity and subjectivity in to two variables
            polarity = Sentiment.polarity
            subjectivity = Sentiment.subjectivity

            #new entry append
            new_entry += [status['id'], status['created_at'], status['source'], status['full_text'],filtered_tweet,
                          Sentiment, polarity, subjectivity, status['lang'], status['favorite_count'], status['retweet_count']]

            #to append original author of the tweet
            new_entry.append(status['user']['screen_name'])

            try:
                is_sensitive = status['possibly_sensitive']
            except KeyError:
                is_sensitive = None
            new_entry.append(is_sensitive)

            # hashtagas and mentiones are saved using comma separted
            hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
            new_entry.append(hashtags)
            mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
            new_entry.append(mentions)

            #get location of the tweet if possible
            try:
                location = status['user']['location']
            except TypeError:
                location = ''
            new_entry.append(location)

            try:
                coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
            except TypeError:
                coordinates = None
            new_entry.append(coordinates)

            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df_to_append = df_to_append.append(single_tweet_df, ignore_index=True)

        with open(file, 'a' ,encoding='utf-8') as csvFile:
            df_to_append.to_csv(csvFile, mode='a', columns=COLS, header=header_switch, index=False, encoding="utf-8")


#call main method passing keywords and file path
#write_tweets(corona_keywords,  corona_tweets)

print("Scrapping just started...")
keep_scraping=True
x=1
while keep_scraping:
    try:
        print("------------------------------------------")
        print("Attempt No.{}".format(x))
        x+=1
        write_tweets(quarentena_keywords, quarentena_tweets)
    except tweepy.TweepError:
        print("A TweepyError occurried... trying again.")
        continue
    else:
        print("An error occurried... trying again.")
        try:
            continue
        except KeyboardInterrupt:
            keep_scraping=False
            break

print("------------------------------------------")
print("Script ended.")
