import pyvisa as visa

class LI5650:
    def __init__(self,instrument:visa.Resource):
        self.instrument = instrument
        idn = instrument.query('*IDN?')
        print(idn)
        return
    
    def initialize(self):
        self.instrument.write('*RST')
        return
    
    def data(self, read:bool, measurement_data:int):
        if(read):
            self.instrument.write('DATA?')
            return float(self.instrument.read())
        else:
            self.instrument.write('DATA ' + str(measurement_data))
            return 0
    
    def coupling(self, read:bool, coupling:str):
        """
        coupling
        --------
        AC  :AC
        DC  :DC
        """
        if(read):
            self.instrument.write(':INP:COUP?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write('INP:COUP ' + coupling)
            return ""
    
    def low(self, read:bool, grounding:str):
        """
        grounding
        -------
        float   :FLOAt
        ground  :GROund
        """
        if(read):
            self.instrument.write(':INP:LOW?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':INP:LOW ' + grounding)
            return ""
    
    def gain(self, read:bool, gain:str):
        """
        gain
        -------
        1MV/A 1uAmax    :IE6
        100MV/A 10nAmax :IE8
        """
        if(read):
            self.instrument.write(':INP:GAIN?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':INP:GAIN ' + str(gain))
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
            self.instrument.write(':ROUT?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':ROUT ' + input)
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
            self.instrument.write(':SENS:DET?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':SENS:DET ' + mode)
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
            self.instrument.write(':CALC1:FORM?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':CALC1:FORM ' + format)
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
            self.instrument.write(':CALC2:FORM?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':CALC2:FORM ' + format)
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
            self.instrument.write(':CALC3:FORM?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':CALC3:FORM ' + format)
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
            self.instrument.write(':CALC4:FORM?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':CALC4:FORM ' + format)
            return 0
    
    def set_data_format(self, data1:str, data2:str, data3:str, data4:str):
        self.data1_format(False, data1)
        self.data2_format(False, data2)
        self.data3_format(False, data3)
        self.data4_format(False, data4)
        return
    
    def volt_sensitivity(self, read:bool, detector:int, sensitivity:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.instrument.write(':SENS:VOLT' + str(detector) +':AC:RANG?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':SENS:VOLT' + str(detector) +':AC:RANG ' + str(sensitivity))
            return 0
    
    def curr_sensitivity(self, read:bool, detector:int, sensitivity:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.instrument.write(':SENS:CURR' + str(detector) +':AC:RANG?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':SENS:CURR' + str(detector) +':AC:RANG ' + str(sensitivity))
            return 0
    
    def set_sensitivity(self, detector:int, sensitivity:float):
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
            self.instrument.write(':DRES?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':DRES ' + dynamic_reserve)
            return ""
    
    #Filter setings

    def filter_type(self, read:bool, detector:int, filter_slope:str):
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
            self.instrument.write(':FILT' + str(detector) +':TYPE?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':FILT:TYPE ' + filter_slope)
            return ""
    
    def filter_time_constant(self, read:bool, detector:int, time_constant:float):
        """
        detector
        ------
        1   :primary
        2   :secondary
        """
        if(read):
            self.instrument.write(':FILT' + str(detector) +':TCON?')
            return float(self.instrument.read())
        else:
            self.instrument.write(':FILT' + str(detector) +':TCON ' + str(time_constant))
            return ""
    
    def filter_slope(self, read:bool, detector:int, slope:int):
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
            self.instrument.write(':FILT' + str(detector) +':SLOP?')
            return int(self.instrument.read())
        else:
            self.instrument.write(':FILT' + str(detector) +':SLOP ' + str(slope))
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
            self.instrument.write(':ROUT2?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':ROUT2 ' + reference)
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
            self.instrument.write(':INP2:TYPE?')
            return int(self.instrument.read())
        else:
            self.instrument.write(':INP2:TYPE ' + reference_type)
            return ""
        
    def phase_shift(self, read:bool, detector:int, phase_shift:float):
        if(read):
            self.instrument.write(':PHAS' + str(detector) +'?')
            return int(self.instrument.read())
        else:
            self.instrument.write(':PHAS' + str(detector) + ' ' + str(phase_shift))
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
            self.instrument.write(':FORM?')
            return str.strip(self.instrument.read())
        else:
            self.instrument.write(':FORM ' + format)
            return ""
    
    def read_data(self):
        data_type = self.data_transfer_format(True, '')
        self.instrument.write(':FETC?')
        if (data_type == 'ASC'):
            data = self.instrument.read()
            return [float(x) for x in data.split(',')]
        elif data_type == 'REAL':
            return #data
        elif data_type == 'INTeger':
            return #data
    
    def enable_harmonics(self, read:bool, detector:int, enable:str, order:int):
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
            self.instrument.write(':FREQ' + str(detector) +':HARM?')
            freq_harm = str.strip(self.instrument.read())
            self.instrument.write(':FREQ' + str(detector) +':MULT?')
            freq_multi = str.strip(self.instrument.read())
            return [freq_harm, freq_multi]
        else:
            self.instrument.write(':FREQ' + str(detector) +':HARM ' + enable)
            if(enable == 'ON'):
                self.instrument.write(':FREQ' + str(detector) +':MULT ' + str(order))
            return ""
    
    