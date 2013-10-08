from simulux.cpus import CPUS
from lib.utils import jsonify

# Global disks var to use in all the tests
cpus = CPUS()

def test_init():
    '''
    Test default load of the CPUS class
    '''
    try:
        cpus = CPUS()
    except Exception as e:
        print "Exception raised: %s" % (e)
        assert False
    assert True

def test_dump():
    '''
    Test that we receive the default CPUs dump
    '''
    dump = cpus.dump()
    expected = {
        "user": [0.0, 0.0],
        "nice": [0.0, 0.0],
        "system": [0.0, 0.0],
        "iowait": [0.0, 0.0],
        "irq": [0.0, 0.0],
        "soft": [0.0, 0.0],
        "steal": [0.0, 0.0],
        "guest": [0.0, 0.0],
        "idle": [100.0, 100.0]
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_cpu_by_avg():
    '''
    Test that we can set a value by its average
    '''
    success = cpus.set_cpu('user', 10)
    assert success == True
    dump = cpus.dump()
    expected = {
        "user": [10.0, 10.0],
        "nice": [0.0, 0.0],
        "system": [0.0, 0.0],
        "iowait": [0.0, 0.0],
        "irq": [0.0, 0.0],
        "soft": [0.0, 0.0],
        "steal": [0.0, 0.0],
        "guest": [0.0, 0.0],
        "idle": [90.0, 90.0]
    }
    assert jsonify(dump) == jsonify(expected)

def test_set_cpu_by_array():
    '''
    Test that we can set a value by a dedicated array of value per core
    '''
    success = cpus.set_cpu('iowait', [10, 50])
    assert success == True
    dump = cpus.dump()
    expected = {
        "user": [10.0, 10.0],
        "nice": [0.0, 0.0],
        "system": [0.0, 0.0],
        "iowait": [10.0, 50.0],
        "irq": [0.0, 0.0],
        "soft": [0.0, 0.0],
        "steal": [0.0, 0.0],
        "guest": [0.0, 0.0],
        "idle": [80.0, 40.0]
    }
    assert jsonify(dump) == jsonify(expected)

def test_get_cpu_raw():
    '''
    Test we can get the raw details of a cpu type
    '''
    raw_cpu = cpus.get_cpu('iowait', avg=False)
    expected = [10.0, 50.0]
    assert jsonify(raw_cpu) == jsonify(expected)

def test_get_cpu_raw():
    '''
    Test we can get the raw details of a cpu type
    '''
    avg_cpu = cpus.get_cpu('iowait')
    expected = 30.0
    assert avg_cpu == expected
