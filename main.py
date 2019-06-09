import feedparser
import tweepy
from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime

#create a new twitter handle and follow Instructions to create a new App.
def handler(event,context):
    #replace with your own keys
        consumer_key=""
        consumer_secret=""

        access_token = ""
        access_secret = ""

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth) # create an API object

        #nycRSSurl = "https://data.cityofnewyork.us/catalog.rss"
        # I created a filtered RSS feed to remove all the "filtered view created entries"
        nycRSSurl = "https://siftrss.com/f/eYbPkjxVJr"
        NYCfeed = feedparser.parse(nycRSSurl)

        for index,entries in enumerate(NYCfeed.entries):
                cleaned_title = entries['title'].encode('utf-8')
                cleaned_link = entries['links'][0]['href'].encode('utf-8')
                tweet = cleaned_title + "\n" + cleaned_link
                cleaned_desc = entries['summary_detail']['value'].encode('utf-8')
          #Excluding feed items with "Filtered View Updated" in them
#                 if "Filtered View Updated" in cleaned_title:
#                         continue
          # This makes sure that you are not reposting the same "Dataset created stuff
          # Update: Use the SIFTRSS link above and you wont need this (i think)
#                 if "Dataset Created" in cleaned_title:
#                         if cleaned_title in open('/tmp/tweets.txt').read():
#                                         continue
#                         else:
#                                         with open("/tmp/tweets.txt", "a") as myfile:
#                                          myfile.write(cleaned_title)
#                                          myfile.write("\n")
#                 else:
#                         print "nothing"
        # For "Dataset Updated" feed entries. So here I  wanted to add a bunch of detail from the dataset to each tweet, 
        # I converted text to image and upload the "image of the text" with every tweet.
                entries = {k: unicode(v).encode("utf-8") for k,v in entries.iteritems()}
                dict_string = '\n'.join('{}: {}'.format(key, val) for key, val in entries.items())
                wrapper = textwrap.TextWrapper(width=500)
                word_list = wrapper.wrap(text=dict_string)
                wrap_desc = '\n\n'.join(word_list)
                img = Image.new('RGB', (2048, 1024), color = (255, 255, 255))
                #specific to OSX
                #fnt = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 15)
                #specific to Linux
                fnt = ImageFont.truetype("fonts/arial.ttf", 28, encoding="unic")
                d = ImageDraw.Draw(img)
                d.text((30,30), dict_string, font=fnt, fill=(0, 0, 0))

                #outfile = 'tweet_%s.jpg' % str(datetime.now())
                img.save('/tmp/tweet.jpg')
                #img.save(outfile)

                # Prints the tweet and saves the image file but does not update twitter. Uncomment the api line to do that.
                print tweet
                api.update_with_media('/tmp/tweet.jpg',str(tweet))
