import time
import asyncio
import serial

from serial_state_machine import SerialStateMachine
from denon_serial_listener import DenonSerialListener

async def main():
    listener = DenonSerialListener()
    machine = SerialStateMachine(listener.listen, '/dev/ttyUSB0', b'\r', 
        baudrate=9600, 
        bytesize=serial.EIGHTBITS, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        xonxoff=True, 
        rtscts=False, 
        dsrdtr=False)
    listener.init(machine)
    while True:
        listener.request_status(machine)
        await asyncio.sleep(5)
        listener.write_states(machine)

asyncio.run(main())
