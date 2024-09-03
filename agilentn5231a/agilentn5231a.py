from pymeasure.instruments import Instrument
import inspect
import pandas as pd
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

### Measurement settings
    def delete_all_measurement(self):
        self.write('CALCulate:PARameter:DELete:ALL')
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    def create_new_measurement(self, parameter:SCATTERING_PARAMETERS, channel:int = 1, measurement_name:str = 'CH1_S11_1'):
        self.write('CALC' + str(channel) +':PAR:EXT ' + measurement_name +',' +parameter.value)

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    
    def select_measurement(self, channel:int, measurement_name:str):
        self.write('CALC' + str(channel) + ':PAR:SEL ' + measurement_name)

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    
    def create_new_trace(self, parameter:SCATTERING_PARAMETERS, window:int=1, trace:int=1, channel:int = 1, measurement_name:str = 'CH1_S11_1'):
        self.create_new_measurement(parameter, channel, measurement_name)
        self.write('DISPlay:WINDow' + str(window) + ':TRACe' + str(trace) + ':FEED ' + measurement_name)
        self.select_measurement(channel, measurement_name)
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    class DISPLAY_FORMAT(Enum):
        LINEAR              =   'MLINear'
        LOG                 =   'MLOGarithmic'
        PHASE               =   'PHASe'
        UNWRAPPED_PHASE     =   'UPHase'
        IMAGINARY           =   'IMAGinary'
        REAL                =   'REAL'
        POLAR               =   'POLar'
        SMITH               =   'SMITh'
        SMITH_ADMITTANCE    =   'SADMittance'
        SWR                 =   'SWR'
        GROUP_DELAY         =   'GDELay'
        KELVIN              =   'KELVin'
        FAHRENHEIT          =   'FAHRenheit'
        CELSIUS             =   'CELSius'

    def set_display_format(self, channel, format:DISPLAY_FORMAT):
        '''
        Sets the display format for the measurement.
        '''
        self.write('CALCulate' + str(channel) + ':FORMat ' + format.value)
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    
    def set_average(self, channel:int, count:int, enable:bool):
        self.write('SENSe' + str(channel) + ':AVERage:COUNt ' + str(count))
        self.write('SENSe' + str(channel) + ':AVERage:STATe ' + str(int(enable)))
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

### Microwave settings    
    def set_bandwidth_resolution(self, channel, resolution):
        '''
        Sets the bandwidth of the digital IF filter to be used in the measurement.
        '''
        self.write('SENSe' + str(channel) + ':BANDwidth:RESolution ' + str(resolution))


