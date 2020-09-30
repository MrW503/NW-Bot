import os
import json
import discord  
import asyncio
import enum
import re

#######################################################################################

class ConfigState(enum.Enum):
    Start = 1
    Color = 2
    Prefix = 3
    IP = 4
    VoiceChannel = 5
    VerifyVoice = 6
    Admin = 7
    VerifyAll = 8
    Save = 9
    Exit = 10
 
 
 
async def exit(desc,color,botmsg):
    await botmsg.delete()
    await oldmsg.delete()
    embed=discord.Embed(title='Configuration',description=desc, color=color)
    message = await botmsg.channel.send(embed = embed)
    await message.delete(delay=10)
 
 
 
def checkemote(event, user):
    if user == oldmsg.author:
        return True
    return False
    
    
    
def isauthor(message):
    return message.author == oldmsg.author



async def checkVCexists(msg,client):
    try:
        channel = client.get_channel(int(msg))
    except ...:
        return False
    else:
        await channel.edit(name='Test Message...')
        return channel
        
   
    
async def editmsg(client,botmsg,desc,color,emojis,timeout=None):
    embed=discord.Embed(title='Configuration',description=desc, color=color)
    await botmsg.edit(embed=embed)
    for emoji in emojis:
        await botmsg.add_reaction(emoji)
    done, pending = await asyncio.wait([client.wait_for('message',timeout=timeout, check=isauthor),client.wait_for('reaction_add',timeout=timeout, check=checkemote)]
            , return_when=asyncio.FIRST_COMPLETED)
    try:
        event = done.pop().result()
    except ...:
        return '❌'
    else:
        if type(event) is tuple:
            response = event[0].emoji
        else:
            response = event.content
    for future in done:
        future.exception()
    for future in pending:
        future.cancel()
    return (response,event)

#######################################################################################

async def config(cfg):
    client = cfg.client
    gID = cfg.guildID
    msg = cfg.message
    guild = msg.guild
    color = cfg.color
    path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'
    owner = msg.guild.owner
    if msg.author != owner:
        embed = discord.Embed(title='Denied.',description='you aren\'t the owner...', color=color)
        await msg.channel.send(embed=embed)
        return
    global oldmsg
    global reaction
    path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'
    oldmsg = msg
    reaction = 0
    tempdict = {}
    botmsg = None
    state = ConfigState.Start

     
    while state != ConfigState.Exit:
        # Start -- do you want to configure?  Either go to color or exit
        if state == ConfigState.Start:
            embed = discord.Embed(title='Configuration.',description='Setting up...', color=color)
            botmsg = await msg.channel.send(embed=embed)
            
            if (str(gID) + '.json') in os.listdir(path):
                desc = 'Update the server config?'
            else:
                desc = 'This server hasn\'t been set up. React below to configure.'
            response,event = await editmsg(client,botmsg,desc,color, ['✅','❌'],timeout=30.0)
            if response == '✅':
                await botmsg.clear_reactions()
                state = ConfigState.Color
            else:
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
                
                
                    
        if state == ConfigState.Color:
            desc = 'What color should the embeds be? *Needs hex code*'
            response,event = await editmsg(client,botmsg,desc,color, ['❌'])
            if response == '❌':
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            else:
                msg = response
                match = re.search('#?([a-fA-F0-9]{6})',msg)
                if match != None:
                    color = int(match.group(1), 16) + 0x0
                    tempdict["color"] = color
                    await event.delete()
                    state = ConfigState.Prefix
                else:
                    await event.delete()
            
            
            
        if state == ConfigState.Prefix:
            desc = 'What prefix'
            response,event = await editmsg(client,botmsg,desc,color, ['❌'])
            if response == '❌':
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            else:
                msg = response
                match = re.search('^([!@#$^&*_\-=+''~`|:;<.,])$',msg)
                if match != None:
                    tempdict["prefix"] = match.group(1)
                    await event.delete()
                    state = ConfigState.IP
                else:
                    await event.delete()
                
                
                
        if state == ConfigState.IP:
            desc = 'What\'s your server IP?'
            response,event = await editmsg(client,botmsg,desc,color, ['❌'])
            if response == '❌':
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            else:
                msg = response
                tempdict["IP"] = msg
                state = ConfigState.Admin
                await event.delete()



        if state == ConfigState.Admin:
            tempdict["admin-role"] = None
            state = ConfigState.VoiceChannel
            
            
            
        if state == ConfigState.VoiceChannel:
            desc = 'Click the check for me to add the status channel.'
            response,event = await editmsg(client,botmsg,desc,color, ['✅','❌'])
            if response == '❌':
                state = ConfigState.Exit
                desc = 'Closed.'
                await exit(desc,color,botmsg)
            elif response == '✅':
                channel = await guild.create_voice_channel('Test Message...')
                state = ConfigState.VerifyVoice
                await botmsg.clear_reactions()
            else:
                pass
                # msg = response
                # channel = await checkVCexists(msg,client)
                # if channel != False:
                #     state = ConfigState.VerifyVoice
                # await event.delete()
               
               
                
        if state == ConfigState.VerifyVoice:
            desc = 'Does your voice channel say `Test Message...`?'
            response,event = await editmsg(client,botmsg,desc,color, ['✅','❌'])
            if response == '❌':
                state = ConfigState.VoiceChannel
            elif response == '✅':
                tempdict["voicechannel"] = channel.id
                await channel.edit(name='Awaiting status update...')
                await botmsg.clear_reactions()
                state = ConfigState.VerifyAll
            else:
                await event.delete()
        
        
        
        if state == ConfigState.VerifyAll:
            embed=discord.Embed(title='Configuration',description='Is this right: ', color=color)
            embed.add_field(name='Prefix',value=tempdict['prefix'])
            embed.add_field(name='Prefix',value=tempdict['IP'])
            embed.add_field(name='Admin',value=tempdict["admin-role"])
            await botmsg.edit(embed=embed)
            await botmsg.add_reaction(emoji='✅')
            await botmsg.add_reaction(emoji='❌')
            try:
                event, user = await client.wait_for('reaction_add', check=checkemote)
            except ...:
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
            embed=discord.Embed(title='Configuration',description=desc, color=color)
            await botmsg.edit(embed=embed)
            await botmsg.delete(delay=15)
            await oldmsg.delete()
            with open(path + str(gID) + '.json', 'w') as json_file:
                json.dump(tempdict, json_file)
            state = ConfigState.Exit
            desc = 'Closed.'