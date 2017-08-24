#!/usr/bin/python


# This is a simple echo script

import sys
import json
import struct

f = open('/tmp/input.txt', 'w')


def ReadMsg():

    try:
        msg = sys.stdin.read(8)
        if len(msg) != 8:
            f.write("Failed to read 8 bytes from buffer, got %i\n" % len(msg))
            f.write("%s\n" % str(msg))
            return
        (version, size) = struct.unpack("II", msg)
    except Exception as e:
        f.write("Exception while reading bytes: %s\n" % str(e))
    
    f.write("Version: %i, size: %s\n" % (version, size))
    try:
        json_raw = str(sys.stdin.read(size))
    except Exception as e:
        f.write("Exception while reading json: %s\n" % str(e))
    
    try:
        json_obj = json.loads(json_raw)
        f.write(str(json_obj))
        f.write("\n")
    except Exception as e:
        f.write("Exception while loading json: %s\n" % str(e))
    

def WriteMsg(msg):
    json_str = json.dumps(msg)
    packed = struct.pack("II", 1, len(json_str))
    sys.stdout.write(packed)
    f.write("Version: 1, length: %i\n" % len(json_str))
    f.write("Json string: %s\n" % json_str)
    sys.stdout.write(json_str)
    sys.stdout.flush()

# Read the initialization
ReadMsg()

# Send the handshake
msg = {}
msg['cvmfs_authz_v1'] = {'msgid': 1, 'revision': 0}
WriteMsg(msg)

ReadMsg()

# Always allow
msg = {}
msg['cvmfs_authz_v1'] = {'msgid': 3, 'revision': 0, 'status': 0, 'bearer_token': "aslkdflkasjkldfakljsdfaj"}
WriteMsg(msg)


f.close()




