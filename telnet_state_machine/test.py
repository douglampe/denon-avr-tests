import time
import asyncio
import serial

from telnet_state_machine import TelnetStateMachine
from denon_serial_listener import DenonSerialListener

async def main():
    listener = DenonSerialListener()
    machine = TelnetStateMachine(listener, '192.168.1.34', 23)
    await machine.start()

asyncio.run(main())
