# entry points

from portutils import portcheck, portkill

def portcheck_main(args=sys.argv[1:]):
    """commandline front-end to portcheck"""
    ports = portcheck(*args)
    for i in ports:
        print '%s: %s' % (i, ports[i])
        
def portkill_main(args=sys.argv[1:]):
    """commandline front-end to portkill"""
    return portkill(*args)
    