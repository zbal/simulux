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
        'free': 4194304,
        'used': 0,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_free():
    '''
    Test set_used method to update used and free
    '''
    memory.set('free', 0)
    dump = memory.dump()
    expected = {
        'free': 0,
        'used': 4194304,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_used():
    '''
    Test set method to update used
    '''
    memory.set('used', 0)
    dump = memory.dump()
    # Cached / buffers / shared "should" be decreased (later)
    expected = {
        'free': 4194304,
        'used': 0,
        'buffers': 0,
        'cached': 0,
        'shared': 0,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_shared():
    '''
    Test set method to update shared
    '''
    memory.set('shared', 113664)
    dump = memory.dump()
    expected = {
        'free': 4080640,
        'used': 113664,
        'buffers': 0,
        'cached': 0,
        'shared': 113664,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_buffers():
    '''
    Test set method to update buffers
    '''
    memory.set('buffers', 113664)
    dump = memory.dump()
    expected = {
        'free': 3966976,
        'used': 227328,
        'buffers': 113664,
        'cached': 0,
        'shared': 113664,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_cached():
    '''
    Test set method to update cached
    '''
    memory.set('cached', 113664)
    dump = memory.dump()
    expected = {
        'free': 3853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 4194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_increase_total():
    '''
    Test increase total memory
    '''
    memory.set('total', 5194304)
    dump = memory.dump()
    expected = {
        'free': 4853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 5194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_decrease_total():
    '''
    Test decrease total memory
    '''
    memory.set('total', 3194304)
    dump = memory.dump()
    expected = {
        'free': 2853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert jsonify(dump) == jsonify(expected)

def test_decrease_total_too_much():
    '''
    Test decrease total memory by too much
    '''
    success = memory.set('total', 0)
    dump = memory.dump()
    expected = {
        'free': 2853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert success == False
    assert jsonify(dump) == jsonify(expected)

def test_update_free_reduce():
    '''
    Test update free memory (-)
    '''
    success = memory.update('free', -1)
    dump = memory.dump()
    expected = {
        'free': 2853311,
        'used': 340993,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert success == True
    assert jsonify(dump) == jsonify(expected)

def test_update_free_increase():
    '''
    Test update free memory (+)
    '''
    success = memory.update('free', 1)
    dump = memory.dump()
    expected = {
        'free': 2853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert success == True
    assert jsonify(dump) == jsonify(expected)

def test_update_buffers_reduce():
    '''
    Test update buffers memory (-)
    '''
    success = memory.update('buffers', -1)
    dump = memory.dump()
    expected = {
        'free': 2853313,
        'used': 340991,
        'buffers': 113663,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert success == True
    assert jsonify(dump) == jsonify(expected)

def test_update_buffers_increase():
    '''
    Test update buffers memory (+)
    '''
    success = memory.update('buffers', 1)
    dump = memory.dump()
    expected = {
        'free': 2853312,
        'used': 340992,
        'buffers': 113664,
        'cached': 113664,
        'shared': 113664,
        'total': 3194304
    }
    assert success == True
    assert jsonify(dump) == jsonify(expected)
