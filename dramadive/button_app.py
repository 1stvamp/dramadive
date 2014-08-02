#!/usr/bin/env python

from sys import exit, stderr
from time import sleep

_bytes = [0x0 for b in range(0, 8)]
_bytes[0] = 0x08
_bytes[7] = 0x02
WRITE_STRING = "".join(map(chr, _bytes))
CLOSED = 0x15
OPEN = 0x17
DEPRESSED = 0x16

def main():
    fd = open('/dev/big_red_button', 'rb+')

    last = None
    try:
        while True:
            print('.')
            data = fd.write(bytes(_bytes))
            data = fd.read(8)
            if data is not None:
                if data[0] != last and data[0] == CLOSED:
                    print('closed')
                elif data[0] != last and data[0] == OPEN:
                    print('open')
                elif data[0] == DEPRESSED:
                    print('down')
            last = data[0]
            sleep(0.1)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(e, file=stderr)
        return 1


if __name__ == '__main__':
    exit(main())
