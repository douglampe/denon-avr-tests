import threading
import asyncio

class TelnetStateMachine(asyncio.Protocol):
    def __init__(self, listener, host, port):
        self.states = {}
        self.commands = {}
        self.queue = []

        self.listener = listener
        self.host = host
        self.port = port
        self.on_con_lost = None

    def connection_made(self, transport):
        self.transport = transport
        print('Port opened: ', transport)
        self.listener.init(self)
        print('Checking queue...')
        while self.queue:
            self.send(self.queue.pop(0))

    def data_received(self, data):
        print('Data received: ', data.decode())
        self.listener.listen(data.decode(), self)

    def connection_lost(self, exc):
        print('Connection lost. Reconnecting...')
        self.start(self.listener.listen)

    async def start(self):
        print('Establishing connection...')
        loop = asyncio.get_event_loop()
        self.on_con_lost = loop.create_future()
        transport, protocol =  await loop.create_connection(lambda: self, self.host, self.port)

        try:
            await self.on_con_lost
        finally:
            transport.close()

    def send(self, data):
        print('Sending: ', repr(data))
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
