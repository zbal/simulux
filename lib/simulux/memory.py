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
    
    def set(self, mem_type, size):
        '''
        Set memory mem_type to size
        '''
        # TODO:
        # - ensure size is within limits
        # - update shared/cached/buffer dynamically and s + c + b < used
        size = int(size)
        prev = self.data.get(mem_type, 0)
        diff = size - prev
        if mem_type in ['shared', 'cached', 'buffers']:
            # Takes memory from free and apply to used
            self.data[mem_type] = size
            self.data['free'] -= diff
            self.data['used'] += diff
            return True
        if mem_type == 'used':
            self.data['used'] = size
            self.data['free'] -= diff
            return True
        if mem_type == 'free':
            self.data['free'] = size
            self.data['used'] -= diff
            return True
        if mem_type == 'total':
            # Need to ensure total mem change maintains all memory
            # can only reduce if diff < free
            if diff < 0 and abs(diff) > self.data['free']:
                print 'Not enough memory to allow shrink - would OOM...'
                return False
            self.data['total'] = size
            self.data['free'] += diff
            return True

    def update(self, mem_type, size):
        '''
        Update memory mem_type by size (+/-)
        '''
        size = int(size)
        if mem_type in ['shared', 'cached', 'buffers']:
            # Takes memory from free and apply to used
            self.data[mem_type] += size
            self.data['free'] -= size
            self.data['used'] += size
            return True
        if mem_type == 'used':
            self.data['used'] += size
            self.data['free'] -= size
            return True
        if mem_type == 'free':
            self.data['free'] += size
            self.data['used'] -= size
            return True
        return False
        
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
