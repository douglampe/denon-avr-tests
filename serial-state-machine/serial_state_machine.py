import threading
import asyncio
import serial_asyncio

class SerialStateMachine(asyncio.Protocol):
    def __init__(self, listener, tty, eol, **kwargs):
        self.data = ""
        self.states = {}
        self.commands = {}
        self.queue = []

        self.serial_args = kwargs
        self.listener = listener
        self.tty = tty
        self.eol = eol

        thread = threading.Thread(target=self.start, args=())
        thread.daemon = True
        thread.start()

    def connection_made(self, transport):
        self.transport = transport
        print('Port opened: ', transport)
        transport.serial.rts = True
        print('Checking queue...')
        while self.queue:
            self.send(self.queue.pop(0))

    def data_received(self, data):
        if data == self.eol:
            self.listener(self.data, self)
            self.data = ""
        else:
            self.data += str(data, 'utf-8')

    def connection_lost(self, exc):
        print('Connection lost. Reconnecting...')
        self.start(self.listener)

    def start(self):
        print('Establishing serial connection...')
        loop = asyncio.new_event_loop()
        coro =  serial_asyncio.create_serial_connection(loop, lambda: self, self.tty, **self.serial_args)
        loop.run_until_complete(coro)
        loop.run_forever()
        loop.close()

    def send(self, data):
        if hasattr(self, 'transport'):
            self.transport.write(data)
            if hasattr(self, 'eol'):
                self.transport.write(self.eol)
        else:
            print('Queueing data: ', repr(data))
            self.queue.append(data)

    def set_state(self, key, value):
        self.states[key] = value
        print('STATE SET: ', key, value)
    
    def get_state(self, key):
        if key in self.states:
            return self.states[key]
        else:
            return ''

    def define_command(self, command, func):
        self.commands[command] = func

    def send_command(self, command, *argv, **kwargs):
        if command in self.commands:
            self.commands[command](*argv, **kwargs)
        else:
            print('Command not defined: ', command)
