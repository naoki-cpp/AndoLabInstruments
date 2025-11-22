from pymeasure.instruments import Instrument

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
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    def configure_power_dBm(self, power:float):
        self.write("SOUR:POW:POW "+str(power))

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    

    def output(self, enable_output:bool):
        if(enable_output):
            self.write('OUTP 1')
        else:
            self.write('OUTP 0')

        err = self.error()
        if(err.split(',')[0] != '+0'):print(err)

        return
    
    def OPC(self):
        self.write("*OPC?")
        return
