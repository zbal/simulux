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
    def __init__(self, arg=dict()):
        super(Memory, self).__init__()
        if type(arg) != dict:
            raise Exception('Invalid Memory argument')
        # Set the memory
        self.free = int(arg.get('free', 0))
        self.used = int(arg.get('used', 0))
        self.buffers = int(arg.get('buffers', 0))
        self.shared = int(arg.get('shared', 0))
        self.cached = int(arg.get('cached', 0))
        self.total = self.free + self.used
    
    def set_used(self, size):
        '''
        Set used memory updates the free memory available
        '''
        self.used = int(size)
        self.free = self.total - self.used
    
    def set_free(self, size):
        '''
        Set free memory updates the used memory
        '''
        self.free = int(size)
        self.used = self.total - self.free
    
    def set_shared(self, size):
        '''
        Setting shared memory updates the used memory and 
        '''
        size = int(size)
        diff = self.shared - size
        self.shared = size
        self.set_used(self.used - diff)
    
    def set_buffers(self, size):
        '''
        Setting buffers memory updates the used memory and 
        '''
        size = int(size)
        diff = self.buffers - size
        self.buffers = size
        self.set_used(self.used - diff)
    
    def set_cached(self, size):
        '''
        Setting buffers memory updates the used memory and 
        '''
        size = int(size)
        diff = self.cached - size
        self.cached = size
        self.set_used(self.used - diff)
    
    def dump(self):
        '''
        Return the full memory details
        '''
        memory = {
            "total": self.total,
            "used": self.used,
            "free": self.free,
            "cached": self.cached,
            "buffers": self.buffers,
            "shared": self.shared
        }
        return memory
