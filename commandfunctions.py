import discord  
from mcstatus import MinecraftServer
from configcmd import config

#######################################################################################
#                               Command Functions
#######################################################################################

def getserver(ip):
    if ip != None:
        return MinecraftServer.lookup(ip)
    else:
        return False
    
async def statuscommand(cfg):
    server = getserver(cfg.ip)
    msg = cfg.message
    color = cfg.color
    if server != False:
        query = server.query()
        latency = server.ping()
        ping = str(round(latency, 0))
        embed = discord.Embed(title='Response Time:', description=ping + ' ms', color=color)
        await msg.channel.send(embed = embed)
        if query.players.online != 0:
            #for i in query.players.names:
            embed = discord.Embed(title='Online Players:', description=str(query.players.names).strip("['']"), color=color)
        else:
            embed = discord.Embed(title='Online Players:', description='There\'s no one online...', color=color)
        await msg.channel.send(embed = embed)
    else:
        embed = discord.Embed(title='Sorry...', description='this command requires a server ip', color=color)
        await msg.channel.send(embed = embed)



async def ipcommand(cfg):
    server = getserver(cfg.ip)
    msg = cfg.message
    color = cfg.color
    if server != False:
        host = str(server.host)
        port = str(server.port)
        embed=discord.Embed(title="Server IP:", description=host+":"+port, color=color)
        await msg.channel.send(embed = embed)
    else:
        embed = discord.Embed(title='Sorry...', description='this command requires a server ip', color=color)
        await msg.channel.send(embed = embed)
    
    
    
async def teamcommand(cfg):
    gID = cfg.guildID
    msg = cfg.message
    color = cfg.color
    if gID == nw:
        embed=discord.Embed(title="NW Build Team", url='https://buildtheearth.net/bte-nw', color=color)
    elif gID == se:
        embed=discord.Embed(title="SE Build Team", url='https://buildtheearth.net/buildteams/138', color=color)
    else:
        embed=discord.Embed(title="Sorry...", description='I don\'t recognize this server.', color=color)
    await msg.channel.send(embed=embed) 



async def helpcommand(cfg):
    prfx = cfg.prefix
    msg = cfg.message
    color = cfg.color
    embed=discord.Embed(title="Commands:", color=color)
    embed.add_field(name=prfx+"ip", value="Server IP", inline=True)
    embed.add_field(name=prfx+"team", value="Build Team Link", inline=True)
    embed.add_field(name=prfx+"website", value="Website Link", inline=True)
    embed.add_field(name=prfx+"patreon", value="Patreon Link", inline=True)
    embed.add_field(name=prfx+"status", value="Server Status", inline=True)
    await msg.channel.send(embed = embed)
    pass



async def websitecommand(cfg):
    gID = cfg.guildID
    msg = cfg.message
    color = cfg.color
    if gID == nw:
        embed=discord.Embed(title="NW Website", url='https://sites.google.com/view/bte-nw/home', color=color)
    elif gID == se:
        embed=discord.Embed(title="SE Website", url='https://sites.google.com/view/southeastbte/home', color=color)
    else:
        embed=discord.Embed(title="Sorry...", description='I don\'t recognize this server.', color=color)
    await msg.channel.send(embed=embed)
    
    
    
async def patreoncommand(cfg):
    gID = cfg.guildID
    msg = cfg.message
    color = cfg.color
    if gID == nw:
        embed=discord.Embed(title="NW Patreon", url='https://www.patreon.com/btenw', color=color)
    elif gID == se:
        embed=discord.Embed(title="SE Patreon", url='https://www.patreon.com/southeastbte', color=color)
    else:
        embed=discord.Embed(title="Sorry...", description='I don\'t recognize this server.', color=color)
    await msg.channel.send(embed=embed) 
    
async def ytcommand(cfg):
    gID = cfg.guildID
    msg = cfg.message
    color = cfg.color
    if gID == nw:
        embed=discord.Embed(title="NW Youtube", url='https://www.youtube.com/channel/UC63tkSDC8MKcGD947m8xu7w', color=color)
    elif gID == se:
        embed=discord.Embed(title="SE Youtube", url='https://www.youtube.com/channel/UC1amqO2YaZSsfjuuK885SxA', color=color)
    else:
        embed=discord.Embed(title="Sorry...", description='I don\'t recognize this server.', color=color)
    await msg.channel.send(embed=embed) 



async def configcommand(cfg):
    await config(cfg)

#######################################################################################

nw = 707747343788802078
se = 723757662390583427
testing = 750500953018466361

def commandlist():               
    return {
    "config": (configcommand, [se, nw,testing]),
    "ip": (ipcommand, [se, nw, testing]),
    "team": (teamcommand, [se, nw, testing]),
    "help": (helpcommand, [se, nw, testing]),
    "website": (websitecommand, [se, nw, testing]),
    "patreon": (patreoncommand, [se, nw, testing]),
    "status": (statuscommand, [se, nw, testing]),
    "youtube": (ytcommand, [se, nw, testing])   
    }