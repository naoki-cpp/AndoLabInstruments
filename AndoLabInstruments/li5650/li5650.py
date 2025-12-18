from pymeasure.instruments import Instrument
from enum import Enum

class LI5650(Instrument):
    def __init__(self, adapter, name="LI5650", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('*RST')
        return
    
    def data(self, read:bool, measurement_data:int):
        """
        setting data format

        measurement_data
        -------
        sum of the numbers below
        
        1 STATUS (16 bits = 1 word)
            Reads the measurement status.
            Measurement status content
        2 DATA1 (16 bits = 1 word)
            Reads the value of DATA1.
        4 DATA2 (16 bits = 1 word)
            Reads the value of DATA2.
        8 DATA3 (16 bits = 1 word)
            Reads the value of DATA3.
        16 DATA4 (16 bits = 1 word)
            Reads the value of DATA4.
        32 FREQ (32 bits = 2 words)
            Records the frequency value.
            The fundamental wave or primary frequency is read when the
            detection mode is SINGLE, DUAL1, or DUAL2, and the
            secondary frequency is read when the detection mode is
            CASCADE.
        """
        if(read):
            self.write('DATA?')
            return float(self.read())
        else:
            self.write('DATA ' + str(measurement_data))
            return 0
    
    def coupling(self, read:bool, coupling:str):
        """
        coupling
        --------
        AC  :AC
        DC  :DC
        """
        if(read):
            self.write(':INP:COUP?')
            return str.strip(self.read())
        else:
            self.write('INP:COUP ' + coupling)
            return ""
    
    def low(self, read:bool, grounding:str):
        """
        grounding
        -------
        float   :FLOAt
        ground  :GROund
        """
        if(read):
            self.write(':INP:LOW?')
            return str.strip(self.read())
        else:
            self.write(':INP:LOW ' + grounding)
            return ""
    
    def gain(self, read:bool, gain:str):
        """
        gain
        -------
        1MV/A 1uAmax    :IE6
        100MV/A 10nAmax :IE8
        """
        if(read):
            self.write(':INP:GAIN?')
            return str.strip(self.read())
        else:
            self.write(':INP:GAIN ' + str(gain))
            return 0
        
    def rout_signal_input(self, read:bool, input:str):
        """
        input
        -------
        A   :A
        AB  :AB
        C   :C
        I   :I
        HF  :HF
        """
        if(read):
            self.write(':ROUT?')
            return str.strip(self.read())
        else:
            self.write(':ROUT ' + input)
            return ""

    
    def set_sig(self, coupling:str, grounding:str, gain:str, input:str):
        self.coupling(False, coupling)
        self.low(False, grounding)
        self.gain(False, gain)
        self.rout_signal_input(False, input)
    
    def set_detect_mode(self, read:bool, mode:str):
        """
        mode
        ------
        SINGle  :single mode
        DUAL1   :2-frequency harmonic mode
        DUAL2   :2-frequency independent mode
        CASCade :2-frequency cascade mode
        """
        if(read):
            self.write(':SENS:DET?')
            return str.strip(self.read())
        else:
            self.write(':SENS:DET ' + mode)
            return ""

    def data1_format(self, read:bool, format:str):
        """
        X                               :REAL 
        R                               :MLINear
        Y                               :IMAGinary
        Θ                               :PHASe
        Input referred noise density    :NOISe
        AUX IN 1 voltage                :AUX1
        Xs                              :REAL2
        Rs                              :MLINear2
        """
        if(read):
            self.write(':CALC1:FORM?')
            return str.strip(self.read())
        else:
            self.write(':CALC1:FORM ' + format)
            return 0
    
    def data2_format(self, read:bool, format:str):
        """
        Y                               :IMAGinary
        Θ                               :PHASe
        Input referred noise density    :NOISe
        AUX IN 1 voltage                :AUX1
        AUX IN 2 voltage                :AUX2
        Xs                              :REAL2
        Ys                              :IMAGinary2
        Rs                              :MLINear2
        Θs                              :PHASe2
        """
        if(read):
            self.write(':CALC2:FORM?')
            return str.strip(self.read())
        else:
            self.write(':CALC2:FORM ' + format)
            return 0

    def data3_format(self, read:bool, format:str):
        """
        X                               :REAL
        R                               :MLINear
        Y                               :IMAGinary
        Θ                               :PHASe
        Xs                              :REAL2
        Rs                              :MLINear2
        """
        if(read):
            self.write(':CALC3:FORM?')
            return str.strip(self.read())
        else:
            self.write(':CALC3:FORM ' + format)
            return 0
    def data4_format(self, read:bool, format:str):
        """
        Y                               :IMAGinary
        Θ                               :PHASe
        Xs                              :REAL2
        Ys                              :IMAGinary2
        Rs                              :MLINear2
        Θs                              :PHASe2
        """
        if(read):
            self.write(':CALC4:FORM?')
            return str.strip(self.read())
        else:
            self.write(':CALC4:FORM ' + format)
            return 0
    
    def set_data_format(self, data1:str, data2:str, data3:str, data4:str):
        self.data1_format(False, data1)
        self.data2_format(False, data2)
        self.data3_format(False, data3)
        self.data4_format(False, data4)
        return
    
    def data1_offset(self, read:bool, offset:float):
        """
        """
        if(read):
            self.write(':CALC1:OFFS?')
            return str.strip(self.read())
        else:
            self.write(':CALC1:OFFS ' + str(offset))
            return 0
    
    def data2_offset(self, read:bool, offset:float):
        """
        """
        if(read):
            self.write(':CALC2:OFFS?')
            return str.strip(self.read())
        else:
            self.write(':CALC2:OFFS ' + str(offset))
            return 0

    def data3_offset(self, read:bool, offset:float):
        """
        """
        if(read):
            self.write(':CALC3:OFFS?')
            return str.strip(self.read())
        else:
            self.write(':CALC3:OFFS ' + str(offset))
            return 0
    
    def data4_offset(self, read:bool, offset:float):
        """
        """
        if(read):
            self.write(':CALC4:OFFS?')
            return str.strip(self.read())
        else:
            self.write(':CALC4:OFFS ' + str(offset))
            return 0
    
    class Detector(Enum):
        PRIMARY = 1
        SECONDARY = 2

    def volt_sensitivity(self, read:bool, detector:Detector, sensitivity:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.write(':SENS:VOLT' + str(detector.value) +':AC:RANG?')
            return str.strip(self.read())
        else:
            self.write(':SENS:VOLT' + str(detector.value) +':AC:RANG ' + str(sensitivity))
            return 0
    
    def curr_sensitivity(self, read:bool, detector:Detector, sensitivity:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.write(':SENS:CURR' + str(detector.value) +':AC:RANG?')
            return str.strip(self.read())
        else:
            self.write(':SENS:CURR' + str(detector.value) +':AC:RANG ' + str(sensitivity))
            return 0
    
    def set_sensitivity(self, detector:Detector, sensitivity:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        input = self.rout_signal_input(True, '')
        if(input == 'I'):
            self.curr_sensitivity(False, detector, sensitivity)
        else:
            self.volt_sensitivity(False, detector, sensitivity)
        return
    
    def dynamic_reserve(self, read:bool, dynamic_reserve:str):
        """
        dynamic_reserve
        ------
        high    :HIGH
        medium  :MEDium
        low     :LOW
        """
        if(read):
            self.write(':DRES?')
            return str.strip(self.read())
        else:
            self.write(':DRES ' + dynamic_reserve)
            return ""
    
    #Filter setings

    def filter_type(self, read:bool, detector:Detector, filter_slope:str):
        """
        detector
        ------
        1   :primary
        2   :secondary
        
        filter_slope
        ------
        EXPonential
        MOVing

        """
        if(read):
            self.write(':FILT' + str(detector.value) +':TYPE?')
            return str.strip(self.read())
        else:
            self.write(':FILT:TYPE ' + filter_slope)
            return ""
    def filter_time_constant(self, read:bool, detector:Detector, time_constant:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.write(':FILT' + str(detector.value) +':TCON?')
            return float(self.read())
        else:
            self.write(':FILT' + str(detector.value) +':TCON ' + str(time_constant))
            return ""
    
    def filter_slope(self, read:bool, detector:Detector, slope:int):
        """
        detector
        ------
        1   :primary
        2   :secondary

        slope
        ------
        6
        12
        18
        24
        """
        if(read):
            self.write(':FILT' + str(detector.value) +':SLOP?')
            return int(self.read())
        else:
            self.write(':FILT' + str(detector.value) +':SLOP ' + str(slope))
            return ""
    
    # reference settings
    def reference_source(self, read:bool, reference:str):
        """
        reference
        -------
        reference input     :RINPut
        internal oscilator  :IOSC
        signal input        :SINPut
        """
        if(read):
            self.write(':ROUT2?')
            return str.strip(self.read())
        else:
            self.write(':ROUT2 ' + reference)
            return ""
    
    def reference_type(self, read:bool, reference_type:str):
        """
        reference_type
        -------
        sin     :SINusoid
        pos     :TPOS
        neg     :TNEG
        """
        if(read):
            self.write(':INP2:TYPE?')
            return int(self.read())
        else:
            self.write(':INP2:TYPE ' + reference_type)
            return ""
        
    def phase_shift(self, read:bool, detector:Detector, phase_shift:float):
        if(read):
            self.write(':PHAS' + str(detector.value) +'?')
            return int(self.read())
        else:
            self.write(':PHAS' + str(detector.value) + ' ' + str(phase_shift))
            return ""
    
    def data_transfer_format(self, read:bool, format:str):
        """
        format
        ------
        ASCII   :ASCii
        real    :REAL
        integer :INTeger
        """
        if(read):
            self.write(':FORM?')
            return str.strip(self.read())
        else:
            self.write(':FORM ' + format)
            return ""
    
    def read_data(self):
        data_type = self.data_transfer_format(True, '')
        self.write(':FETC?')
        if (data_type == 'ASC'):
            data = self.read()
            return [float(x) for x in data.split(',')]
        elif data_type == 'REAL':
            return #data
        elif data_type == 'INTeger':
            return #data
    
    def enable_harmonics(self, read:bool, detector:Detector, enable:str, order:int):
        """
        detector
        ------
        1   :primary
        2   :secondary

        enable
        ------
        ON
        OFF
        """
        if(read):
            self.write(':FREQ' + str(detector.value) +':HARM?')
            freq_harm = str.strip(self.read())
            self.write(':FREQ' + str(detector.value) +':MULT?')
            freq_multi = str.strip(self.read())
            return [freq_harm, freq_multi]
        else:
            self.write(':FREQ' + str(detector.value) +':HARM ' + enable)
            if(enable == 'ON'):
                self.write(':FREQ' + str(detector.value) +':MULT ' + str(order))
            return ""
