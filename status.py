import os
import json
from discord.ext import tasks
from mcstatus import MinecraftServer
from checkclass import CheckSpecificServer
from checkclass import Status

#######################################################################################

cstatus = True
tries = []
serverinfo = []
check = CheckSpecificServer()
path = os.path.dirname(os.path.realpath(__file__)) + '/Server-Configs/'

@tasks.loop(seconds=15)
async def getStatusData():
    global serverinfo
    serverinfo = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            config = json.load(f)
            serverinfo.append(config)




@tasks.loop(seconds=3)
async def checkstatus(client):
    global check
    global serverinfo
    print(serverinfo)
    for config in serverinfo:
        ip = config['IP']
        if ip == None:
            continue
        else:
            server = MinecraftServer.lookup(ip)
            try:
                _ = server.status()
            except (ConnectionRefusedError, OSError, IOError, BrokenPipeError):
                response = check.check(ip, False)
            else:
                response = check.check(ip, True)
            print(response)
            await getServer(client,config,response)



async def getServer(client,config,response):
    vc = config['voicechannel']
    channel = client.get_channel(vc)
    print(channel)
    print(response)
    if response[1] == Status.JustOnline:
        await channel.edit(name='Server Online')
    elif response[1] == Status.JustOffline:
        await channel.edit(name='Server Offline')
    else:
        pass