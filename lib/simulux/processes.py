import os
from simulux.utils import load_json
from simulux.constants import DIST_DEFAULTS_PATH

DEFAULT_LAYOUT = os.path.join(DIST_DEFAULTS_PATH, 'processes_layout.json')

def load_layout(layout_file=None):
    '''
    Load the layout from the config file (structured and hierarchical)
    '''
    if not layout_file:
        layout_file = DEFAULT_LAYOUT
    return load_json(layout_file)

'''
Processes object 

Defines the operaton related to Processes, including:
- CPU usage,
- memory usage,
- disk usage (+IO)

'''

class Processes(object):
    '''
    Meta class to handle all the processes of an environment / server
    '''
    def __init__(self, cpus={}, disks={}, memory={}):
        super(Processes, self).__init__()

        # Capture the args
        self.cpus = cpus
        self.disks = disks
        self.memory = memory

        # Store all the processes in a array
        self.processes = {}

        # Add default layout
        self.set_layout()

    def set_layout(self):
        '''
        Set the default processes layout
        '''
        layout = load_layout()

        for item in layout:
            process = Process(
                config=item, 
                cpus=self.cpus, 
                disks=self.disks,
                memory=self.memory
            )
            self.processes.update({process.get('pid'): process})

class Process(object):
    """Define a Process object"""
    def __init__(self, config={}, cpus={}, disks={}, memory={}):
        super(Process, self).__init__()

        # Capture the args
        self.config = config
        self.cpus = cpus
        self.disks = disks
        self.memory = memory

        # Propagate changes in CPU / RAM
        self.allocate_resources()

    def __del__(self):
        '''
        If instantiated object get destroyed - release resources
        '''
        self.release_resources()

    def allocate_resources(self):
        '''
        Allocate the resources used by the process
        '''
        # TODO - split per type of resource ?
        cpus = self.config.get('cpus', {})
        for cpu_type, value in cpus.iteritems():
            self.cpus.set_cpu(cpu_type, value)

        memory = self.config.get('memory', {})
        for mem_type, value in memory.iteritems():
            # Only care about RSS for the moment
            if mem_type != 'rss':
                continue
            self.memory.update('used', value)

    def release_resources(self):
        '''
        Release the resources allocated to the process
        '''
        pass
