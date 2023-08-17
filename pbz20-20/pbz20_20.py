import pyvisa as visa
from enum import Enum

class PBZ20_20:
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

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def error(self):
        self.instrument.write(':SYST:ERR?')
        return self.instrument.read()
    
    def output(self, enable:bool):
        if(enable):
            self.instrument.write('OUTPut:STATe:IMMediate 1')
        else:
            self.instrument.write('OUTPut:STATe:IMMediate 0')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return

    def set_voltage(self, voltage:float):
        self.instrument.write('VOLT ' + str(voltage))
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def clear_protection(self):
        self.instrument.write('OUTPut:PROTection:CLEar')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    class PROT_MODE(Enum):
        LIMIT   = 0
        TRIP    = 1

    def set_OVP_mode(self, mode:PROT_MODE):
        '''
        Sets the mode (V-LIMIT or OVP) of the overvoltage protection features.
        '''
        if(mode == self.PROT_MODE.LIMIT):
            self.instrument.write('VOLTage:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.instrument.write('VOLTage:PROTection:STATe TRIP')
        return

    def set_OCP_mode(self, mode:PROT_MODE):
        '''
        Sets the mode (I or OCP) of the overcurrent protection features.
        '''
        if(mode == self.PROT_MODE.LIMIT):
            self.instrument.write('CURRent:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.instrument.write('CURRent:PROTection:STATe TRIP')
        return
    
    def set_OVP_limit(self, under:float, over:float):
        self.instrument.write('VOLTage:PROTection:UNDer ' + str(under))
        self.instrument.write('VOLTage:PROTection:OVER ' + str(over))
        return

    def set_OCP_limit(self, under:float, over:float):
        self.instrument.write('CURRent:PROTection:UNDer ' + str(under))
        self.instrument.write('CURRent:PROTection:OVER ' + str(over))
        return
    
    def set_OVP_limit_abs(self, unsigned_limit:float):
        self.set_OVP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_OCP_limit_abs(self, unsigned_limit:float):
        self.set_OCP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_soft_start_timer(self, time:float):
        self.instrument.write('TRIGger:OUTPut:SSTart:RISE ' + str(time))
