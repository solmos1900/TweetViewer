import sys
sys.path.insert(0,'./modulesForOauth')
import requests
from requests_oauthlib import OAuth1
import json
from urllib.parse import quote_plus


#API_KEY = 
#API_SECRET = 
#ACCESS_TOKEN = 
#ACCESS_TOKEN_SECRET = 
 
def authTwitter():
    global client
    client = OAuth1(API_KEY, API_SECRET,
                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Iowa City's lat/lng is [41.6611277, -91.5301683] 
#      
#
#
#
def searchTwitter(searchString, count = 20, radius = 2, latlngcenter = None):    
    query = "https://api.twitter.com/1.1/search/tweets.json?q=" + quote_plus(searchString) + "&count=" + str(count)


    query = query + "&tweet_mode=extended" 
    
    if latlngcenter != None:
        query = query + "&geocode=" + str(latlngcenter[0]) + "," + str(latlngcenter[1]) + "," + str(radius) + "km"
    global response
    #global client
    
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
    # The most important information in resultDict is the value associated with key 'statuses'
    tweets = resultDict['statuses']
    tweetsWithGeoCount = 0 
    for tweetIndex in range(len(tweets)):
        tweet = tweets[tweetIndex]
        if tweet['coordinates'] != None:
            tweetsWithGeoCount += 1
            
            print("Tweet {} has geo coordinates.".format(tweetIndex))
            

            
    return tweets
    


def printable(s):
    result = ''
    for c in s:
        result = result + (c if c <= '\uffff' else '?')
    return result



def whoIsFollowedBy(screenName):
    global response
    global resultDict
    
    query = "https://api.twitter.com/1.1/friends/list.json?&count=50"
    query = query + "&screen_name={}".format(screenName)
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
    count = 0
    for person in resultDict['users']:
        print(person['screen_name'])
        count+=1
    print(count)
    
def getMyRecentTweets():
    global response
    global data
    global statusList 
    query = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    response = requests.get(query,auth=client)
    statusList = json.loads(response.text)
    for tweet in statusList:
        print(printable(tweet['text']))
        print()

 
