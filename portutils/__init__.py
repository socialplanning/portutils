# entry points

import sys
from portutils import portcheck, portkill

def portcheck_main(args=sys.argv[1:]):
    """commandline front-end to portcheck"""
    ports = portcheck(*args)
    for i in ports:
        print '%s: %s' % (i, ports[i])
    return 0
        
def portkill_main(args=sys.argv[1:]):
    """commandline front-end to portkill"""
    return int(not portkill(*args))
    
