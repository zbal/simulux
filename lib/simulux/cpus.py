import os
import operator
from simulux.utils import load_json
from simulux.constants import DIST_DEFAULTS_PATH

DEFAULT_LAYOUT = os.path.join(DIST_DEFAULTS_PATH, 'cpus_layout.json')

def load_layout(layout_file=None):
    '''
    Load the layout from the config file (structured and hierarchical)
    '''
    if not layout_file:
        layout_file = DEFAULT_LAYOUT
    return load_json(layout_file)

'''
CPU object 

Define the operation related to the CPU usage.

Assumption is made as values passed as array are matching the number of cores;
ex. [1.0, 1.0] is for 2 cores - it will fail if only 1 core is defined
Also, it is expected that the number of cores / arrays of each cpu type is 
consistant! we do not have information on 1 core on idle and 4 cores on system...
'''

class CPUS(object):
    """Define a CPUS object"""
    def __init__(self):
        super(CPUS, self).__init__()
        # Set the cpu layout
        self.cores = 1

        self.data = {
            "user": [],
            "nice": [],
            "system": [],
            "iowait": [],
            "irq": [],
            "soft": [],
            "steal": [],
            "guest": [],
            "idle": []
        }

        # Set default layout
        self.set_layout()

    def set_layout(self, layout_file=None):
        '''
        Set the CPU configuration based on the default layout (or get it overriden)
        '''
        layout = load_layout(layout_file)

        self.cores = layout.get('cores')

        self.data['user'] = layout.get('user')
        self.data['nice'] = layout.get('nice')
        self.data['system'] = layout.get('system')
        self.data['iowait'] = layout.get('iowait')
        self.data['irq'] = layout.get('irq')
        self.data['soft'] = layout.get('soft')
        self.data['steal'] = layout.get('steal')
        self.data['guest'] = layout.get('guest')
        self.data['idle'] = layout.get('idle')

    def dump(self):
        '''
        Dump the CPUs information
        '''
        cpus = {
            'user': self.data['user'],
            'nice': self.data['nice'],
            'system': self.data['system'],
            'iowait': self.data['iowait'],
            'irq': self.data['irq'],
            'soft': self.data['soft'],
            'steal': self.data['steal'],
            'guest': self.data['guest'],
            'idle': self.data['idle']
        }
        return cpus

    def get(self, cpu_type, avg=False):
        '''
        Get the cpus details per type (idle, nice, system, iowait, etc.).
        By default averaged across all CPUs. Else return array of per CPU details
        '''
        # Ensure the CPU type passed as arg
        if not cpu_type in [ 'user', 'nice', 'system', 'iowait', 'irq', 'soft',
                             'steal', 'guest', 'idle' ] :
            print 'Invalid CPU type: %s' % (cpu_type,)
            return False
        # Only process cpu info that have data (and prevent divide / 0 ...)
        if len(self.data[cpu_type]) == 0:
            print 'No data available for CPU type %s' % (cpu_type,)
            return False
        # If not avgerage data - return the raw array of cpu type
        if not avg:
            return self.data[cpu_type]
        # Else, calculate the avg and return the averaged value
        total = 0
        for idx in range(self.cores):
            total += float(self.data[cpu_type][idx])
        return total / len(self.data[cpu_type])

    def set(self, cpu_type, value):
        '''
        Set the CPU for the specific cpu_type to value. Propagate the change to
        idle.
        If value is an array, propagate the change per cpu core.
        Else use the value as individual value of each array item
        '''
        # Ensure the CPU type passed as arg
        if not cpu_type in [ 'user', 'nice', 'system', 'iowait', 'irq', 'soft',
                             'steal', 'guest', 'idle' ] :
            print 'Invalid CPU type: %s' % (cpu_type,)
            return False

        # Convert the diff value to an array of float
        value = self._value_to_list(value)

        # We have values as an array of floats that we can use to modify the
        # other CPU info accordingly
        if cpu_type != 'idle':
            for idx in range(self.cores):
                # Calculate diff between prev and new value and apply change to 
                # idle cpu
                diff = value[idx] - self.data[cpu_type][idx]
                self.data['idle'][idx] -= diff
        else:
            # We are setting the idle cpu - we want to keep the ratio across the
            # other CPU type though ...
            for idx in range(self.cores):
                prev = 100.0 - self.data['idle'][idx]
                new = 100.0 - value[idx]
                for ctype in [ 'user', 'nice', 'system', 'iowait', 'irq', 'soft',
                             'steal', 'guest' ]:
                    ratio = self[ctype][idx] / prev
                    self[ctype][idx] = ratio * new
        # Now set the value of the cpu 
        self.data[cpu_type] = value
        return True

    def update(self, cpu_type, diff):
        '''
        Update cpu_type data using diff
        '''
        # Ensure the CPU type passed as arg
        if not cpu_type in [ 'user', 'nice', 'system', 'iowait', 'irq', 'soft',
                             'steal', 'guest', 'idle' ] :
            print 'Invalid CPU type: %s' % (cpu_type,)
            return False

        # Convert the diff value to an array of float
        diff = self._value_to_list(diff)

        # Compare CPU and prepare absolute value
        prev = self.get(cpu_type)
        value = []
        for idx in range(self.cores):
            value.append(prev[idx] + diff[idx])

        # Apply new CPU
        success = self.set(cpu_type, value)
        return success

    def _value_to_list(self, value):
        '''
        Ensure a provided value is matching the list requirements ...
        '''
        # TODO: better catch-phrase !
        # Check and cast the values to float
        result = []

        if type(value) == list:
            if len(value) != self.cores:
                print 'Wrong number of cores provided in value %s' % (value,)
                return False
            for idx in range(self.cores):
                if type(value[idx]) in [int, float]:
                    result.append(float(value[idx]))
                else:
                    print 'Invalid value %s (type: %s)' % (value[idx], type(value[idx]),)
                    return False
        else:
            # Force value to array
            if type(value) in [int, float]:
                value = float(value)
            else:
                print 'Invalid value %s (type: %s)' % (value, type(value),)
                return False

            for idx in range(self.cores):
                result.append(float(value))

        return result

