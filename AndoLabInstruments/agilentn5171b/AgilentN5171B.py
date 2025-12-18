from pymeasure.instruments import Instrument
from enum import Enum

class AgilentN5171B(Instrument):
    def __init__(self, adapter, name="AgilentN5171B", **kwargs):
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
        self.write(':SYST:ERR?')
        return self.read()
    
    def configure_frequency(self, frequency:float, enable_reference:bool = False, reference_frequency:float = 0, offset_frequency:float = 0, frequency_multiplier:float = 1, phase_adjustment:float = 0, phase_noise_offsets:int = 1):
        '''
        configure output frequency(Hz)
        '''
        self.write(':FREQ:MODE FIX')
        self.write(':FREQ '+ str(frequency) +' HZ;')
        if(enable_reference):
            self.write(':FREQ:REF:STAT ON')
            self.write(':FREQ:REF ' + str(reference_frequency) + ' HZ')
        else:
            self.write(':FREQ:REF:STAT OFF')
        self.write(':FREQ:OFFS ' + str(offset_frequency) +' HZ')
        self.write(':FREQ:MULT ' + str(frequency_multiplier))
        self.write(':PHAS ' + str(phase_adjustment) + ' RAD')
        self.write(':FREQ:SYNT ' + str(phase_noise_offsets))

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    def configure_power_dBm(self, power:float, enable_reference:bool = False, reference_power:float = 0, offset_power:float = 0, attenuator_auto_mode:bool = False, attenuation_level = 115):
        '''
        configure output power(dBm)
        '''
        self.write(':POW:MODE FIX')
        self.write(':POW '+ str(power) +' DBM')
        if (enable_reference):
            self.write(':POW:REF:STAT ON')
            self.write(':POW:REF ' + str(reference_power) + ' DBM')
        else:
            self.write(':POW:REF:STAT OFF')

        self.write(':POW:OFFS ' + str(offset_power) + ' DB')

        if(attenuator_auto_mode):
            self.write(':POW:ATT:AUTO ON')
            self.write(':POW:ATT ' + str(attenuation_level) + ' DB')
        else:
            self.write(':POW:ATT:AUTO OFF')
        
        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    class ALCBandwidth(Enum):
        _100HZ = '100HZ'
        _1KHZ  = '1KHZ'
        _10KHZ = '10KHZ'
        _100KHZ= '100KHZ'
        _200HZ = '200HZ'
        _2KHZ  = '2KHZ'
        _20KHZ = '20KHZ'
    
    class ALCSource(Enum):
        INTERNAL = 'INT'
        EXTERNAL_DETECTOR = 'DIOD'
        MILLIMETER_WAVE = 'MMH'

    def configure_alc(self, enable_alc:bool, alc_level:float = 1, enable_automatic_bandwidth:bool = True, bandwidth:ALCBandwidth = ALCBandwidth._100HZ, alcsource:ALCSource = ALCSource.INTERNAL, external_detector_coupling_factor:float = 16):
        '''
        configure auto level control
        '''
        if(enable_alc):
            self.write(':POW:ALC ON')
            self.write(':POW:ALC:LEV ' + str(alc_level) + ' DB')
            if(enable_automatic_bandwidth):
                self.write(':POW:ALC:BAND:AUTO ON')
            else:
                self.write(':POW:ALC:BAND:AUTO OFF')
                self.write(':POW:ALC:BAND ' + bandwidth.value)
            self.write(':POW:ALC:SOUR ' + alcsource.value)
            if(alcsource == self.ALCSource.EXTERNAL_DETECTOR):
                self.write(':POW:ALC:SOUR:EXT:COUP ' + str(external_detector_coupling_factor) +' DB')
        else:
            self.write(':POW:ALC OFF')

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    def output(self, enable_output:bool, enable_modulation:bool = True, enable_auto_blanking:bool = True, enable_blanking:bool = True):
        if(enable_output):
            self.write(':OUTP ON')
        else:
            self.write(':OUTP OFF')

        if(enable_modulation):
            self.write(':OUTP:MOD ON')
        else:
            self.write(':OUTP:MOD OFF')
        
        if(enable_auto_blanking):
            self.write(':OUTP:BLAN:AUTO ON')
        else:
            self.write(':OUTP:BLAN:AUTO OFF')
        
        if(enable_blanking):
            self.write(':OUTP:BLAN:STAT ON')
        else:
            self.write(':OUTP:BLAN:STAT OFF')

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
