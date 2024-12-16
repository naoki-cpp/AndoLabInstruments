from pymeasure.instruments import Instrument
import enum

class ZNB20(Instrument):
    def __init__(self, adapter, name="ZNB20", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def __del__(self):
        self.instrument.close()
        return
    
    def initialize(self):
        self.write('*CLS;*RST;:INITiate:CONTinuous:ALL OFF')
        return
    
    def set_update_display(self, flag:bool):
        if(flag):
            self.write('SYST:DISP:UPD ON')
        else:
            self.write('SYST:DISP:UPD OFF')
        return
    
    class TraceFormatType(enum.Enum):
        MAGNITUDE_LINEAR = "MLINear"
        MAGNITUDE_dB = "MLOGarithmic"
        PHASE = "PHASe"
        UNRAPPED_PHASE = "UPHase"
        POLAR = "POLar"
        SMITH = "SMITh"
        INVERTED_SMITH = "ISMith"
        GROUP_DELAY = "GDELay"
        REAL = "REAL"
        IMAGINARY = "IMAGinary"
        STANDING_WAVE_RATIO = "SWR"
        COMPLEX = "COMPlex"
        MAGNITUDE = "MAGNitude"


    def set_trace_format(self, channel, format:TraceFormatType):
        self.write('CALC' + str(channel) + ':FORM ' + format.value)
        return
    
    def set_trace_aperture_points(self, channel, aperture:int):
        self.write('CALC' + str(channel) + ':GDAP:SCO ' + str(aperture))
        return
    
    def configure_trace_format(self, channel, format:TraceFormatType, aperture:int):
        self.set_trace_format(channel, format)
        self.set_trace_aperture_points(channel, aperture)
        return
    
    def set_start_frequency(self, channel:int, start:float):
        self.write('SENS' + str(channel) + ':FREQ:STAR ' + str(start))
        return

    def set_stop_frequency(self, channel:int, stop:float):
        self.write('SENS' + str(channel) + ':FREQ:STOP ' + str(stop))
        return

    def set_frequency(self, channel, start, stop):
        self.set_start_frequency(channel, start)
        self.set_stop_frequency(channel, stop)
        return
    
    def add_new_trace(self, channel, tracename, out_port, in_port):
        self.write('CALC' + str(channel) + ':PAR:SDEF ' + "'" + tracename + "'" + ", 'S" + str(out_port) + str(in_port) + "'")
        return
    
    def set_existing_trace(self, channel, tracename, out_port, in_port):
        self.write('CALC' + str(channel) + ':PAR:MEAS ' + "'" + tracename + "'" + ", 'S" + str(out_port) + str(in_port) + "'")
        return
    
    def get_trace_catalog(self, channel):
        self.write('CALC' + str(channel) + ':PAR:CAT?')
        return self.read().replace("'","").strip()
    
    def set_trace(self, channel, tracename, out_port, in_port):
        tracelist = self.get_trace_catalog(channel).split(',')[::2]
        if(any(s.startswith(tracename) for s in tracelist)):
            self.set_existing_trace(channel, tracename, out_port, in_port)
        else:
            self.add_new_trace(channel, tracename, out_port, in_port)
        return
    
    def set_power(self, channel, power):
        self.write('SOUR' + str(channel) + ':POW ' + str(power))
        return
    
    def set_bandwidth(self, channel, bandwidth):
        self.write('SENS' + str(channel) + ':BAND ' + str(bandwidth))
        return
    
    def set_sweep_points(self, channel, points):
        self.write('SENS' + str(channel) + ':SWE:POIN ' + str(points))
        return

    def set_sweep_time(self, channel, time):
        self.write('SENS' + str(channel) + ':SWE:TIME ' + str(time))
        return
    
    def set_continuous_sweep(self, channel, flag:bool):
        if(flag):
            self.write('INIT' + str(channel) + ':CONT ON')
        else:
            self.write('INIT' + str(channel) + ':CONT OFF')
        return
    
    def set_sweep_count_for_all_channel(self, count):
        self.write('SENS:SWE:COUN:ALL ' + str(count))
        return

    def initiate_all(self):
        self.write('INIT:ALL')
        return
    
    def get_data_all(self, channel):
        self.write('CALC' + str(channel) + ':DATA:CALL? SDAT')
        data = self.read().strip().split(',')
        data = [float(s) for s in data]
        return data

    def set_continuous_wave(self, channel, frequency):
        self.write('SOUR' + str(channel) + ':FREQ '+ str(frequency) + 'GHz')
        return
    
    def output_on(self):
        self.write("SOUR:POW:STAR")
        return
    
    def output_off(self):
        self.write("SOUR:POW:STOP")
        return
