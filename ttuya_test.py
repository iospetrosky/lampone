#!/usr/bin/env python3

import tinytuya
# tutorial here
# https://pypi.org/project/tinytuya/

# install system wide to be able to call via php
# sudo python3 -m pip install --system tinytuya



# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='bf61be231bcf42e639r9zj',
    address='Auto',      # Or set to 'Auto' to auto-discover IP address
    local_key='ad46ecffe1ef0c0b', 
    version=3.3)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

# Turn On
#d.turn_on()

# Turn Off
d.turn_off()