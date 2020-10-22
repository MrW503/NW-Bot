import os
import json
import platform
import discord  
import asyncio
from discord.ext import tasks
import yaml
import commandfunctions
import status
from configclass import Config

#######################################################################################

if platform.system() == 'Windows':
    path = 'data.yml'
elif platform.system() == 'Linux':
    path = '/home/pi/git/NW-Bot/data.yml'
with open(path) as file:
    TOKEN = yaml.load(file, Loader=yaml.FullLoader)['token']

client = discord.Client()



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    status.getStatusData.start()
    status.checkstatus.start(client)
    statuschange.start()
    
#######################################################################################
#                               Message Handler
#######################################################################################

@client.event
async def on_message(message):
    cdict = commandfunctions.commandlist()
    msg = message.content
    guildid = message.guild.id
    path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'
    
    if (str(guildid) + '.json') in os.listdir(path):
        with open(path + str(guildid) + '.json', 'r') as openfile: 
            parinfo = json.load(openfile)
            color = parinfo['color']
            prefix = parinfo['prefix']
            ip = parinfo['IP']
            role = parinfo['admin-role']
            vc = parinfo['voicechannel']
    else:
        with open(path + 'default.json', 'r') as openfile: 
            parinfo = json.load(openfile)
            color = parinfo['color']
            prefix = parinfo['prefix']
            ip = None
            role = None
            vc = None   

    parmsg = msg.strip(prefix)
    if msg != '' and msg[0] == prefix and parmsg in cdict:
        if guildid in cdict[parmsg][1]:
            config = Config(client,message,color,role,guildid,prefix,ip,vc)
            await cdict[parmsg][0](config)
        else:
            pass
        
#########################################################################z##############
#                                  Status Loop
#######################################################################################

@tasks.loop(seconds=40)
async def statuschange():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Helping Builders Build The Earth"))
    await asyncio.sleep(20)
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Building The Earth Since 2020"))
    

client.run(TOKEN)