### Sweep settings
    def set_start_frequency(self, frequency, channel:int = 1):
        self.write('SENS' + str(channel) + ':FREQ:STAR ' + str(frequency))
        
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    
    def set_stop_frequency(self, frequency, channel:int = 1):
        self.write('SENS' + str(channel) + ':FREQ:STOP ' + str(frequency))

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
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
        ALTERNATE   =   "NONE"

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
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
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
                self.write('SENS' + str(channel) + ':SWE:DWEL ' + str(sweep_or_dwell_time))

        if(sweep_generation == self.SWEEP_GENERATION_MODE.ANALOG):
            self.write('SENS' + str(channel) + ':SWE:GEN ANALOG')
            if(enable_auto):
                self.write('SENS' + str(channel) + ':SWE:TIME:AUTO ON')
            else:
                self.write('SENS' + str(channel) + ':SWE:TIME ' + str(sweep_or_dwell_time))

        self.write('SENS' + str(channel) + ':SWE:POIN ' + str(sweeppoints))

        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err
    
    class TRIGGER_SOURCE(Enum):
        EXTERNAL    =   'EXTernal'
        IMMEDIATE   =   'IMMediate'
        MANUAL      =   'MANual'

    class TRIGGER_SCOPE(Enum):
        ALL     =   'ALL'
        CURRENT =   'CURR'
    
    class TRIGGER_LEVEL(Enum):
        HIGH    =   'HIGH'
        LOW     =   'LOW'

    def configure_trigger_sweep_signal(self, trigger_source:TRIGGER_SOURCE, trigger_scope:TRIGGER_SCOPE, trigger_level:TRIGGER_LEVEL, delay:float = 0):
        self.write('TRIG:SOUR ' + trigger_source.value + ';')
        self.write('TRIG:SCOP ' + trigger_scope.value + ';')
        self.write('TRIG:LEV ' + trigger_level.value + ';')
        self.write('TRIG:DEL ' + str(delay) + ';')
        
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    def configure_power(self, port:int, power:float, enable_power_slope:bool = False, power_slope:float = 0, enable_auto_attenuation:bool = False, attenuation:float = 0, channel:int = 1):
        """
        power: dBm
        """
        self.write('SOUR' + str(channel) + ':POW' + str(port) + ':ATT ' + str(attenuation))
        self.write('SOUR' + str(channel) + ':POW' + str(port) + ':ATT:AUTO ' + str(int(enable_auto_attenuation)))
        self.write('SOUR' + str(channel) + ':POW' + str(port) + ' ' + str(power))
        self.write('SOUR' + str(channel) + ':POW:SLOP ' + str(power_slope))
        self.write('SOUR' + str(channel) + ':POW:SLOP:STAT ' + str(int(enable_power_slope)))
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    
    def enable_rf_power(self, enable_rf_power:bool):
        if(enable_rf_power):
            self.write('OUTP ON')
        else:
            self.write('OUTP OFF')
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    def send_immidiate_trigger(self, channel:int = 1):
        self.write('INIT' + str(channel))
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    def query_sweep_complete(self):
        self.write('STAT:OPER:DEV?')
        register = self.read()
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        if (int(register) >> 4) & 1 == 1:
            return True
        else:
            return False

##### DATA settings #####
    def get_data_catalog(self, channel):
        '''
        Returns the names and parameters of existing measurements for the specified channel.
        '''
        self.write('CALCulate' + str(channel) + ':PARameter:CATalog?')
        catalog = self.read()[1:-2].split(',')
        return catalog


    class DATA_FORMAT(Enum):
        REAL32  =   'REAL,32'
        REAL64  =   'REAL,64'
        ASCII   =   'ASCii,0'

    def set_data_format(self, format:DATA_FORMAT):
        '''
        REAL,32 - (default value for REAL) Best for transferring large amounts of measurement data.

        REAL,64 - Slower but has more significant digits than REAL,32. Use REAL,64 if you have a computer that doesn't support REAL,32.

        ASCii,0 - The easiest to implement, but very slow. Use if small amounts of data to transfer.
        '''
        self.write('FORMat:DATA ' + format.value)
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))
        return err

    class DATA_TYPE(Enum):
        FDATA   =   "FDATA"
        RDATA   =   "RDATA"
        SDATA   =   "SDATA"
        FMEM    =   "FMEM"
        SMEM    =   "SMEM"
        SDIV    =   "SDIV"
        
    def read_data(self, channel:int, data_type:DATA_TYPE):
        self.write('CALC'+ str(channel) +':DATA? ' + data_type.value)
        data = self.read()
        err = self.error()
        if(err.split(',')[0] != '+0'):
            raise Exception("Error" + str(err) + " occured in " + str(inspect.currentframe().f_back.f_code.co_name))

        return data
    
    def read_all_data(self, channel:int, data_format:DATA_FORMAT, data_type:DATA_TYPE):
        catalog = self.get_data_catalog(channel)
        measurement_names = catalog[0::2]
        parameters = catalog[1::2]
        df = pd.DataFrame()
        for measurement_name, parameter in zip(measurement_names, parameters):
            self.select_measurement(channel, measurement_name)
            self.set_data_format(data_format)
            rawdata = self.read_data(channel=channel, data_type=data_type).split(',')
            df[measurement_name] = rawdata
        return df

    def shutdown(self):
        self.enable_rf_power(False)
