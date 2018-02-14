import websocket
import json
import requests
import urllib
import os


# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        MESSAGE = """Hello,
        Welcome to Eulercoder Community!

        The aim of this community is to build a community of entrepreneurs helping each other in finding the best possible solution to the problems identified and experienced. Eulercoder community is a place for developers, marketers, sales persons, co-founders, wanna be entrepreneurs to come together and dicuss & Validate ideas, work on products, talk about things, hire and work together.

You can post about random ideas that come in your mind to get validated in #general  channel. You can post about things you’re planning to do and get feedback here.

Community Rules (Kindly Read these before posting anything in *#general*):

1. Only posts related to the following things are allowed:
  1.1. New Start-up Ideas
  1.2. Problems identified in existing products, services or technology which needs Solution
  1.3. Problems faced while working on a Startup Idea
  1.4. New startup launches
2. Only discussions related to giving advice, feedbacks, and suggestions on the posts is allowed.
3. LINKS are only and only allowed if they add VALUE to the discussion. The moment the post turns unethical and irrelevant to the community’s theme, it would be rejected and deleted.
4. Keep the posts Polite and spam free.
5. Posts apart from the above-mentioned categories will be removed or moved to a different channel and if rules are not followed then after 3rd time, the person will be blocked.

We have many channels for you to talk about all things related our community theme.
Based on your interests and likes, check out and post in respectives channels if post is directly related to any of these channels.
#good_finds : _anything you find interesting on the web_
#hiring: _anything related to hiring, if you or any of your friend is hiring_
#for-hire: _if you would like to get hired_

Similarly we have, #nodejs, #software_development, #webdevelopement, #whereyouat , #marketing. You can click on “channels” to list all the channels.

If anyone has any suggestions or feedback feel free to reach out me directly,
@eulercoder or you can also write an email to be - tvicky002 [at] gmail [dot] com.

Let’s invite like minded people to join this community and get started!

Thank you!"""
        TOKEN = 'xoxb-315111499269-06ZGLRvxCQeGSTdLimqfJ4XZ'
        UNFURL = 'TRUE'
except:
        MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
        TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'
        UNFURL = 'FALSE'
###############################################################

def parse_join(message):
    m = json.loads(message)
    if (m['type'] == "team_join"):
        x = requests.get("https://slack.com/api/im.open?token="+TOKEN+"&user="+m["user"]["id"])
        x = x.json()
        x = x["channel"]["id"]
        if (UNFURL.lower() == "false"):
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true&unfurl_links=false")
        else:
          xx = requests.post("https://slack.com/api/chat.postMessage?token="+TOKEN+"&channel="+x+"&text="+urllib.quote(MESSAGE)+"&parse=full&as_user=true")
        #DEBUG
        #print '\033[91m' + "HELLO SENT" + m["user"]["id"] + '\033[0m'
        #

#Connects to Slacks and initiates socket handshake
def start_rtm():
    r = requests.get("https://slack.com/api/rtm.start?token="+TOKEN, verify=False)
    r = r.json()
    print r
    r = r["url"]
    return r

def on_message(ws, message):
    parse_join(message)

def on_error(ws, error):
    print "SOME ERROR HAS HAPPENED", error

def on_close(ws):
    print '\033[91m'+"Connection Closed"+'\033[0m'

def on_open(ws):
    print "Connection Started - Auto Greeting new joiners to the network"


if __name__ == "__main__":
    r = start_rtm()
    ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
    #ws.on_open
    ws.run_forever()
