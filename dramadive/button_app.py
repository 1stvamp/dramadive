#!/usr/bin/env python3

import os
from select import select
from sys import exit, stderr
from time import sleep

WRITE_BYTES = [0x0 for b in range(0, 8)]
WRITE_BYTES[0] = 0x08
WRITE_BYTES[7] = 0x02
CLOSED = 0x15
OPEN = 0x17
DOWN = 0x16

def main():
    fd_id = os.open('/dev/big_red_button', os.O_RDWR|os.O_NONBLOCK)
    fd = os.fdopen(fd_id, 'rb+')

    last = None
    return_code = 0
    try:
        while True:

            data = fd.write(bytes(WRITE_BYTES))
            data = fd.read(8)
            if data is not None and data[0] != last:
                if data[0] == CLOSED:
                    print('closed')
                elif last == DOWN and data[0] == OPEN:
                    print('up')
                elif data[0] == OPEN:
                    print('open')
                elif data[0] == DOWN:
                    print('down')
                last = data[0]
            sleep(0.1)

    except KeyboardInterrupt:
        return_code = 0
    except Exception as e:
        print(e, file=stderr)
        return_code = 1
    finally:
        fd.close()

    return return_code


if __name__ == '__main__':
    exit(main())
