import discord
import pyowm
import upsidedown
import praw

import asyncio
import requests
import os
import json
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

owm = pyowm.OWM(os.getenv('PYOWM_TOKEN'))

reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                      client_secret=os.getenv('CLIENT_SECRET'),
                      grant_type='client_credentials',
                      user_agent='mytestscript/1.0')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):

    if 'jarvis' in message.content.lower():

        with open('quotes.json', 'r') as quotes:
            jarvisQuotes = json.load(quotes)

        await message.channel.send(random.choice(jarvisQuotes))

    await bot.process_commands(message)

async def my_background_task():
    await bot.wait_until_ready()
    count = 0
    channel = bot.get_channel(602607175340130304)

    print('this is in here')
    while not bot.is_closed():
        print(r"""
	      .-----.
	    .' -   - '.
	   /  .-. .-.  \    Y O U  H A V E
	   |  | | | |  |    B E E N  S P O O K E D
	    \ \o/ \o/ /
	   _/    ^    \_
	  | \  '---'  / |
	  / /'--. .--'\ \
	 / /'---' '---'\ \
	 '.__.       .__.'
	     '|     |'
	      |     \
	      \      '--.
	       '.        '\
	         '---.   |
	            ,__) /
        """)

        await channel.send('```' + r"""
		 .             *        .     .       .
		       .     _     .     .            .       .
		.    .   _  / |      .        .  *         _  .     .
		        | \_| |                           | | __
		      _ |     |                   _       | |/  |
		     | \      |      ____        | |     /  |    \
		     |  |     \    +/_\/_\+      | |    /   |     \
		   _/____\--...\___ \_||_/ ___...|__\-..|____\____/__
		      .     .      |_|__|_|         .       .
		   .    . .       _/ /__\ \_ .          .
		      .       .    .           .         .
       """ + '```')
        await asyncio.sleep(60)

@bot.command(name='hello', help='Jarvis says hello.')
async def hello(context):

    if context.author.id == 445619407520268298:
        msg = 'Hello Master ' + context.author.mention

    else:
        msg = 'Hello ' + context.author.mention

    await context.send(msg)

#helper function to get weather info at coords
def getWeatherData():
    observation = owm.weather_at_coords(48.082778, -121.969722)
    return observation.get_weather()

@bot.command(name='weather', help='Gives current weather')
async def weather(context):
    msg = 'Weather Status: {}'.format(getWeatherData().get_detailed_status())
    await context.send(msg)

@bot.command(name='temp', help='Gives current temp')
async def temp(context):
    msg = 'Current Temperature: {} F'.format(getWeatherData().get_temperature('fahrenheit')['temp'])
    await context.send(msg)

@bot.command(name="clap", help="Inserts some value into give string.")
async def clap(context):
    msg = context.message.content
    wordList = msg.split(" ")
    msg = msg.split(' ', 2)[2]
    newMsg = msg.replace(" ", ' ' + wordList[1] + ' ')

    await context.send(newMsg)

@bot.command(name="upsidedown", help="turns text upsidedown")
async def upsidedownWords(context):
    msg = context.message.content
    msg = msg.split(' ', 1)[1]
    newMsg = upsidedown.transform(msg)

    await context.send(newMsg)

@bot.command(name="reddit", help="gets top posts from given subreddit")
async def redditPosts(context):
    msg = context.message.content
    wordList = msg.split(" ")
    subType = wordList[1]

    subs = reddit.subreddit(subType).hot(limit=5)
    subs = [sub for sub in subs if not sub.domain.startswith('self.')]

    mes = 'Fetching posts from front page of ' + subType + ':\n\n'

    for sub in subs:
        res = requests.get(sub.url)
        print(res.status_code)
        if(res.status_code == 200 and 'content-type' in res.headers and res.headers.get('content-type').startswith('text/html')):
            mes += 'Title: ' + sub.title + '\n'
            mes += 'Link: ' + sub.url + '\n\n'
            print('getting links' + sub.title)

    print(mes)
    await context.send(mes)

bot.loop.create_task(my_background_task())
bot.run(token)
