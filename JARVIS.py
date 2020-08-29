import discord
import pyowm
import upsidedown
import praw

import asyncio
import requests
import os
import json
import random
import time
import datetime
import math


from discord.ext import commands
from dotenv import load_dotenv
from spookyASCII import spooky_ascii_art


#this is access able on the .env (on computer running jarvis program)
load_dotenv()

token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

owm = pyowm.OWM(os.getenv('PYOWM_TOKEN'))

reminderInfo = [] #store reminder message and when reminder needs to be sent out




#info from reddit bot (api) I'm using (reddit developer account)
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                      client_secret=os.getenv('CLIENT_SECRET'),
                      grant_type='client_credentials',
                      user_agent='mytestscript/1.0')


# bot info runs on start
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):

    #jarvis says a random quotes if you speak it's names (lowercase only)
    if 'jarvis' in message.content.lower():

        with open('quotes.json', 'r') as quotes:
            jarvisQuotes = json.load(quotes)

        await message.channel.send(random.choice(jarvisQuotes))

    await bot.process_commands(message)

#jarvis background task always running will run with the remindMe Function
async def my_background_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(602605656704417999)
    waitTime = 300 #check for updated every 5 minutes
    n = ["", "", "", "", "", "", "", ""] #fill with whatever words you want to address user with

    while not bot.is_closed():
        for info in reminderInfo:
            timeTillPrint = info[0] - datetime.datetime.now()
            seconds = timeTillPrint.seconds
            hours = int(math.floor(seconds / 3600))
            minutes = int(math.floor((seconds - (hours * 3600)) / 60))

            # if at time (+/- 5 min) then print reminder
            if timeTillPrint.days == 0:
                if hours == 0:
                    if minutes <= 5:
                        ran = random.randint(0, len(n) - 1)
                        msg = "HEY " + n[ran] + " " + info[2] + " here is your reminder: " + info[1] + " your welcome. " 
                        await channel.send(msg)

        #check if reminder needs to be send every 5 minutes
        await asyncio.sleep(waitTime)


# simple example that prints out hello
@bot.command(name='hello', help='Jarvis says hello.')
async def hello(context):

    # my user
    if context.author.id == 445619407520268298:
        msg = 'Hello Master ' + context.author.mention

    else:
        msg = 'Hello ' + context.author.mention

    await context.send(msg)

# helper fuction for remindMe
# https://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python
def addSecs(date, secs):

    day = date.day
    month = date.month
    year = date.year
    tm = date.time()

    fulldate = datetime.datetime(year, month, day, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate

# reminds the user of something and given time.
@bot.command(name='remindMe', help='')
async def remindeMe(context):

    msg = context.message.content

    #todo catch errors 

    #remove the prompt word
    msg = msg.split(' ', 1)[1]

    # seperate the time from the messsage
    msgInfo = msg.split('>')

    # user's message
    userReminder = msgInfo[0]

    time = msgInfo[1]

    # min or hr
    unitOfTime = time.split(' ')[1]

    # amount of time (int)
    timeTillReminder = time.split(' ')[0]

    secTillReminder = 0

    if unitOfTime == 'hr':
        print("hr")
        secTillReminder = int(timeTillReminder) * 3600
    else:
        secTillReminder = int(timeTillReminder) * 60


    timeToPrintReminder = addSecs(datetime.datetime.now(), secTillReminder)

    reminderInfo.append([timeToPrintReminder, userReminder, context.author.mention])

    msg = "OK I will try to remind you to: " + userReminder + " in about " + time + " give or take some time."

    await context.send(msg)

goldStarTable = {}

@bot.command(name='goldstar', help='Gives user a gold star')
async def goldstar(context):
    #how to give another user the star? (give username and map that to id?)
    #Gobal list of user and their star count, when called jarvis rewards 

    msg = context.message.content
    #message: !goldstar >>@username
    #remove the prompt word

    msg = msg.split(' ', 1)[1]

    # seperate the time from the messsage
    msgInfo = msg.split('>>')

    username = magInfo[0]

    if username in userStars:
        goldStarTable[username] += 1

    else:
        goldStarTable[username] = 1





#helper function to get weather info at coords (add input options)
def getWeatherData():
    observation = owm.weather_at_coords(48.082778, -121.969722)
    return observation.get_weather()

#Get weather @ set locations
@bot.command(name='weather', help='Gives current weather')
async def weather(context):
    msg = 'Weather Status: {}'.format(getWeatherData().get_detailed_status())
    await context.send(msg)

# print current temp @ set locations 
@bot.command(name='temp', help='Gives current temp')
async def temp(context):
    msg = 'Current Temperature: {} F'.format(getWeatherData().get_temperature('fahrenheit')['temp'])
    await context.send(msg)

# repeats users message with emoji between values
@bot.command(name="clap", help="Inserts some value into give string.")
async def clap(context):
    msg = context.message.content
    wordList = msg.split(" ")
    msg = msg.split(' ', 2)[2]
    newMsg = msg.replace(" ", ' ' + wordList[1] + ' ')

    await context.send(newMsg)

# turns given texts upsidedown (using api)
@bot.command(name="upsidedown", help="turns text upsidedown")
async def upsidedownWords(context):
    msg = context.message.content
    msg = msg.split(' ', 1)[1]
    newMsg = upsidedown.transform(msg)

    await context.send(newMsg)

#grabs top pages on reddit from any given subreddit
@bot.command(name="reddit", help="gets top posts from given subreddit: !reddit <subReddit>")
async def redditPosts(context):
    msg = context.message.content
    wordList = msg.split(" ")
    subType = wordList[1]

    subs = reddit.subreddit(subType).hot(limit=5)
    subs = [sub for sub in subs if not sub.domain.startswith('self.')]

    mes = 'Fetching posts from front page of ' + subType + ':\n\n'

    #graps link (not .self)
    for sub in subs:
        res = requests.get(sub.url)
        print(res.status_code)
        if(res.status_code == 200 and 'content-type' in res.headers and res.headers.get('content-type').startswith('text/html')):
            mes += 'Title: ' + sub.title + '\n'
            mes += 'Link: ' + sub.url + '\n\n'
            print('getting links' + sub.title)

    await context.send(mes)

#todo move hoilday stuff to new file
#funtion to run spooky jokes put in another file
#@bot.command(name="spookyjoke", help="jarvis will tell you a spooky joke")
#async def spookyJoke(context):

 #   with open('spookyJokes.json', 'r') as joke:
 #       listOfJokes = json.load(joke)

   # await context.send(random.choice(listOfJokes))

bot.loop.create_task(my_background_task())

#print days, hours, min till xmas
#todo: make it so year rolls over to the new xmas automaticly
@bot.command(name="daystillxmas", help="days till xmas 2020")
async def daystillxmas(context):
    christmas = datetime.datetime.strptime("12/25/2020", "%m/%d/%Y")
    now = datetime.datetime.now()
    diff = christmas - now
    days = diff.days
    seconds = int(diff.seconds)
    hours = int(math.floor(seconds / 3600))
    minutes = int(math.floor((seconds - (hours * 3600)) / 60))

    strHours = str(hours)
    strMinutes = str(minutes)

    if minutes < 10:
        strMinutes = "0" + strMinutes
    if hours < 10:
        strHours = " " + strHours

    output = "There are " + str(days) + " Days, " + strHours + " Hours, and " + strMinutes + " Minutes till xmas."
    await context.send(output)

#runs bot
bot.run(token)
