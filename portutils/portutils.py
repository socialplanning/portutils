#!/usr/bin/env python

import subprocess
import sys
import time

def netstat():
    """
    returns a dictionary of lists based on netstat
    """

    netstat_keys = [ 'Proto', 'Recv-Q', 'Send-Q', 'Local Address', 
                     'Foreign Address', 'State',  'PID/Program name',
                     'User', 'Timer' ]

    netstat = subprocess.Popen(["netstat", "-tunlp"], stdout=subprocess.PIPE).communicate()[0]
    netstat = [ i for i in netstat.split('\n') if i ]

    def parse_header(header):
        retval = {}
        index = 0

        while header:
            for key in netstat_keys:
                if header.startswith(key):
                    retval[index] = key
                    index += 1
                    header = header.lstrip(key)
                    header = header.strip()
                    break
            else:
                print "Could not find additional keys"
                sys.exit(1)

        return retval

    # find the header
    index = 0
    flag = False
    while index < len(netstat):

        line = netstat[index]
        for j in netstat_keys:
            if line.startswith(j):
                header = parse_header(line)
                flag = True
                netstat = netstat[index+1:]
                break
        if flag:
            index = len(netstat)
        index += 1

    if not flag:
        print "Header not found"
        sys.exit(1)

    retval = dict([(i,[])for i in header.values()])

    # read the file
    for line in netstat:
        line = line.split()
        for index in range(len(line)):
            retval[header[index]].append(line[index])
            
    return retval
            
def portcheck(*ports):
    """
    check a list of ports seeing if any of them are being used
    returns a dictionary with keys of the ports used
    and values the PIDs of the processes
    """
    ns = netstat()

    ports = [ str(i) for i in ports ]

    retval = {}
    for index in range(len(ns['Local Address'])):
        i = ns['Local Address'][index]
        ( address, port ) = i.rsplit(':', 1)
        if port in ports:
            retval[port] = ns['PID/Program name'][index].split('/')[0]
            try:
                int(retval[port])
            except ValueError:
                retval[port] = None

    return retval

def portkill(*ports, **kw):
    """
    kill processes by ports
    """
    verbose = kw.get('verbose')
    for signal in range(2, 10):
        ports = portcheck(*ports)
        processes = [p for p in ports.values() if p]
        if processes:
            cmd = ['kill', '-%d' % signal] + processes
            if verbose:
                print 'running:', ' '.join(cmd)
            subprocess.call(cmd)
            # Give things a bit of a chance to exit gracefully.
            time.sleep(0.5)
        else:
            if verbose:
                print "no processes left on those ports"
            break
