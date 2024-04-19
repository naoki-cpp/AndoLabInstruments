import pyvisa as visa
from enum import Enum

class AgilentN5183A:
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

    def configure_frequency(self, frequency:float, enable_reference:bool = False, reference_frequency:float = 0, offset_frequency:float = 0, frequency_multiplier:float = 1, phase_adjustment:float = 0, phase_noise_offsets:int = 1):
        '''
        configure output frequency(Hz)
        '''
        self.instrument.write(':FREQ:MODE FIX')
        self.instrument.write(':FREQ '+ str(frequency) +' HZ;')
        if(enable_reference):
            self.instrument.write(':FREQ:REF:STAT ON')
            self.instrument.write(':FREQ:REF ' + str(reference_frequency) + ' HZ')
        else:
            self.instrument.write(':FREQ:REF:STAT OFF')
        self.instrument.write(':FREQ:OFFS ' + str(offset_frequency) +' HZ')
        self.instrument.write(':FREQ:MULT ' + str(frequency_multiplier))
        self.instrument.write(':PHAS ' + str(phase_adjustment) + ' RAD')
        self.instrument.write(':FREQ:SYNT ' + str(phase_noise_offsets))

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    def configure_power_dBm(self, power:float, enable_reference:bool = False, reference_power:float = 0, offset_power:float = 0, attenuator_auto_mode:bool = False, attenuation_level = 115):
        '''
        configure output power(dBm)
        '''
        self.instrument.write(':POW:MODE FIX')
        self.instrument.write(':POW '+ str(power) +' DBM')
        if (enable_reference):
            self.instrument.write(':POW:REF:STAT ON')
            self.instrument.write(':POW:REF ' + str(reference_power) + ' DBM')
        else:
            self.instrument.write(':POW:REF:STAT OFF')

        self.instrument.write(':POW:OFFS ' + str(offset_power) + ' DB')

        if(attenuator_auto_mode):
            self.instrument.write(':POW:ATT:AUTO ON')
            self.instrument.write(':POW:ATT ' + str(attenuation_level) + ' DB')
        else:
            self.instrument.write(':POW:ATT:AUTO OFF')
        
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
            self.instrument.write(':POW:ALC ON')
            self.instrument.write(':POW:ALC:LEV ' + str(alc_level) + ' DB')
            if(enable_automatic_bandwidth):
                self.instrument.write(':POW:ALC:BAND:AUTO ON')
            else:
                self.instrument.write(':POW:ALC:BAND:AUTO OFF')
                self.instrument.write(':POW:ALC:BAND ' + bandwidth.value)
            self.instrument.write(':POW:ALC:SOUR ' + alcsource.value)
            if(alcsource == self.ALCSource.EXTERNAL_DETECTOR):
                self.instrument.write(':POW:ALC:SOUR:EXT:COUP ' + str(external_detector_coupling_factor) +' DB')
        else:
            self.instrument.write(':POW:ALC OFF')

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    class PulseSource(Enum):
        INTERNAL = 'INT'
        EXTERNAL = 'EXT'
    
    class InternalSource(Enum):
        SQUARE = 'SQUare'
        FREE_RUN = 'FRUN'
        TRIGGERED = 'TRIGgered'
        ADJUSTABLE_DOUBLET = 'ADOublet'
        TRIGGER_DOUBLET = 'DOUBlet'
        GATED = 'GATEd'

    def configure_pulse_modulation(self, enable_pulse:bool, pulse_source:PulseSource = PulseSource.INTERNAL, internal_source:InternalSource = InternalSource.FREE_RUN, pulse_period:float = 3E-6, pulse_width = 1.5E-6):
        if(enable_pulse):
            self.instrument.write(':PULM:STAT ON')
            self.instrument.write(':PULM:SOURce ' + pulse_source.value)
            if(pulse_source == self.PulseSource.INTERNAL):
                self.instrument.write(':PULM:Source:INTernal ' + internal_source.value)
                self.instrument.write(':PULM:INTernal:PERiod ' + str(pulse_period))
                self.instrument.write(':PULM:INTernal:PWIDth ' + str(pulse_width))
                self.instrument.write(':ROUTe:TOUT PSYNc')
        else:
            self.instrument.write(':PULM:STAT OFF')
            return


        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)
        return
