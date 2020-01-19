import smbus
import struct
from time import sleep

i2c_address = 0x66
COMMAND_RESET=1
NULL_I2C_VALUE=0

REGISTER_COMMAND_RESET_DISTANCE=9
REGISTER_REQ=0


def unpack(data, offset=0, limit=4):
    b = bytearray(data[offset:limit])
    f = struct.unpack('<f', b)[0]
    return f


class I2cOdom:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.counter = 0
        self.dist = None
        # Reset total distance to 0
        self.bus.write_byte_data(i2c_address, REGISTER_COMMAND_RESET_DISTANCE, NULL_I2C_VALUE)

    def run(self):
        d = self.bus.read_i2c_block_data(i2c_address, REGISTER_REQ, 8)
        vel = unpack(d)
        total_dist = unpack(d, 4, 8)
        self.counter += 1
        if self.counter % 40 == 0:
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
