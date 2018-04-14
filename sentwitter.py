subscription_key = '0d4a0166bde9467dacfd41da8bbb6904'
assert subscription_key
text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
sentiment_api_url = text_analytics_base_url + "sentiment"
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json 
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '873423774-dRGyXg4TqxE4xLPCD3ad1PxcHPXqhzLVNAkA5U3N'
ACCESS_SECRET = 'vVknv5YnAAwtleYmS0WvjJIEZ1Ej8yXxEBqevPe2JQyG9'
CONSUMER_KEY = 'YCDgQaaYIyjJoOB9kaM9tK8dz'
CONSUMER_SECRET = '0vQSTCoqJDA6waVOy8hSuvoAq7zFD9lm1eHs6Oot8wKuyRGBgL'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


twitter = Twitter(auth=oauth)

#q input -----------------------------------------------------------------------------
search = "google"
results = twitter.search.tweets(q=search,result_type='recent', lang='en', count=100)
print("twitter api for %s done !!",search)

txt = results['statuses']
documents = {}
docs = []
print(len(txt))
for i in range(len(txt)):
    docs.append({'id':i+1,'language':'en','text':txt[i]['text']})
documents.update({'documents':docs})

import requests
headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=documents)
sentiments = response.json()
print("microsoft cognitive service sentiment scoring done !!")
#sentiment score------------------------------------------------------------------------
l = sentiments['documents']
pos = 0 
neg = 0
for i in l:
    if i['score']>0.5:
        pos+=1
    elif i['score']<0.5:
        neg+=1
if pos+neg == 0:
    print("neutral")
else:
    print(pos*100/(pos+neg))

key_phrase_api_url = text_analytics_base_url + "keyPhrases"
response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()
print("microsoft cognitive service key phrases done !!")

st = ""
r = [w.lower() for l in key_phrases['documents'] for w in l['keyPhrases']]
for i in r:
	if i != "rt" and i !="amp":
		st = st+" "+i
print(st)
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(max_font_size=40).generate(st)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('wordcloud.png')