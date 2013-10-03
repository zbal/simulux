from simulux.memory import Memory

'''
The memory expected behavior is the following:
  - total = free + used
  - used = x + shared + cached + buffers

Changing shared / cached / buffers will directly change used memory - and will
reflect to free memory accordingly.

It is expected that the provided values will remain in range of available 
memory ... until we find a way to cleanly handle such out-of-range value ...
'''

def test_init_bare():
    '''
    Test class instantiation without params
    '''
    memory = Memory()
    assert memory.free == 0
    assert memory.used == 0
    assert memory.buffers == 0
    assert memory.cached == 0
    assert memory.shared == 0
    assert memory.total == 0

def test_init_with_params():
    '''
    Test class instantiation with params
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 1234
    }
    memory = Memory(params)
    assert memory.free == 1234
    assert memory.used == 1234
    assert memory.buffers == 0
    assert memory.cached == 1234
    assert memory.shared == 0
    assert memory.total == 2468

def test_set_used():
    '''
    Test set_used method to update used and free
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 1234
    }
    memory = Memory(params)
    memory.set_used(0)
    assert memory.free == 2468
    assert memory.used == 0
    # Cached / buffers / shared "should" be decreased (later)
    assert memory.buffers == 0
    assert memory.cached == 1234
    assert memory.shared == 0
    assert memory.total == 2468

def test_set_free():
    '''
    Test set_used method to update used and free
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 1234
    }
    memory = Memory(params)
    memory.set_free(0)
    assert memory.free == 0
    assert memory.used == 2468
    assert memory.buffers == 0
    assert memory.cached == 1234
    assert memory.shared == 0
    assert memory.total == 2468

def test_set_shared():
    '''
    Test set_used method to update used and free
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 1234
    }
    memory = Memory(params)
    memory.set_shared(111)
    assert memory.free == 1123
    assert memory.used == 1345
    assert memory.buffers == 0
    assert memory.cached == 1234
    assert memory.shared == 111
    assert memory.total == 2468

def test_set_buffers():
    '''
    Test set_used method to update used and free
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 1234
    }
    memory = Memory(params)
    memory.set_buffers(111)
    assert memory.free == 1123
    assert memory.used == 1345
    assert memory.buffers == 111
    assert memory.cached == 1234
    assert memory.shared == 0
    assert memory.total == 2468

def test_set_cached():
    '''
    Test set_used method to update used and free
    '''
    params = {
        'free': 1234, 
        'used': 1234, 
        'cached': 321
    }
    memory = Memory(params)
    memory.set_cached(111)
    assert memory.free == 1444
    assert memory.used == 1024
    assert memory.buffers == 0
    assert memory.cached == 111
    assert memory.shared == 0
    assert memory.total == 2468
