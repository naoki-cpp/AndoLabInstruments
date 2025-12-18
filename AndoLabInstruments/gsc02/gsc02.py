from pymeasure.instruments import Instrument
from enum import Enum

class GSC02(Instrument):
    def __init__(self, adapter, name="GSC02", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    class SpeedRange(Enum):
        LOW_SPEED   = 1
        HIGH_SPEED  = 2
    
    def set_speed(self, speed_range:SpeedRange, low_speed1:int, high_speed1:int, acceleration_time1:int, low_speed2:int, high_speed2:int, acceleration_time2:int):
        self.write('D:{:1d}S{:d}F{:d}R{:d}S{:d}F{:d}R{:d}'.format(speed_range.value, low_speed1, high_speed1, acceleration_time1, low_speed2, high_speed2, acceleration_time2))
        return
    
    class Axis(Enum):
        VERTICAL_AXIS  = '1'
        DEPTH_AXIS = '2'

    class Direction(Enum):
        FORWARD     = '+'
        BACKWARD    = '-'

    def move(self, axis:Axis, direction:Direction, pulse_num:int):
        self.write('M:' + axis.value + direction.value + 'P' + str(pulse_num))
        self.write('G')
