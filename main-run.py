#!/usr/bin/env python3

...
...

import os
import platform
from time import ctime
import discord  
import asyncio
from discord.ext import tasks, commands
from mcstatus import MinecraftServer
from timeloop import Timeloop
import datetime
import mechanize
import urllib.parse
import brotli
import re
import yaml

if platform.system() == 'Windows':
    with open(r'data.yml') as file:
        TOKEN = yaml.load(file, Loader=yaml.FullLoader)['token']
elif platform.system() == 'Linux':
    with open(r'/home/pi/git/PNW-Bot/data.yml') as file:
        TOKEN = yaml.load(file, Loader=yaml.FullLoader)['token']

server = MinecraftServer.lookup("bte-nw.apexmc.co")

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
    channel = client.get_channel(711296187818442816)
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
        with open(r'/home/pi/git/PNW-Bot/data.yml') as file:
            username = yaml.load(file, Loader=yaml.FullLoader)['username']
        with open(r'/home/pi/git/PNW-Bot/data.yml') as file:
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

#######################################################################################
#                               Command Stuff
#######################################################################################

#fulcrum
async def fulcrum(message):
    await message.delete(delay=3)
    message = await message.channel.send('<@630961425967218718>')
    await message.delete(delay=3)
    

#status
async def statuscommand(message):
    global cstatus 
    if cstatus == False:
        embed = discord.Embed(title='Sorry...',description = 'Server is \n```diff\n- Down\n```', color=color)
        await message.channel.send(embed = embed)
    else:
        latency = server.ping()
        ping = str(round(latency, 0))
        embed = discord.Embed(title='Response Time:', description=ping + ' ms', color=color)
        await message.channel.send(embed = embed)

#ip
async def ipcommand(message):
    host = server.host
    embed=discord.Embed(title="Server IP:", description=host, color=color)
    await message.channel.send(embed = embed)

#team
async def teamcommand(message):
    embed=discord.Embed(title="NW Build Team", url='https://buildtheearth.net/buildteams/153', color=color)
    await message.channel.send(embed = embed)
    
#help
async def helpcommand(message):
    embed=discord.Embed(title="Commands:", color=color)
    embed.add_field(name=".ip", value="Server IP", inline=True)
    embed.add_field(name=".status", value="Server's Ping", inline=True)
    embed.add_field(name=".team", value="Build Team Link", inline=True)
    embed.add_field(name=".data", value="Server Stats", inline=True)
    embed.add_field(name=".mods", value="Install Tutorial", inline=True)
    await message.channel.send(embed = embed)

#mods  
async def modscommand(message):
    embed=discord.Embed(title="How To Get On The Server", url='https://sites.google.com/view/bte-nw/infotutorials/installing-mods', color=color)
    await message.channel.send(embed = embed)
    
#website
async def websitecommand(message):
    embed=discord.Embed(title="Our Website", url='https://sites.google.com/view/bte-nw/home', color=color)
    await message.channel.send(embed = embed)
    
#server
async def servercommand(message):
    await message.delete(delay=10)
    embed=discord.Embed(title="ur dumb do .status", color=color)
    message =  await message.channel.send(embed = embed)
    await message.delete(delay=10)
    
#down
async def downcommand(message):
    global cstatus 
    channel = client.get_channel(730305091965288550)
    host = server.host
    if is_staff(message) == True:
        if cstatus == True: 
            embed=discord.Embed(title="Status set to down.",description="Status will stay down until you type .auto.", color=color)
            await message.channel.send(embed = embed)
            pause()
            await asyncio.sleep(2)
            cstatus = False
            await client.change_presence(status=discord.Status.do_not_disturb,activity=None)
        else:
            embed=discord.Embed(title="Server is already down.", color=color)
            await message.channel.send(embed = embed)
    else:
        await message.delete(delay=10)
        embed=discord.Embed(title="You aren't staff stop trying to break things smh", color=color)
        message = await message.channel.send(embed = embed)
        await message.delete(delay=10)
        
#auto
async def autocommand(message):
    if is_staff(message) == True:
        embed=discord.Embed(title="Set to auto-monitor.", color=color)
        await message.channel.send(embed = embed)
        resume()
    else:
        await message.delete(delay=10)
        embed=discord.Embed(title="You aren't staff stop trying to break things smh", color=color)
        message = await message.channel.send(embed = embed)
        await message.delete(delay=10)

#pause
async def pausecommand(message):
    if is_staff(message) == True:
        embed=discord.Embed(title="Status paused, no new messages will occur until you type .auto.", color=color)
        await message.channel.send(embed = embed)
        pause()
    else:
        await message.delete(delay=10)
        embed=discord.Embed(title="You aren't staff stop trying to break things smh", color=color)
        message = await message.channel.send(embed = embed)
        await message.delete(delay=10)

#data
async def datacommand(message):
    global cstatus 
    if cstatus == False:
        embed = discord.Embed(title='Sorry...',description = 'Server is \n```diff\n- Down\n```', color=color)
        await message.channel.send(embed = embed)
    else:
        embed=discord.Embed(title="Getting data...", color=color)
        message = await message.channel.send(embed = embed)
        data = getstats()
        await message.delete()
        embed=discord.Embed(title=data[0]+'% CPU usage, ' + data[1] + "% ram usage.", color=color)
        await message.channel.send(embed = embed)
        


commands = {
".status": statuscommand,
".ip": ipcommand,
".team": teamcommand,
'.help': helpcommand,
'.mods': modscommand,
'.website': websitecommand,
'.server': servercommand,
'.down': downcommand,
'.auto': autocommand,
'.pause': pausecommand,
'.data': datacommand,
'.fulcrum': fulcrum

}

#Run commands if valid
@client.event
async def on_message(message):
    global cstatus
    global commands
    if message.content in commands:
        await commands[message.content](message)
    
   
        
        


@client.event
async def on_member_join(member):
    channel = client.get_channel(707748041599483986)
    embed=discord.Embed(title='Welcome to the server!',description='Check out <#707749870584332458> for info, get your roles in <#707784141550256188>, and say hi in <#712526046188273726>!', color=color)
    embed.add_field(name="Server IP:", value="bte-nw.apexmc.co", inline=False)
    embed.add_field(name="Our Build Team:", value="https://buildtheearth.net/buildteams/153", inline=False)
    await channel.send(embed=embed)
    await channel.send('<@'+str(member.id)+'>')
        
#######################################################################################
#                                  Loops
#######################################################################################

@tasks.loop(seconds=10)
async def playerlist():
    if cstatus == True:
        query = server.query()
        activity = discord.Game(name=str(query.players.online) + '/' + str(query.players.max) + ' players Building The NW')
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
