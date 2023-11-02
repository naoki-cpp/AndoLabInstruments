from .keithley2000 import Keithley2000
import pyvisa as visa
    
if __name__ == "__main__":
    rm=visa.ResourceManager()
    keithley2000 = Keithley2000(rm.open_resource('GPIB0::14::INSTR'))
    keithley2000.initialize()
    keithley2000.configure_DC_volts()
    keithley2000.configure_trigger(Keithley2000.Source.IMMEDIATE)
    voltage, _, _ = keithley2000.read_single()
    print(voltage)
