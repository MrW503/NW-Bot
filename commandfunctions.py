import os
import json
import discord  
import asyncio
from mcstatus import MinecraftServer
import enum



#client = main.discord.Client()
#######################################################################################
#                               Command Stuff
#######################################################################################
 
 ##############
# Server IDS
##############     

nw = 707747343788802078
se = 723757662390583427
testing = 750500953018466361

#############


def getserver(message,guildid):
    if guildid == nw:
        return MinecraftServer.lookup("bte-nw.apexmc.co")
    if guildid == se or guildid == testing:
        return MinecraftServer.lookup("104.243.43.228:25571")

async def ipcommand(client,message,color,role,guildid,prefix):
    server = getserver(message,guildid)
    host = server.host
    embed=discord.Embed(title="Server IP:", description=host, color=color)
    await message.channel.send(embed = embed)
    
async def teamcommand(client,message,color,role,guildid,prefix):
    if guildid == nw:
        embed=discord.Embed(title="NW Build Team", url='https://buildtheearth.net/bte-nw', color=color)
    elif guildid == se:
        embed=discord.Embed(title="SE Build Team", url='https://buildtheearth.net/buildteams/138', color=color)
    await message.channel.send(embed=embed) 

async def helpcommand(client,message,color,role,guildid,prefix):
    embed=discord.Embed(title="Commands:", color=color)
    embed.add_field(name=prefix+"ip", value="Server IP", inline=True)
    embed.add_field(name=prefix+"team", value="Build Team Link", inline=True)
    await message.channel.send(embed = embed)
    pass
     
 
 
 
 
 
 
 
 #start: color or {timer}exit
 #color: prefix or color or exit
#prefix: admin or prefix or exit
#admin: verify or ?? or exit 
#verify: save or exit
#save: exit
 
class ConfigState(enum.Enum):
    Start = 1
    Color = 2
    Prefix = 3
    Admin = 4
    Verify = 5
    Save = 6
    Exit = 7
 
async def exit(desc,color,botmsg):
    await botmsg.delete()
    await oldmsg.delete()
    embed=discord.Embed(title='Configuration',description=desc, color=color)
    message = await botmsg.channel.send(embed = embed)
    await message.delete(delay=10)
 
def checkemote(event, user):
    if user == oldmsg.author and str(event.emoji) == '✅':
        return True
    elif user == oldmsg.author and str(event.emoji) == '❌':
        return True
    else:
        return False
    
def isauthor(message):
    return message.author == oldmsg.author

    
async def editmsg(botmsg,desc,color):
    embed=discord.Embed(title='Configuration',description=desc, color=color)
    await botmsg.edit(embed=embed)
 
async def configcommand(client,message,color,role,guildid,prefix):
    global oldmsg
    global reaction
    path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'
    oldmsg = message
    reaction = 0
    tempdict = {}
    botmsg = None
    state = ConfigState.Start
    
    
    while state != ConfigState.Exit:
        # Start -- do you want to configure?  Either go to color or exit
        if state == ConfigState.Start:
            embed=discord.Embed(title='Configuration',description='This server hasn\'t been set up. React below to configure.', color=color)
            botmsg = await message.channel.send(embed = embed)
            await botmsg.add_reaction(emoji='✅')
            await botmsg.add_reaction(emoji='❌')
            try:
                event, user = await client.wait_for('reaction_add', timeout=30.0, check=checkemote)
            except asyncio.TimeoutError:
                state = ConfigState.Exit
                desc = 'Timed out... type .configure to reopen me.'
                await exit(desc,color,botmsg)
            else:
                if str(event.emoji) == '✅':
                    await botmsg.clear_reactions()
                    state = ConfigState.Color
                else:
                    state = ConfigState.Exit
                    desc = 'Closed.'
                    await exit(desc,color,botmsg)
                    
        if state == ConfigState.Color:
            desc = 'What color should the embeds be? *Needs hex code*'
            await editmsg(botmsg,desc,color)
            await botmsg.add_reaction(emoji='❌')
            done, pending = await asyncio.wait([client.wait_for('message', check=isauthor),client.wait_for('reaction_add', check=checkemote)]
                , return_when=asyncio.FIRST_COMPLETED)
            try:
                event = done.pop().result()
            except ...:
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            else:
                if type(event) is tuple and str(event[0].emoji) == '❌':
                    state = ConfigState.Exit
                    desc = 'Closed.'
                    await exit(desc,color,botmsg)
                else:
                    color = int(event.content, 16) + 0x0
                    tempdict["color"] = color
                    await event.delete()
                    state = ConfigState.Prefix
            for future in done:
                future.exception()
            for future in pending:
                future.cancel()  # we don't need these anymore
                
        if state == ConfigState.Prefix:
            desc = 'What prefix'
            await editmsg(botmsg,desc,color)
            await botmsg.add_reaction(emoji='❌')
            done, pending = await asyncio.wait([client.wait_for('message', check=isauthor),client.wait_for('reaction_add', check=checkemote)]
                , return_when=asyncio.FIRST_COMPLETED)
            try:
                event = done.pop().result()
            except ...:
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            else:
                if type(event) is tuple and str(event[0].emoji) == '❌':
                    state = ConfigState.Exit
                    desc = 'Closed.'
                    await exit(desc,color,botmsg)
                else:
                    tempdict["prefix"] = event.content
                    await event.delete()
                    state = ConfigState.Admin
            for future in done:
                future.exception()
            for future in pending:
                future.cancel()  # we don't need these anymore
        
        if state == ConfigState.Admin:
            tempdict["admin-role"] = None
            state = ConfigState.Verify
            
        if state == ConfigState.Verify:
            embed=discord.Embed(title='Configuration',description='Is this right: ', color=color)
            embed.add_field(name='Prefix',value=tempdict['prefix'])
            embed.add_field(name='Admin',value=tempdict["admin-role"])
            await botmsg.edit(embed=embed)
            await botmsg.add_reaction(emoji='✅')
            await botmsg.add_reaction(emoji='❌')
            try:
                event, user = await client.wait_for('reaction_add', check=checkemote)
            except asyncio.TimeoutError:
                state = ConfigState.Exit
            else:
                if str(event.emoji) == '✅':
                    await botmsg.clear_reactions()
                    state = ConfigState.Save
                else:
                    await botmsg.clear_reactions()
                    state = ConfigState.Color
            
        if state == ConfigState.Save:
            desc = 'All set up!'
            await editmsg(botmsg,desc,color)
            await botmsg.delete(delay=15)
            await oldmsg.delete()
            with open(path + str(guildid) + '.json', 'w') as json_file:
                json.dump(tempdict, json_file)
            state = ConfigState.Exit
            desc = 'Closed.'
            await exit(desc,color,botmsg)



def commandlist():               
    return {
    "config": (configcommand, [nw,testing]),
    "ip": (ipcommand, [se, nw, testing]),
    "team": (teamcommand, [se, nw, testing]),
    "help": (helpcommand, [nw, testing])    
    }

        