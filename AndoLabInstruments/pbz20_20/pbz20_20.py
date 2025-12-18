from pymeasure.instruments import Instrument
from enum import Enum

class PBZ20_20:
    def __init__(self, adapter, name="PBZ20_20", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('*RST')

        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def error(self):
        self.write(':SYST:ERR?')
        return self.read()
    
    def output(self, enable:bool):
        if(enable):
            self.write('OUTPut:STATe:IMMediate 1')
        else:
            self.write('OUTPut:STATe:IMMediate 0')
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return

    def set_voltage(self, voltage:float):
        self.write('VOLT ' + str(voltage))
        
        err = self.error()
        if(err.split(',')[0] != '0'):print(err)

        return
    
    def clear_protection(self):
        self.write('OUTPut:PROTection:CLEar')
        
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
            self.write('VOLTage:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.write('VOLTage:PROTection:STATe TRIP')
        return

    def set_OCP_mode(self, mode:PROT_MODE):
        '''
        Sets the mode (I or OCP) of the overcurrent protection features.
        '''
        if(mode == self.PROT_MODE.LIMIT):
            self.write('CURRent:PROTection:STATe LIMit')
        if(mode == self.PROT_MODE.TRIP):
            self.write('CURRent:PROTection:STATe TRIP')
        return
    
    def set_OVP_limit(self, under:float, over:float):
        self.write('VOLTage:PROTection:UNDer ' + str(under))
        self.write('VOLTage:PROTection:OVER ' + str(over))
        return

    def set_OCP_limit(self, under:float, over:float):
        self.write('CURRent:PROTection:UNDer ' + str(under))
        self.write('CURRent:PROTection:OVER ' + str(over))
        return
    
    def set_OVP_limit_abs(self, unsigned_limit:float):
        self.set_OVP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_OCP_limit_abs(self, unsigned_limit:float):
        self.set_OCP_limit(-1*unsigned_limit, unsigned_limit)
        return
    
    def set_soft_start_timer(self, time:float):
        self.write('TRIGger:OUTPut:SSTart:RISE ' + str(time))
