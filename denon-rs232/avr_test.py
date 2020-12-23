import asyncio
import serial_asyncio

class Output(asyncio.Protocol):
    def __init__(self):
        self.data = ""

    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False

    def data_received(self, data):
        if data == b'\r':
            print(self.data)
            self.data = ""
        else:
            self.data += str(data, 'utf-8')

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

    def start(self):
        print('Establishing serial connection...')
        loop = asyncio.get_event_loop()
        transport =  serial_asyncio.create_serial_connection(loop, lambda: self, self.tty, baudrate=self.baudrate)
        loop.run_until_complete(transport)
        loop.run_forever()
        loop.close()

    def send(self, data):
        if hasattr(self, 'transport'):
            self.transport.write(data)

print('Starting...')
protocol = Output()
protocol.tty = '/dev/ttyUSB0'
protocol.baudrate = 9600
protocol.start()
protocol.send(b'SI?\r')
