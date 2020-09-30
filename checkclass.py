import enum

class Status(enum.Enum):
    Online = 1
    Offline = 2
    JustOnline = 3
    JustOffline = 4

class Check:
    
    def __init__(self):
        self.tries = []
        self.cstatus = True
    
    def check(self,tf):
        
        if len(self.tries)==0:
            self.tries.insert(0,tf)
            return Status.JustOnline
        
        if len(self.tries)<3:
            self.tries.insert(0,tf)
            #print('given ' + str(tf) + ' memory is' + str(self.tries))
            return Status.Online
        
        self.tries.pop()
        self.tries.insert(0,tf)
        #if server was down and its now up then its up
        if self.tries[0] and self.tries[1] and self.tries[2] and not self.cstatus:
            self.cstatus = True
            return Status.JustOnline
        #if server was up and its now down then its down
        elif not self.tries[0] and not self.tries [1] and not self.tries[2] and self.cstatus:
            self.cstatus = False
            return Status.JustOffline
        return Status.Online if self.cstatus else Status.Offline
    
    
    
class CheckSpecificServer:
    
    def __init__(self):
        self.serverlist = {}
        
    def check(self,ip,tf):
        if not ip in self.serverlist:
            self.serverlist[ip] = Check()
        return (ip,self.serverlist[ip].check(tf))
        