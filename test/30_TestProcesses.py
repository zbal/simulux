from simulux.cpus import CPUS
from simulux.memory import Memory
from simulux.disks import Disks
from simulux.processes import Processes

from lib.utils import jsonify

# Set our environment
cpus = CPUS()
memory = Memory()
disks = Disks()

# Handle processes
processes = Processes(cpus=cpus, memory=memory, disks=disks)

def test_process_counts():
    '''
    Ensure the default processes are created
    '''
    expected_cpus = {
        'steal': [0.0, 0.0],
        'idle': [91.0, 91.0],
        'user': [3.0, 3.0],
        'irq': [0.0, 0.0],
        'iowait': [3.0, 3.0],
        'soft': [0.0, 0.0],
        'system': [3.0, 3.0],
        'guest': [0.0, 0.0],
        'nice': [0.0, 0.0]
    }
    expected_memory = {
        'used': 3072, 
        'cached': 0, 
        'free': 4191232, 
        'shared': 0, 
        'total': 4194304, 
        'buffers': 0
    }
    assert len(processes.processes) == 3
    assert jsonify(expected_cpus) == jsonify(cpus.dump())
    assert jsonify(expected_memory) == jsonify(memory.dump())

def test_kill_process():
    '''
    Ensure the killing a process by pid + release resources
    '''
    processes.kill_process(1)
    expected_cpus = {
        'steal': [0.0, 0.0],
        'idle': [94.0, 94.0],
        'user': [2.0, 2.0],
        'irq': [0.0, 0.0],
        'iowait': [2.0, 2.0],
        'soft': [0.0, 0.0],
        'system': [2.0, 2.0],
        'guest': [0.0, 0.0],
        'nice': [0.0, 0.0]
    }
    expected_memory = {
        'used': 2048, 
        'cached': 0, 
        'free': 4192256, 
        'shared': 0, 
        'total': 4194304, 
        'buffers': 0
    }
    assert len(processes.processes) == 2
    assert jsonify(expected_cpus) == jsonify(cpus.dump())
    assert jsonify(expected_memory) == jsonify(memory.dump())

def test_killall_process():
    '''
    Ensure the killing a process by name + release resources
    '''
    processes.killall_process('bash')
    expected_cpus = {
        'steal': [0.0, 0.0],
        'idle': [97.0, 97.0],
        'user': [1.0, 1.0],
        'irq': [0.0, 0.0],
        'iowait': [1.0, 1.0],
        'soft': [0.0, 0.0],
        'system': [1.0, 1.0],
        'guest': [0.0, 0.0],
        'nice': [0.0, 0.0]
    }
    expected_memory = {
        'used': 1024, 
        'cached': 0, 
        'free': 4193280, 
        'shared': 0, 
        'total': 4194304, 
        'buffers': 0
    }
    assert len(processes.processes) == 1
    assert jsonify(expected_cpus) == jsonify(cpus.dump())
    assert jsonify(expected_memory) == jsonify(memory.dump())