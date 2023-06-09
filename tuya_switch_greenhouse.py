#!/usr/bin/env python3

import tinytuya, sys

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='bf61be231bcf42e639r9zj', # presa JOLLY
    address='Auto',      # Or set to 'Auto' to auto-discover IP address
    local_key='ad46ecffe1ef0c0b', 
    version=3.3)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

if sys.argv[1].upper() == "ON":
    # Turn On
    d.turn_on()
if sys.argv[1].upper() == "OFF":
    # Turn Off
    d.turn_off()
