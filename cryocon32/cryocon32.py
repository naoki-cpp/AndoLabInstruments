from pymeasure.instruments import Instrument
import inspect
from enum import Enum

class Cryocon32(Instrument):
    class CHANNEL(Enum):
        CHANNEL_A = "A"
        CHANNEL_B = "B"

    class LOOP(Enum):
        LOOP_1 = "Loop 1"
        LOOP_2 = "Loop 2"

    def __init__(self, adapter, name="Cryocon32", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def read_temperature(self, channel:CHANNEL):
        self.write('INPUT? ' + channel.value)
        return self.read()
    
    def set_point(self, loop:LOOP, setpoint:float):
         self.write(loop.value + ':SETPT ' + str(setpoint)+';SETPT?')
         return self.read()
    
    def control(self):
        self.write('CONTROL')
        return
    
