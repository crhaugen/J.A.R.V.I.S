import discord
import pyowm

#REMOVE/ADD keys as need!!!
##**************
TOKEN = '####'
owm = pyowm.OWM('####') 

#creating a discord client from discord import
client = discord.Client()

#switch for different bot operations
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    #possible commands 
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


<<<<<<< HEAD
  
=======
#this is bot information printing to console
>>>>>>> de8c5e8b8b7266116a1b37297bb109b5690b05d3
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#function to perform the tasks
def hello(message):
    msg = 'Hello {0.author.mention}'.format(message)
    print(message.author.id)

    if message.author.id == 'PUT IN YOUR ID':
        print(message.author.id)
        msg = 'Hello Master {0.author.mention}'.format(message)

    return msg

#weather function
def weather():
    observation = owm.weather_at_coords(48.082778, -121.969722)//change coor for different places
    w = observation.get_weather()
    return w 

<<<<<<< HEAD
def clap(message):
    msg = message.content

    wordList = msg.split(" ") 

    msg = msg.split(' ', 2)[2]

    newMsg = msg.replace(" ", ' ' + wordList[1] + ' ')

    return newMsg



=======
#starts the bot
>>>>>>> de8c5e8b8b7266116a1b37297bb109b5690b05d3
client.run(TOKEN)
