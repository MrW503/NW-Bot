#!/usr/bin/env python3

...
...

import os
import json
import platform
import discord  
import asyncio
from discord.ext import tasks, commands
from mcstatus import MinecraftServer
from timeloop import Timeloop
import mechanize
import urllib.parse
import brotli
import re
import yaml
#from commandfunctions import commandlist
import commandfunctions

if platform.system() == 'Windows':
    path = 'data.yml'
elif platform.system() == 'Linux':
    path = '/home/pi/git/NW-Bot/data.yml'
with open(path) as file:
    TOKEN = yaml.load(file, Loader=yaml.FullLoader)['token']

tl = Timeloop()

cstatus = True

color = 0x9BBF5D

tries = []

client = discord.Client()

nicklist = {
"RowTheGreat": "Fedora Man",
'bluecrafter111': 'timtim',
'wyatttheriotb': 'DJChadRL',
'Speedster2003': 'ryan'
}



#Startup sequence
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    servercheck.start()
    playerlist.start()
    channel = client.get_channel(750500953018466364)
    await channel.send('I\'m online.')
    
    # channel = client.get_channel(707749870584332458)
    # embed=discord.Embed(title="BTE NW: Important Info", color=color)
    # embed.add_field(name="Server Link:", value="https://discord.gg/98RdXk4", inline=False)
    # embed.add_field(name="Patreon:", value="https://www.patreon.com/btenw", inline=False)
    # embed.add_field(name="Server IP:", value="bte-nw.apexmc.co", inline=False)
    # embed.add_field(name="Website Link:", value="https://sites.google.com/view/bte-nw/home", inline=False)
    # await channel.send(embed=embed)
    
#######################################################################################
#                               Misc Functions
#######################################################################################
    
#Login and get server usage stats
def getstats():
    csrf = ''
    final = []
    user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    if platform.system() == 'Windows':
        with open(r'data.yml') as file:
            username = yaml.load(file, Loader=yaml.FullLoader)['username']
        with open(r'data.yml') as file:
            password = yaml.load(file, Loader=yaml.FullLoader)['password']
    elif platform.system() == 'Linux':
        with open(r'/home/pi/git/NW-Bot/data.yml') as file:
            username = yaml.load(file, Loader=yaml.FullLoader)['username']
        with open(r'/home/pi/git/NW-Bot/data.yml') as file:
            password = yaml.load(file, Loader=yaml.FullLoader)['password']            


    browser = mechanize.Browser()
    browser.set_handle_robots( False )
    browser.addheaders = [('User-agent', user)]
    browser.open("https://panel.apexminecrafthosting.com/site/login")
    browser.select_form(nr = 0)
    control = browser.form.find_control("YII_CSRF_TOKEN")
    csrf = urllib.parse.quote(control.value)
    browser.form['LoginForm[name]'] = username
    browser.form['LoginForm[password]'] = password
    browser.submit()


    data='ajax=refresh&type=all&log_seq=0&YII_CSRF_TOKEN=' + csrf
    req = mechanize.Request('https://panel.apexminecrafthosting.com/server/312215', data=data)
    req.add_header("user-agent", user)
    req.add_header("accept-encoding","gzip, deflate, br")
    browser.cookiejar.add_cookie_header(req)
    raw = mechanize.urlopen(req).read()
    decoded = brotli.decompress(raw).decode("utf-8")
    cpudat = re.search("(\d+)[%] CPU",decoded).group().split('%', 1)
    ramdat = re.search("(\d+)[%] MEM",decoded).group().split('%', 1)

    final.append(cpudat[0])
    final.append(ramdat[0])
    return final
    
#Check if message author is a staff member
def is_staff(message):
    for role in message.author.roles:
        if role.name == 'Admin':
            return True
    return False

#Stop the server check loop
def pause():
    servercheck.stop()
    return

#Start the server check loop
def resume():
    servercheck.start()
    return

#Check for message
def playercountmessage(m):
    if m.id != 737344532991049819:
        return True
    else:
        return False

#Check for server up/down
async def check(response):
    global cstatus
    global tries
    channel = client.get_channel(730305091965288550)
    host = server.host
    if len(tries)<3:
        tries.insert(0,response)
        return
    else:
        tries.pop()
        tries.insert(0,response)
        if tries[0] == True and tries[1] == True and tries[2] == True and cstatus == False:
            cstatus = True
            await client.change_presence(status=discord.Status.online,activity=None)
            return
        elif tries[0] == False and tries [1] == False and tries[2] == False and cstatus == True:
            cstatus = False
            await client.change_presence(status=discord.Status.do_not_disturb,activity=None)
            return
        else:
            return

# commands = {
#  "config": (configcommand, [nw,testing]),
#  "status": (statuscommand, [nw, testing]),
#  "ip": (ipcommand, [nw, testing]),
#  "team": (teamcommand, [nw, testing]),
#  "help": (helpcommand, [nw, testing]),
#  "mods": (modscommand, [nw, testing]),
#  "website": (websitecommand, [nw, testing]),
#  "server": (servercommand, [nw, testing]),     
#  "down": (downcommand, [nw, testing]),
#  "auto": (autocommand, [nw, testing]),
#  "pause": (pausecommand, [nw, testing]),
#  "data": (datacommand, [nw, testing])
# }

#Run commands if valid
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
            role = parinfo['admin-role']
    else:
        with open(path + 'default.json', 'r') as openfile: 
            parinfo = json.load(openfile)
            color = parinfo['color']
            prefix = parinfo['prefix']
            role = None   

    parmsg = msg.strip(prefix)
    if parmsg in cdict:
        if guildid in cdict[parmsg][1]:
            await cdict[parmsg][0](client,message,color,role,guildid,prefix)
        else:
            pass
#########################################################################z##############
#                                  Loops
#######################################################################################

@tasks.loop(seconds=10)
async def playerlist():
    if cstatus == True:
        query = server.query()
        activity = discord.Game(name=str(query.players.online) + '/' + str(query.players.max) + ' players building the NW')    
        await client.change_presence(activity=activity)
    else:
        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('someone probably broke the server...'))


@tasks.loop(seconds=2)
async def servercheck():
    try:
        status = server.status()
    except (ConnectionRefusedError, OSError, IOError, BrokenPipeError):
        await check(False)
    else:
        await check(True)

@tasks.loop(seconds=40)
async def statuschange():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Helping Builders Build The Earth"))
    await asyncio.sleep(20)
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Building The Earth Since 2020"))

client.run(TOKEN)
