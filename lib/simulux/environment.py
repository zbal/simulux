from disks import Disks
from memory import Memory
from cpus import CPUS
from processes import Processes

class Environment(object):
    """
    Simulated Environment, including disks, memory, etc.
    """
    def __init__(self, servers={}):
        self.servers = {}
        for name, details in servers.iteritems():
            self.servers.update({name: self.add_server(details)})

    def add_server(self, details={}):
        '''
        Add a server to the Environment
        '''
        server = {}
        server.update({'memory': Memory(details)})
        server.update({'disks': Disks(details)})
        server.update({'cpus': CPUS(details)})
        server.update({
            'processes': Processes(
                cpus=server.get('cpus'), 
                memory=server.get('memory'),
                disks=server.get('disks'),
                conf=details
            )
        })
        return server

    def add_disks(self, name, layout):
        '''
        Add disks to a server
        '''
        server = self.servers.get('name')
        if server.Disks:
            server.Disks.add_layout(layout)
        
