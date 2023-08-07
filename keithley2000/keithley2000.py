import pyvisa as visa
from parse import parse
from enum import Enum

class Keithley2000():
    def __init__(self, instrument:visa.Resource):
        self.instrument = instrument
        idn = instrument.query('*IDN?')
        print(idn)
        return
       
    def __del__(self):
        self.instrument.close()
        return
    
    def initialize(self):
        self.instrument.write('*RST')
        return
    
    def error(self):
        self.instrument.write(':SYST:ERR?')
        return self.instrument.read()
    
    class Digits(Enum):
        _3H     = 4
        _4H     = 5
        _5H     = 6
        _6H     = 7
        DEFAULT = 'DEFault'
        MINIMUM = 'MINimum'
        MAXIMUM = 'MAXIMUM'
    
    class DigitalFilter(Enum):
        OFF                 = 0
        MOVING_FILTER       = 1
        REPEATING_FILTER    = 2
    
    class Reference(Enum):
        OFF     = 0
        SET     = 1
        ACQUIRE = 2

    def configure_DC_volts(self, resolution:Digits = Digits.DEFAULT, power_line_cycle:float = 1, enable_auto_range:bool = True, custom_range:float = 0, digital_filter:DigitalFilter = DigitalFilter.OFF, digital_filter_readings:int = 10, reference:Reference = Reference.OFF, reference_value:float = 0):
        self.instrument.write(":FUNC 'VOLT:DC';")

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
            
    
    def abort(self):
        self.instrument.write(':INIT:CONT OFF')
        self.instrument.write(':ABOR')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return
    
    class Source(Enum):
        IMMEDIATE   = 0
        TIMER       = 1
        MANUAL      = 2
        BUS         = 3
        EXTERNAL    = 4
    
    class CountMode(Enum):
        INFINITE    = 0
        CUSTOM      = 1

    def configure_trigger(self, source:Source = Source.IMMEDIATE, timer_delay:float = 0.001, count_mode:CountMode = CountMode.INFINITE, custom_count:int = 1, enable_auto_delay:bool = True, delay:float = 0):

        self.abort()

        if(source == self.Source.IMMEDIATE):
            self.instrument.write(':TRIG:SOUR IMM')
        if(source == self.Source.TIMER):
            self.instrument.write(':TRIG:SOUR TIM;TIM ' + str(timer_delay))
        if(source == self.Source.MANUAL):
            self.instrument.write(':TRIG:SOUR MAN')
        if(source == self.Source.BUS):
            self.instrument.write(':TRIG:SOUR BUS')
        if(source == self.Source.EXTERNAL):
            self.instrument.write(':TRIG:SOUR EXT')
        
        if(count_mode == self.CountMode.INFINITE):
            self.instrument.write(':TRIG:COUN INF')
        if(count_mode == self.CountMode.CUSTOM):
            self.instrument.write(':TRIG:COUN ' + str(custom_count))
        
        if(enable_auto_delay):
            self.instrument.write(':TRIG:DEL:AUTO ON')
        else:
            self.instrument.write(':TRIG:DEL:AUTO OFF')
            self.instrument.write(':TRIG:DEL ' + str(delay))
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return
    
    def read_single(self):
        self.instrument.write(':FORM ASC;:FORM:ELEM READ,UNIT,CHAN;')
        self.instrument.write(':DATA?')
        data = self.instrument.read().strip()
        raw, channel = data.split(',')
        raw_voltage, strings = parse("{:f}{:S}", raw)
        voltage = float(str(raw_voltage) + strings[0:4])
        unit = strings[4:]

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)
        
        return voltage, unit, channel
