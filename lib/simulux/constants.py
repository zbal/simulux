import os
import sys

if getattr(sys, "real_prefix", None):
    DIST_DEFAULTS_PATH = os.path.join(sys.prefix, 'share/simulux/')
else:
    DIST_DEFAULTS_PATH = '/usr/share/simulux/'
    
FILES_DEFAULT_PATH = 'scenarios/fixture/'
