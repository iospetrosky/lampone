import smbus
import time

address = 0x48 # test with command: i2cdetect -y 1
A0 = 0x40 # address of the first analog input, add 1 for every successive input

bus = smbus.SMBus(1)

while True:
    bus.write_byte(address,A0)
    value = bus.read_byte(address)
    print(value)
    time.sleep(1)