from pymeasure.instruments import Instrument
from enum import Enum
import inspect

class  RohdeSchwarzSGS100A(Instrument):
    def __init__(self, adapter, name="RohdeSchwarzSGS100A", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    
    def initialize(self):
        self.write('*RST')
        return
    
    def error(self):
        self.write(':SYST:ERR:ALL?')
        return self.read()
    
    def configure_frequency(self, frequency:float):
        self.write("SOUR:FREQ "+str(frequency)+" Hz")
        
        err = self.error()
        if(err.split(',')[0] != '0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

        return
    
    def configure_power_dBm(self, power:float):
        self.write("SOUR:POW:POW "+str(power))

        err = self.error()
        if(err.split(',')[0] != '0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

        return
    

    def output(self, enable_output:bool):
        if(enable_output):
            self.write('OUTP 1')
        else:
            self.write('OUTP 0')

        err = self.error()
        if(err.split(',')[0] != '0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

        return
    
    def OPC(self):
        self.write("*OPC?")
        return self.read()
    
    class AutoLevelControlMode(Enum):
        OFFTABLE    =   'OFFTable'
        OFF         =   'OFF'
        ONTABLE     =   'ONTable'
        AUTO        =   'AUTO'
        ON          =   'ON'

    def auto_level_control(self, mode:AutoLevelControlMode):
        self.write(':SOURce:POWer:ALC:STATe '+ mode.value)
        return

    class DetectorSensitivity(Enum):
        OFF =   'OFF'
        LOW =   'LOW'
        MED =   'MED'
        HIGH=   'HIGH'

    def detector_sensitivity(self, detector_mode:DetectorSensitivity):
        self.write(':SOURce:POWer:ALC:DSENsitivity ' + detector_mode.value)
        return


