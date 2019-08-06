import discord
import pyowm

#REMOVE/ADD keys as need!!!
##**************
TOKEN = '####'
owm = pyowm.OWM('####') 
reddit = praw.Reddit('####')

#creating a discord client from discord import
client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = hello(message)
        await client.send_message(message.channel, msg)
    
    elif message.content.startswith('!temp'):
        msg = weather() 
        await client.send_message(message.channel, 'Current Temperature: {} F'.format(msg.get_temperature('fahrenheit')['temp']))

    elif message.content.startswith('!weather'):
        msg = weather()
        await client.send_message(message.channel, 'Weather Status: {}'.format(msg.get_detailed_status()))
    
    elif  message.content.startswith('!clap'):
        msg = clap(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!upsidedown'):
        msg = upsidedownWords(message)
        await client.send_message(message.channel, msg)
   
    elif message.content.startswith('!reddit'):
        msg = redditPosts(message)
        await client.send_message(message.channel, msg)


  
@client.event    
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def hello(message):
    msg = 'Hello {0.author.mention}'.format(message)
    print(message.author.id)

    if message.author.id == '445619407520268298':
        print(message.author.id)
        msg = 'Hello Master {0.author.mention}'.format(message)

    return msg

def weather():
    observation = owm.weather_at_coords(48.082778, -121.969722)
    w = observation.get_weather()
    return w 
#prints string with emoijs inbetween
def clap(message):
    msg = message.content

    wordList = msg.split(" ") 

    msg = msg.split(' ', 2)[2]

    newMsg = msg.replace(" ", ' ' + wordList[1] + ' ')

    return newMsg

#prints string upside down
def upsidedownWords(message):
    msg = message.content
    
    wordList = msg.split(" ")

    msg = msg.split(' ', 1)[1]

    newMsg = upsidedown.transform(msg)

    return newMsg
#scraps posts off reddit
def redditPosts(message):
    msg = message.content

    wordList = msg.split(" ")

    subType = wordList[1]

    subs = reddit.subreddit(subType).hot(limit=5)

    subs = [sub for sub in subs if not sub.domain.startswith('self.')]

    mes = 'Fetching posts from front page of ' + subType + ':\n\n'

    for sub in subs:
        res = requests.get(sub.url)
        if(res.status_code == 200 and 'content-type' in res.headers and res.headers.get('content-type').startswith('text/html')):

            mes +='Title: ' + sub.title + '\n'
            mes += 'Link: ' + sub.url + '\n\n'

    return mes



client.run(TOKEN)

client.run(TOKEN)
