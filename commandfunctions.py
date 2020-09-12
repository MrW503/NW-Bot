import os
import json
import discord  
import asyncio
from mcstatus import MinecraftServer



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
     
 
 
 
######################

def check(reaction, user):
    if user == oldmsg.author and str(reaction.emoji) == '✅':
        reaction = 0
        return True
    elif user == oldmsg.author and str(reaction.emoji) == '❌':
        reaction = 1
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
    oldmsg = message
    reaction = 0
    path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'
    
    if (str(guildid) + '.json') in os.listdir(path):
        pass
    else:
        embed=discord.Embed(title='Configuration',description='This server hasn\'t been set up. React below to configure.', color=color)
        botmsg = await message.channel.send(embed = embed)
        await botmsg.add_reaction(emoji='✅')
        await botmsg.add_reaction(emoji='❌')
        try:
            await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await botmsg.delete()
            await oldmsg.delete()
            embed=discord.Embed(title='Configuration',description='Timed out... type .configure to reopen me.', color=color)
            message = await botmsg.channel.send(embed = embed)
            await message.delete(delay=10)
        else:
            if reaction == 0:   
                tempdict = {}
                await botmsg.clear_reactions()
                
                desc = 'What color should the embeds be? *Needs hex code*'
                await editmsg(botmsg,desc,color)
                message = await client.wait_for('message', check=isauthor)
                color = int(message.content, 16) + 0x200
                tempdict["color"] = color
                await message.delete()
                desc = 'What prefix should this server use?'
                await editmsg(botmsg,desc,color)
                #await botmsg.edit(embed=embed)
                message = await client.wait_for('message', check=isauthor)
                tempdict["prefix"] = message.content
                tempdict["admin-role"] = None
                await message.delete()
                desc = 'All set up!'
                await editmsg(botmsg,desc,color)
                await botmsg.delete(delay=15)
                with open(path + str(guildid) + '.json', 'w') as json_file:
                    json.dump(tempdict, json_file)  
            else:
                await message.delete()
                await botmsg.delete()


commandlist = {
    "config": (configcommand, [nw,testing]),
    "ip": (ipcommand, [se, nw, testing]),
    "team": (teamcommand, [se, nw, testing]),
    "help": (helpcommand, [nw, testing])    
    }

def commandlist():               
    return {
    "config": (configcommand, [nw,testing]),
    "ip": (ipcommand, [se, nw, testing]),
    "team": (teamcommand, [se, nw, testing]),
    "help": (helpcommand, [nw, testing])    
    }


            
   
        
        


# @client.event
# async def on_member_join(member):
#     channel = client.get_channel(707748041599483986)
#     embed=discord.Embed(title='Welcome to the server!',description='Check out <#707749870584332458> for info, get your roles in <#707784141550256188>, and say hi in <#712526046188273726>!', color=color)
#     embed.add_field(name="Server IP:", value="bte-nw.apexmc.co", inline=False)
#     embed.add_field(name="Our Build Team:", value="https://buildtheearth.net/bte-nw", inline=False)
#     await channel.send(embed=embed)
#     await channel.send('<@'+str(member.id)+'>')
        