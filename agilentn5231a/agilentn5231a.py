from pymeasure.instruments import Instrument
import inspect
from enum import Enum

class AgilentN5231A(Instrument):
    class SCATTERING_PARAMETERS(Enum):
        S11 = "S11"
        S12 = "S12"
        S21 = "S21"
        S22 = "S22"

    def __init__(self, adapter, name="Agilent N5231A", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )

    def error(self):
        self.write(':SYST:ERR?')
        return self.read()
    
    def reset(self):
        self.write('*RST')
        return
    
    def configure_standard_measurement(self, parameter:SCATTERING_PARAMETERS, channel:int = 1, measurement_name:str = 'CH1_S11_1'):
        self.write('CALC' + str(channel) +':PAR:EXT ' + measurement_name + ',' + parameter.value)

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    def select_measurement(self, channel:int = 1, measurement_name:str = 'CH1_S11_1'):
        self.write('CALC' + str(channel) + ':PAR:SEL ' + measurement_name)

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    def set_start_frequency(self, frequency, channel:int = 1):
        self.write('SENS' + str(channel) + ':FREQ:STAR ' + str(frequency))
        
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    def set_stop_frequency(self, frequency, channel:int = 1):
        self.write('SENS' + str(channel) + ':FREQ:STOP ' + str(frequency))

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    class SWEEP_TYPE(Enum):
        LIN     =   "LIN"
        LOG     =   "LOG"
        POW     =   "POW"
        CW      =   "CW"
        SEGM    =   "SEGM"
        PHAS    =   "PHAS"
    
    class SWEEP_MODE(Enum):
        CHOPPED     =   "ALL"
        Alternate   =   "NONE"

    def configure_sweep(self, sweep_type:SWEEP_TYPE, sweepmode:SWEEP_MODE, channel:int = 1):
        """
        ALL - Sweep mode set to Chopped - reflection and transmission measured on
        the same sweep.
        ---
        NONE - Sweep mode set to Alternate - reflection and transmission measured
        on separate sweeps. Increases sweep time
        """
        self.write('SENS' + str(channel) + ':SWE:TYPE ' + sweep_type.value)
        self.write('SENS' + str(channel) + ':COUP ' + sweepmode.value)
        
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    class SWEEP_GENERATION_MODE(Enum):
        STEP = 0
        ANALOG = 1

    def configure_sweep_generation(self, sweep_generation:SWEEP_GENERATION_MODE, enable_auto:bool, sweep_or_dwell_time:float, sweeppoints:int, channel:int = 1):
        """
        STEPped - source frequency is CONSTANT during measurement of eah
        displayed point. More accurate than ANALog. Dwell time can be set in this
        mode.
        ---
        ANALog - source frequency is continuously RAMPING during measurement
        of each displayed point. Faster than STEPped. Sweep time (not dwell time) can
        be set in this mode.
        """
        if(sweep_generation == self.SWEEP_GENERATION_MODE.STEP):
            self.write('SENS' + str(channel) + ':SWE:GEN STEP')
            if(enable_auto):
                self.write('SENS' + str(channel) + ':SWE:DWEL:AUTO ON')
            else:
                self.write('SENS' + str(channel) + '%:SWE:DWEL ' + str(sweep_or_dwell_time))

        if(sweep_generation == self.SWEEP_GENERATION_MODE.ANALOG):
            self.write('SENS' + str(channel) + ':SWE:GEN ANALOG')
            if(enable_auto):
                self.write('SENS' + str(channel) + ':SWE:TIME:AUTO ON')
            else:
                self.write('SENS' + str(channel) + '%:SWE:TIME ' + str(sweep_or_dwell_time))

        self.write('SENS' + str(channel) + 'SWE:POIN ' + str(sweeppoints))

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err
    
    class TRIGGER_SOURCE(Enum):
        IMMIDIATE   =   'IMM'
        EXTERNAL    =   'EXT'
        MANUAL      =   'MAN'
    
    class TRIGGER_SCOPE(Enum):
        ALL     =   'ALL'
        CURRENT =   'CURR'
    
    class TRIGGER_LEVEL(Enum):
        HIGH    =   'HIGH'
        LOW     =   'LOW'

    def configure_trigger_sweep_signal(self, trigger_source:TRIGGER_SOURCE, trigger_scope:TRIGGER_SCOPE, trigger_level:TRIGGER_LEVEL, delay:float = 0):
        self.write('TRIG:SOUR ' + trigger_source.value)
        self.write('SCOP ' + trigger_scope.value)
        self.write('LEV ' + trigger_level.value)
        self.write('DEL ' + str(delay))
        
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_code.co_name))
        return err

