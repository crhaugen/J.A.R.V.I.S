import discord
import pyowm
import upsidedown
import praw
import requests
import os

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
bot.run(token)
