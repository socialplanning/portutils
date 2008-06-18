#!/usr/bin/env python

import os
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



# Just to be explicit about the signalls we'll use to kill things...
# most of these are of dubious relevance, but in practice, it's
# generally good to try almost anything other than 9 before trying 9.
import signal
signals = (
    signal.SIGTERM,  # 15, terminate but allow cleanup handlers.
    signal.SIGINT,   # 2, Ctrl-C
    signal.SIGQUIT,  # 3, quit and dump core
    signal.SIGILL,   # 4, illegal instruction
    #signal.SIGTRAP,  # 5, trace/breakpoint trap
    signal.SIGABRT, # 6, process aborted. "the current operation
                    # cannot be completed but the main program can
                    # perform cleanup before exiting."
    signal.SIGBUS, # 7, bus error (improper memory handling)
    signal.SIGFPE, # 8, float exception 
    signal.SIGKILL # 9, kill
)

def portkill(*ports, **kw):
    """
    kill processes by ports
    """
    verbose = kw.get('verbose')
    sleeptime = float(kw.get('sleeptime', 0.5))
    
    for sig in signals:
        process_info = portcheck(*ports)
        if not process_info:
            break
        for port, pid in process_info.items():
            if not pid and port:
                continue
            pid = int(pid)
            port = int(port)
            # Kill the whole process group. This should help
            # with parent or child processes that don't directly touch the port.
            try:
                pgid = os.getpgid(pid)
                if verbose:
                    print "Sending signal %d to process group %d (pid %d, port %d)" % (
                        sig, pgid, pid, port)
                os.killpg(pgid, sig)
            except OSError:
                try:
                    if verbose:
                        print "Sending signal %d to pid %d (port %d)" % (sig, pid, port)
                    os.kill(pid, sig)
                except OSError:
                    if verbose:
                        print "Nothing to kill at pid %d (port %d)" % (pid, port)
        if verbose:
            print" Sleeping %f before trying again." % sleeptime
        time.sleep(sleeptime)
    if verbose:
        print "No processes left to kill."
