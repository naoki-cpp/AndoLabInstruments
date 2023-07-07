import pyvisa as visa
from enum import Enum

class WF1948:
    def __init__(self,instrument:visa.Resource):
        self.instrument = instrument
        idn = instrument.query('*IDN?')
        print(idn)
        return
    
    def initialize(self):
        self.instrument.write('*RST')
    
    class Channel(Enum):
        CH1 = 1
        CH2 = 2

    def set_frequency(self, read:bool, channel:Channel, frequency:float, unit:str):
        """
        channel :1 or 2
        unit    :M, K, HZ, U, N, USER
        """
        if(read):
            self.instrument.write('SOUR' + str(channel) + ':FREQ?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write('SOUR' + str(channel) + ':FREQ ' + str(frequency) + unit)
            return ""
    
    def set_voltage(self, read:bool, channel:Channel, voltage:float, unit:str):
        """
        channel :1 or 2
        unit    :M, K, HZ, U, N, USER
        """
        if(read):
            self.instrument.write('SOUR' + str(channel) + ':VOLT:LEV:IMM:AMPL?')
            read_voltage = str.strip(self.instrument.read())
            self.instrument.write('SOUR' + str(channel) + ':VOLT:LEV:IMM:AMPL:UNIT?')
            read_unit = str.strip(self.instrument.read())
            return [read_voltage, read_unit]
        else:
            self.instrument.write('SOUR' + str(channel) + ':VOLT:LEV:IMM:AMPL ' + str(voltage) + unit)
            return []
        
    def set_function(self, read:bool, channel:Channel, function:str):
        """
        function
        ------
        DC          :DC
        NOISe       :noise
        SINusoid    :sine wave
        SQUare      :square wave
        PULSe       :pulse
        RAMP        :ramp
        USER        :arbitary wave
        """
        if(read):
            self.instrument.write('SOUR' + str(channel) + ':FUNC?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write('SOUR' + str(channel) + ':FUNC ' + function)
            return ""

    
    def output(self, read:bool, channel, enable:int):
        """
        enable  :0:OFF, 1:ON
        """
        if(read):
            self.instrument.write('OUTP' + str(channel) + '?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write('OUTP' + str(channel) + ' ' + str(enable))
            return
