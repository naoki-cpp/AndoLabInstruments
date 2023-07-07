#%%
from .wf1948 import WF1948
import pyvisa as visa
#%%
if __name__ == "__main__":
    rm=visa.ResourceManager()
    wf1948 = WF1948(rm.open_resource("GPIB0::2::INSTR"))
    wf1948.initialize()

    #Channel 1 settings
    wf1948.set_frequency(False, WF1948.Channel.CH1, 100, 'Hz')
    wf1948.set_voltage(False, WF1948.Channel.CH1, 1.0, "Vpp")
    wf1948.set_function(False, WF1948.Channel.CH1, 'SINusoid')
    wf1948.output(False, WF1948.Channel.CH1, 1)
    #Channel 2 settings
    wf1948.set_frequency(False, WF1948.Channel.CH2, 200, 'Hz')
    wf1948.set_voltage(False, WF1948.Channel.CH2, 2.0, "Vpp")
    wf1948.set_function(False, WF1948.Channel.CH2, 'SUQare')
    wf1948.output(False, WF1948.Channel.CH2, 1)
