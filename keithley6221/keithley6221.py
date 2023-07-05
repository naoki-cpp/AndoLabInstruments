import pyvisa as visa

class Keithley6221:
    def __init__(self,instrument:visa.Resource):
        self.instrument = instrument
        idn = instrument.query('*IDN?')
        print(idn)
        return
    
    def abort(self):
        self.instrument.write(':SOUR:WAVE:ABOR')
        return
    
    def set_wave_type(self, wavetype:str):
        """
        wavetype
        -------------
        Sinusoid    :SIN
        Square      :SQU
        Ramp        :RAMP
        Arbitary0   :ARB0
        Arbitary1   :ARB1
        Arbitary2   :ARB2
        Arbitary3   :ARB3
        Arbitary4   :ARB4
        """
        self.abort()
        self.instrument.write(':SOUR:WAVE:FUNC ' + wavetype)
        return
    
    def get_wave_freq(self):
        self.instrument.write(':SOUR:WAVE:FREQ?')
        return float(self.instrument.read())
    
    def set_wave_freq(self, frequency:float):
        self.instrument.write('SOUR:WAVE:FREQ ' + str(frequency))
        return 
    
    def get_wave_amplitude(self):
        self.instrument.write(':SOUR:WAVE:AMPL?')
        return float(self.instrument.read())
     
    def set_wave_amplitude(self, amplitude:float):
        self.instrument.write(':SOUR:WAVE:AMPL ' + str(amplitude))
        return self.get_wave_amplitude()

    def get_wave_offset(self):
        self.instrument.write(':SOUR:WAVE:OFFS?')
        return float(self.instrument.read())
    
    def set_wave_offset(self, offset:float):
        self.instrument.write(':SOUR:WAVE:OFFS ' + str(offset))
        return
    
    def set_wave_ranging_mode(self, mode:str):
        """
        Fixed   :FIX
        Best    :BEST
        """
        self.instrument.write(':SOUR:WAVE:RANG ' + mode)
        return
    
    def set_current_range(self, autorange:bool, selected_range:float):
        """
        range list
        ----------
        2nA     :2E-9
        20nA    :20E-9
        200nA   :200E-9
        2uA     :2E-6
        20uA    :20E-6
        200uA   :200E-6
        2mA     :2E-3    
        20mA    :20E-3
        100mA   :100E-3
        """
        if(autorange):
            self.instrument.write('SOUR:CURR:RANG:AUTO 1')
        else:
            self.instrument.write('SOUR:CURR:RANG:AUTO 0')
            self.instrument.write('SOUR:CURR:RANG ' + str(selected_range))
        return

    def get_wave_playback_time(self):
        self.instrument.write(':SOUR:WAVE:DUR:TIME?')
        return self.instrument.read()
    
    def set_wave_playback_time(self, playback_time:float):
        self.instrument.write(':SOUR:WAVE:DUR:TIME ' + str(playback_time))
        return self.get_wave_playback_time()

    def get_wave_playback_num_cycles(self):
        self.instrument.write(':SOUR:WAVE:DUR:CYCL?')
        return self.instrument.read()

    def set_wave_playback_num_cycles(self, playback_num_cycles:float):
        self.instrument.write(':SOUR:WAVE:DUR:CYCL ' + str(playback_num_cycles))
        return self.get_wave_playback_num_cycles()
    
    def set_wave_ph_mark_enab_state(self, enabele:bool):
        if(enabele):
            self.instrument.write(':SOUR:WAVE:PMAR:STAT 1')
        else:
            self.instrument.write(':SOUR:WAVE:PMAR:STAT 0')
        return
    
    def get_wave_ph_marker(self):
        self.instrument.write(':SOUR:WAVE:PMAR:LEV?')
        return self.instrument.read()

    def set_wave_ph_marker(self,phase_marker:float):
        self.instrument.write(':SOUR:WAVE:PMAR:LEV ' + str(phase_marker))
        return self.get_wave_ph_marker()
    
    def set_wave_ph_mark_trig_link_out_line(self, trig_link_out_line:int):
        self.instrument.write('SOUR:WAVE:PMAR:OLIN ' + str(trig_link_out_line))
        return


    def set_sinewave_params(self, frequency:float, amplitude:float, offset:float, mode:str, range:float, playback_mode:str, playback_time:float, playback_cycle:float, phase_marker_enable:bool, phase_marker:float, trig_link_line:int):
        """
        playback_mode
        ----------
        Time
        Num Cycles
        """
        self.set_wave_type('SIN')
        self.set_wave_freq(frequency)
        self.set_wave_amplitude(amplitude)
        self.set_wave_offset(offset)
        self.set_wave_ranging_mode(mode)
        
        if mode == 'FIX':
            self.set_current_range(False, range)
        
        if playback_mode == "Time":
            self.set_wave_playback_time(playback_time)
        elif playback_mode == "Num Cycles":
            self.set_wave_playback_num_cycles(playback_cycle)
        self.set_wave_ph_mark_enab_state(phase_marker_enable)
        self.set_wave_ph_marker(phase_marker)
        self.set_wave_ph_mark_trig_link_out_line(trig_link_line)
        return
    
    def arm_waveform_func(self,wave_type:str, init_sweep:bool = True):
        self.set_wave_type(wave_type)
        self.instrument.write(':SOUR:WAVE:ARM')
        if(init_sweep):
            self.instrument.write(':SOUR:WAVE:INIT')
        return