import time
import asyncio

from serial_state_machine import SerialStateMachine

class DenonSerialListener:
    def listen(self, data, machine):
        if data.startswith('SI'):
            self.set_zone_state(machine, 'ZONE1', data[2:])
        elif data.startswith('Z2'):
            self.set_zone_state(machine, 'ZONE2', data[2:])
        elif data.startswith('Z3'):
            self.set_zone_state(machine, 'ZONE3', data[2:])
        elif data.startswith('MVMAX'):
            machine.set_state('ZONE1_VOL_MAX', data[4:])
        elif data.startswith('MV'):
            machine.set_state('ZONE1_VOL', data[2:])
        elif data.startswith('MU'):
            machine.set_state('ZONE1_MUTE', data[2:])
        elif data.startswith('ZM'):
            machine.set_state('ZONE1', data[2:])
        elif data.startswith('SV'):
            machine.set_state('VIDEO_SELECT', data[2:])

    def set_zone_state(self, machine, key, state):
        if key == 'ON' or key == 'OFF':
            machine.set_state(key, state)
        if state == 'MUON' or state == 'MUOFF':
            machine.set_state(key + '_MUTE', state[2:])
        elif state.isnumeric() == True:
            machine.set_state(key + '_VOL', state)
        else:
            machine.set_state(key + '_INPUT', state)

    def init(self, machine):
        machine.define_command('ZONE1_INFO', lambda: machine.send(b'SI?\rMV?\rZM?\rMU?'))
        machine.define_command('ZONE2_INFO', lambda: machine.send(b'Z2?\rZ2MU?'))
        machine.define_command('ZONE3_INFO', lambda: machine.send(b'Z3?\rZ3MU?'))

    def request_status(self, machine):
        machine.send(b'SI?\rMV?\rZM?\rMU?\rZ2?\rZ2MU?\rZ3?\rZ3MU?\r')

    def write_states(self, machine):
        print('AVR STATUS:')
        for key in machine.states:
            print(key, machine.states[key])
