import os
from simulux.utils import load_json
from simulux.constants import DIST_DEFAULTS_PATH

DEFAULT_LAYOUT = os.path.join(DIST_DEFAULTS_PATH, 'memory_layout.json')

def load_layout(layout_file=None):
    '''
    Load the layout from the config file (structured and hierarchical)
    '''
    if not layout_file:
        layout_file = DEFAULT_LAYOUT
    return load_json(layout_file)

'''
Memory class:

Memory (ram) is defined by:
- used
- free
- buffers
- cached
- shared

All is stored in bytes
'''

class Memory(object):
    """Define a Memory object"""
    def __init__(self):
        super(Memory, self).__init__()

        self.data = {
            "free": 0,
            "used": 0,
            "buffers": 0,
            "shared": 0,
            "cached": 0,
            "total": 0
        }

        # Set default layout
        self.set_layout()

    def set_layout(self, layout_file=None):
        '''
        Set the Memory configuration based on the default layout (or get it overriden)
        '''
        layout = load_layout(layout_file)

        self.data.update({'free': layout.get('free')})
        self.data.update({'used': layout.get('used')})
        self.data.update({'buffers': layout.get('buffers')})
        self.data.update({'shared': layout.get('shared')})
        self.data.update({'cached': layout.get('cached')})
        self.data.update({'total': layout.get('total')})
    
    def set_used(self, size):
        '''
        Set used memory updates the free memory available
        '''
        self.data.update({'used': int(size)})
        self.data.update({'free': self.data.get('total') - self.data.get('used')})
    
    def set_free(self, size):
        '''
        Set free memory updates the used memory
        '''
        self.data.update({'free': int(size)})
        self.data.update({'used': self.data.get('total') - self.data.get('free')})
    
    def set_shared(self, size):
        '''
        Setting shared memory updates the used memory and 
        '''
        size = int(size)
        diff = self.data.get('shared') - size
        self.data.update({'shared': size})
        self.set_used(self.data.get('used') - diff)
    
    def set_buffers(self, size):
        '''
        Setting buffers memory updates the used memory and 
        '''
        size = int(size)
        diff = self.data.get('buffers') - size
        self.data.update({'buffers': size})
        self.set_used(self.data.get('used') - diff)
    
    def set_cached(self, size):
        '''
        Setting buffers memory updates the used memory and 
        '''
        size = int(size)
        diff = self.data.get('cached') - size
        self.data.update({'cached': size})
        self.set_used(self.data.get('used') - diff)
    
    def dump(self):
        '''
        Return the full memory details
        '''
        memory = {
            "total": self.data.get('total'),
            "used": self.data.get('used'),
            "free": self.data.get('free'),
            "cached": self.data.get('cached'),
            "buffers": self.data.get('buffers'),
            "shared": self.data.get('shared')
        }
        return memory
