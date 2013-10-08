from simulux.memory import Memory
from lib.utils import jsonify

'''
The memory expected behavior is the following:
  - total = free + used
  - used = x + shared + cached + buffers

Changing shared / cached / buffers will directly change used memory - and will
reflect to free memory accordingly.

It is expected that the provided values will remain in range of available 
memory ... until we find a way to cleanly handle such out-of-range value ...
'''

memory = Memory()

def test_init_bare():
    '''
    Test class instantiation without params
    '''
    dump = memory.dump()
    expected = {
        'free': 4096,
        'used': 0,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_free():
    '''
    Test set_used method to update used and free
    '''
    memory.set_free(0)
    dump = memory.dump()
    expected = {
        'free': 0,
        'used': 4096,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_used():
    '''
    Test set_used method to update used and free
    '''
    memory.set_used(0)
    dump = memory.dump()
    # Cached / buffers / shared "should" be decreased (later)
    expected = {
        'free': 4096,
        'used': 0,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_shared():
    '''
    Test set_used method to update used and free
    '''
    memory.set_shared(111)
    dump = memory.dump()
    expected = {
        'free': 3985,
        'used': 111,
        'buffers': 0,
        'cached': 0,
        'shared': 111,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_buffers():
    '''
    Test set_used method to update used and free
    '''
    memory.set_buffers(111)
    dump = memory.dump()
    expected = {
        'free': 3874,
        'used': 222,
        'buffers': 111,
        'cached': 0,
        'shared': 111,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_cached():
    '''
    Test set_used method to update used and free
    '''
    memory.set_cached(111)
    dump = memory.dump()
    expected = {
        'free': 3763,
        'used': 333,
        'buffers': 111,
        'cached': 111,
        'shared': 111,
        'total': 4096
    }
    assert jsonify(dump) == jsonify(expected)
