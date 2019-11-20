import google.oauth2.credentials
import youtube_sentiment as yt
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle
import pandas as pd
import time
import csv
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'




def get_authenticated_service():
   credentials = None
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           credentials = pickle.load(token)
   #  Check if the credentials are invalid or do not exist
   if not credentials or not credentials.valid:
       # Check if the credentials have expired
       if credentials and credentials.expired and credentials.refresh_token:
           flow = InstalledAppFlow.from_client_secrets_file(
           CLIENT_SECRETS_FILE, SCOPES)
       credentials = flow.run_console()

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(credentials, token)

   return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
'''
def get_videos_FromChanel(youtube, channelId,order):
    search_response = youtube.search().list(
        channelId=channelId,
        type="video",
        part="id,snippet",
        maxResults=1,
        order=order
    ).execute()

    return search_response.get("items", [])
'''
def get_comment_threads(youtube,videoId):
    tempComments = []
    #for video in videos:
        #time.sleep(1.0)
        #print(video["snippet"]["title"])
    print("videoId",videoId)
    results = youtube.commentThreads().list(
    part="snippet",
    videoId=videoId,
    textFormat="plainText",
    maxResults=50,
    order='relevance'
).execute()
    

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        tempComment = dict(nbrReplies = item["snippet"]["totalReplyCount"],author = comment["snippet"]["authorDisplayName"],likes = comment["snippet"]["likeCount"],publishedAt=comment["snippet"]["publishedAt"],text = comment["snippet"]["textDisplay"].strip())
        tempComments.append(tempComment)

    return tempComments
    
youtube =get_authenticated_service()

'''
request = youtube.search().list(
    part="snippet",
    q=YOUTUBE_CHANNEL_NAME,
    type="channel",
    fields="items/snippet/channelId"
)

response = request.execute()
print("Response:",response)
print(response["items"][0])
'''
#videos = get_videos_FromChanel(youtube, CHANNEL_ID,"viewCount")


#url = input("Enter URL)
#videoId = url.split("=")[1]
videoIds = ["HzeekxtyFOY","t433PEQGErc"]
ctr =1
for videoId in videoIds:
    comments = get_comment_threads(youtube, videoId)
    l = []

    for i in comments:
        print(i["text"])
        l.append([i["text"]])

    with open('Comments_scraped'+str(ctr)+'.csv', 'w') as comments_file:
        print("*********")
        comments_writer = csv.writer(comments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        comments_writer.writerow(['Comment'])
        for row in l:
            # convert the tuple to a list and write to the output file
            
            comments_writer.writerow(row)
    ctr+=1

