import asyncio
import serial_asyncio


class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        transport.write(b'SI?\n')

    def data_received(self, data):
        print('data received', repr(data))

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=9600)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
