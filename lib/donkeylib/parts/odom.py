import smbus
import struct
from time import sleep

i2c_address = 0x66


def unpack(data, offset=0, limit=4):
    b = bytearray(data[offset:limit])
    f = struct.unpack('<f', b)[0]
    return f


class I2cOdom:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.counter = 0
        self.dist = None

    def run(self):
        d = self.bus.read_i2c_block_data(i2c_address, 0, 8)
        vel = unpack(d)
        total_dist = unpack(d, 4, 8)
        self.counter += 1
        if self.counter % 40 == 0:
            print('distance:', total_dist)
            self.counter = 0
            self.dist = total_dist

        return vel, total_dist

    def shutdown(self):
        print()
        print('distance traveled', self.dist)


if __name__ == '__main__':
    odom = I2cOdom()

    while True:
        vel, dist = odom.run()
        print('vel', vel)
        print('total dist', dist)
        sleep(2)
