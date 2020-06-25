import tkinter
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json
from twitteraccess import *


#GOOGLEAPIKEY = 


class Globals:
   
   rootWindow = None
   mapLabel = None
   searchEntry = None
   increaseButton = None
   decreaseButton = None
   stateVars = None
   counter = 0
   countLabel = None
   selectedButtonText = None
   mapType = None
   tweets = None
   currentTweetIndex = 0
   tweetText = None
   
   
   #label = None
   #choiceVar = None

   defaultLocation = "Mauna Kea, Hawaii"
   mapLocation = defaultLocation
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9

def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + GOOGLEAPIKEY

   # required (non-secure) security stuff for use of urlopen
   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      result = (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   else:
      loc = jsonResult['results'][0]['geometry']['location']
      result = (float(loc['lat']),float(loc['lng']))
   return result


def getMapUrl():
   lat, lng = geocodeAddress(Globals.mapLocation)
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&format=gif&maptype={}&markers=color:red%7Clabel:A%7C{},{}".format(lat,lng,Globals.zoomLevel,Globals.mapSize,Globals.mapSize, Globals.mapType, lat, lng)
   args = args + "&key=" + GOOGLEAPIKEY
   mapURL = urlbase + args
   return mapURL

# Retrieve a map image via Google Static Maps API, storing the 
# returned image in file name specified by Globals' mapFileName
#
def retrieveMapFromGoogle():
   url = getMapUrl()
   urlretrieve(url, Globals.mapFileName)

########## 
#  basic GUI code

def displayMapAndTweets():
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
   Globals.mapLabel.mapImage = mapImage
   Globals.searchEntry
   
   
def generateMarkerString(currentTweetIndex, tweetLatLonList, mapCenterLatLon):
    centerList = []
    newi = ''
    centerList = mapCenterLatLon
    currTweet = currentTweetIndex
    
    for i in tweetLatLonList:
        print(i)
        if i != tweetLatLonList[currTweet]:
            if i == None:
                newi += (str(mapCenterLatLon).strip("[]").replace(" ","") + "|")
            else:
                newi += (str(i).strip("[]").replace(" ","") + "|")
    return "&markers=color:red|{},{}&markers=color:blue|size:small|{}".format(centerList[0], centerList[1],newi[:-1])

   
def readEntryDisplayMapAndTwitter():
   authTwitter()
   
   Globals.tweets = searchTwitter(Globals.twitterEntry.get(), Globals.searchEntry.get())
   
   text = Globals.tweets[(Globals.currentTweetIndex)]['full_text']
   name = Globals.tweets[(Globals.currentTweetIndex)]['user']['name']
   screen_name = Globals.tweets[(Globals.currentTweetIndex)]['user']['screen_name']

   
   
   print(text,"|",name,"|",screen_name)
   
   
   Globals.tweetText.configure(text= str(text))
   

   Globals.mapLocation = Globals.searchEntry.get()
   
   displayMapAndTweets()
   
def initializeGUIetc():

   Globals.rootWindow = tkinter.Tk()
   Globals.rootWindow.title("HW9")

   mainFrame = tkinter.Frame(Globals.rootWindow) 
   mainFrame.pack()

   topFrame = tkinter.Frame(mainFrame)
   topFrame.pack()
   
   searchLabel = tkinter.Label(topFrame, text = "Enter the location: ")
   searchLabel.pack(side = tkinter.TOP)
   
   Globals.searchEntry = tkinter.Entry(topFrame)
   Globals.searchEntry.pack(side = tkinter.TOP)
   
   Globals.twitterEntry = tkinter.Entry(topFrame)
   Globals.twitterEntry.pack(side = tkinter.BOTTOM)
   twitterLabel = tkinter.Label(topFrame, text = "Enter the twitter keyword: ")
   twitterLabel.pack(side = tkinter.BOTTOM)

   readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map and twitter results!", command=readEntryDisplayMapAndTwitter)
   readEntryAndDisplayMapButton.pack()

   Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
   Globals.mapLabel.pack()
   
   bottomFrame = tkinter.Frame(mainFrame)
   bottomFrame.pack()
   
   decreaseButton = tkinter.Button(bottomFrame, text="-", command=decreaseBy1)
   decreaseButton.pack(side=tkinter.LEFT)
   increaseButton = tkinter.Button(bottomFrame, text="+", command=increaseBy1)
   increaseButton.pack(side=tkinter.LEFT)
   Globals.countLabel = tkinter.Label(bottomFrame, text="Zoom: 0")
   Globals.countLabel.pack(side = tkinter.BOTTOM)
       
   choice1 = tkinter.Radiobutton(mainFrame, text="Road", variable=choiceVar, value=1, command=radioButtonOne)
   choice1.pack()
    
   choice2 = tkinter.Radiobutton(mainFrame, text="Satellite", variable=choiceVar, value=2, command=radioButtonTwo)
   choice2.pack()
    
   choice3 = tkinter.Radiobutton(mainFrame, text="Terrain", variable=choiceVar, value=3, command=radioButtonThree)
   choice3.pack()
    
   choice4 = tkinter.Radiobutton(mainFrame, text="Hybrid", variable=choiceVar, value=4, command=radioButtonFour)
   choice4.pack()
   
   twitterFrame = tkinter.Frame(mainFrame)
   twitterFrame.pack(side = tkinter.BOTTOM)
   
   Globals.tweetText = tkinter.Label(twitterFrame,text ='No tweets yet')
   Globals.tweetText.pack()
   prevButton = tkinter.Button(twitterFrame, text="Prev", command=PrevBy1)
   prevButton.pack(side=tkinter.LEFT)
   nextButton = tkinter.Button(twitterFrame, text="Next", command=NextBy1)
   nextButton.pack(side=tkinter.RIGHT)
   
   

   



    
def NextBy1():
    Globals.currentTweetIndex
    Globals.currentTweetIndex = Globals.currentTweetIndex + 1
    readEntryDisplayMapAndTwitter()
    

def PrevBy1():
    Globals.currentTweetIndex
    if Globals.currentTweetIndex > 0:
        Globals.currentTweetIndex = Globals.currentTweetIndex - 1
        readEntryDisplayMapAndTwitter()

def increaseBy1():
    Globals.zoomLevel += 1
    displayMapAndTweets()
    Globals.counter
    Globals.counter = Globals.counter + 1
    updateCountLabel()
    
def decreaseBy1():
    Globals.counter
    if Globals.counter > 0:
        Globals.counter = Globals.counter - 1
        Globals.zoomLevel -= 1
        displayMapAndTweets()
    updateCountLabel()

def updateCountLabel():
    Globals.countLabel.configure(text="Zoom: {}".format(Globals.counter))

    

def radioButtonOne():
    Globals.mapType = "road"
    displayMapAndTweets()
def radioButtonTwo():
    Globals.mapType = "satellite"
    displayMapAndTweets()
def radioButtonThree():
    Globals.mapType = "terrain"
    displayMapAndTweets()
def radioButtonFour():
    Globals.mapType = "hybrid"
    displayMapAndTweets()
    
    

choiceVar = None
def radioButtonChosen():
    choiceVar = tkinter.IntVar()
    choiceVar.set(1)
    
    if choiceVar.get() == 1:
        Globals.mapType = "roadmap"
        displayMapAndTweets()
    elif choiceVar.get() == 2:
       Globals.mapType = "satellite"
       displayMapAndTweets()
    elif choiceVar.get() == 3:
       Globals.mapType = "terrain" 
       displayMapAndTweets()
    else:
        Globals.mapType = "hybrid"
        displayMapAndTweets()


def HW9():    
    initializeGUIetc()
    displayMapAndTweets()
    authTwitter()
    Globals.rootWindow.mainloop()
    
    
