#!/usr/bin/python

# bypassPortal
VERSION = '0.6.2'
# Clay Michaels
# Dec-2014
#
# Usage: 
# python bypassPortal.py

import sys
from os import system
import paramiko
from cStringIO import StringIO
from time import sleep

# CCU CREDENTIALS
CCUUSER = '<SNIPPED USER>'
SSHKEY =('''-----BEGIN DSA PRIVATE KEY-----\n
         <SNIPPED SSH KEY>
         -----END DSA PRIVATE KEY-----''') # helpdesk.ssh

verbose = False
reboot = False
debug = False
PROJETconf = ''

def usage(  ):
    print 'USAGE:'
    print 'python bypassPortal.py [-options] [target CCU]'
    print ' '
    print '[-options] should be combined and may be included in any order.'
    print '    -d    debug mode'
    print '    -v    verbose mode'
    print '    -r    reboot the CCU after (un)bypass CAUTION!'
    print ' '
    print '[target CCU] must include the fleet name.'
    print ' '
    print 'EXAMPLE:'
    print 'python bypassPortal.py -rv amfleet1.43353'
    sys.exit(  )

# PARSE ARGUMENTS
for arg in sys.argv[ 1: ]:
    if '-' in arg:
        # Check if debug mode is desired
        if 'd' in arg:
            debug = True
        else:
            debug = False
        # Check if verbose mode is desired
        if 'v' in arg:
            verbose = True
        else:
            verbose = False
        # Check if reboot is requested
        if 'r' in arg:
            reboot = True
        else:
            reboot = False
        # Check if help requested
        if '?' in arg or 'h' in arg:
            usage(  )
#if len( sys.argv ) not in ( 2, 3):
#    usage(  )
targetCCU= sys.argv[ -1 ]

 
if verbose: print 'bypassPortal v' + VERSION

system( 'rsync -aP root@' + targetCCU + ':/conf/PROJECT.conf PROJECT.conf.temp' )
file = open( 'PROJECT.conf.temp', 'r' )
text = file.read(  ).splitlines(  )
print 'Length: ' + str( len( text ) )
print 'HEAD:'
for line in text[ :5 ]:
    print line
print 'TAIL:'
for line in text[ -5: ]:
    print line

def paramikossh():
    # SSH INTO CCU
    ccu = paramiko.SSHClient(  )
    key = paramiko.DSSKey.from_private_key( StringIO( SSHKEY ) )
    ccu.set_missing_host_key_policy( paramiko.AutoAddPolicy(  ) )
    try:
        ccu.connect( targetCCU, username = CCUUSER, pkey = key, timeout = 30 )
        channel=ccu.invoke_shell()
        stdin=channel.makefile('wb')
        stdout=channel.makefile('rb')
    except paramiko.BadAuthenticationType:
        print "Error: Bad password."
        sys.exit( 0 )
    except paramiko.SSHException:
        print "Error: Possible timeout. Try again."
        sys.exit( 0 )

    # RUN COMMANDS
    response=channel.recv( 1024 ) # dump the login cruft, motd, etc.
    channel.send( 'cat /conf/PROJECT2.conf\r' )
    sleep( 2 )
    PROJECTconf = channel.recv( 1024 ).splitlines(  )
    print 'Length: ' + str( len( PROJECTconf ) )
    print 'Head:'
    for line in PROJECTconf[ :5 ]:
        print line
    print 'Tail:'
    for line in PROJECTconf[ -5: ]:
        print line


def dummy( ):
    for line in PROJECTconf:
        if debug: print line
        if 'click_through' in line and aaa == 0: # " and aaa == 0" means this will only (un)bypass the first occurence.
            if debug: print 'found click_through'
            if line[0] == '#':
                PROJECTconf[ index ] = line[1:]
                aaa = -1
            else:
                PROJECTconf[ index ] = '#' + line
                aaa = 1
            if verbose: print PROJECTconf[ index ]
        elif 'redirect_url' in line and redirect == 0:
            if debug: print 'found redirect'
            if line[0] == '#':
                PROJECTconf[ index ] = line[1:]
                redirect = -1
            else:
                PROJECTconf[ index ] = '#' + line
                redirect = 1
            if verbose: print PROJECTconf[ index ]
        index += 1

    channel.send( 'kill ' + pid + ';reset-usb ' + wanNumber + '\r' )
    response = channel.recv( 1024 )
    if ( 'Powered up wan' + wan ) in response:
            print 'WAN' + wan + ' killed and reset successfully.'
    else:
            print 'Expected output not seen; confirm success manually.'

    # CLOSE SSH CONNECTION
    stdout.close(  )
    stdin.close(  )
    ccu.close(  )


def dummy2(  ):
    #system( 'rsync -aP root@' + targetCCU + ':/conf/PROJECT.conf PROJECT.conf' )

    file = open( '/conf/PROJECT2.conf', 'r' )
    PROJECTconf = file.read(  ).splitlines(  )
    file.close(  )
    aaa = 0
    redirect = 0
    index = 0
    for line in PROJECTconf:
        if debug: print line
        if 'click_through' in line and aaa == 0: # " and aaa == 0" means this will only (un)bypass the first occurence.
            if debug: print 'found click_through'
            if line[0] == '#':
                PROJECTconf[ index ] = line[1:]
                aaa = -1
            else:
                PROJECTconf[ index ] = '#' + line
                aaa = 1
            if verbose: print PROJECTconf[ index ]
        elif 'redirect_url' in line and redirect == 0:
            if debug: print 'found redirect'
            if line[0] == '#':
                PROJECTconf[ index ] = line[1:]
                redirect = -1
            else:
                PROJECTconf[ index ] = '#' + line
                redirect = 1
            if verbose: print PROJECTconf[ index ]
        index += 1

    file = open( '/conf/PROJECT2.conf', 'w' )
    for line in PROJECTconf:
        file.write( line + '\n' )
    file.close(  )

    if debug: system( 'cat /conf/PROJECT2.conf | grep click_' )
    if debug: system( 'cat /conf/PROJECT2.conf | grep redirect_' )
                                            
    if aaa + redirect == 2:
        print 'Portal Bypassed!'
    elif aaa + redirect == -2:
        print 'Portal UnBypassed!'
    else:
        print 'Something went wrong!'
        print 'Please check manually.'
        sys.exit(  )

    if reboot:
        print 'Rebooting...'
        subprocess.call( [ 'sync;reboot' ] )
