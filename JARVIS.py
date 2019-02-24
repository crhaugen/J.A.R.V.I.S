import discord
import pyowm

#REMOVE/ADD keys as need!!!
TOKEN = '####'
owm = pyowm.OWM('####') 

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


client.run(TOKEN)
