import discord
import pyowm

#REMOVE/ADD keys as need!!!
TOKEN = 'insert discord key'
owm = pyowm.OWM('insert owm key') 

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
        msg = temperature() 
        await client.send_message(message.channel, 'Current Temperature: {} F'.format(msg.get_temperature('fahrenheit')['temp']))


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

def temperature():
    observation = owm.weather_at_coords(48.082778, -121.969722)
    w = observation.get_weather()
    return w 


client.run(TOKEN)
