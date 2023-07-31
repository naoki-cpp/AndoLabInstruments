#%%
from .keithley2182 import Keithley2182
import pyvisa as visa
    
if __name__ == "__main__":
    rm=visa.ResourceManager()
    keithley2182 = Keithley2182(rm.open_resource('GPIB0::5::INSTR'))
    keithley2182.initialize()
    keithley2182.configure_analog_filter(Keithley2182.Channel.VOLTAGE_CHANNEL_1, False)
    keithley2182.configure_measurement(Keithley2182.Channel.VOLTAGE_CHANNEL_1, 1, Keithley2182.RateUnit.LINE_CYCLES, 1)
    keithley2182.initiate_measurement(Keithley2182.InitiateType.IMMIDIATE)
    print(keithley2182.fetch())

# %%
