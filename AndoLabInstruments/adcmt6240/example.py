#%%
from adcmt6240 import ADCMT6240
import pyvisa as visa
#%%
if __name__ == "__main__":
    rm=visa.ResourceManager() 
    adcmt6240 = ADCMT6240('GPIB0::5::INSTR')
    adcmt6240.initialize()
    adcmt6240.configure_output(ADCMT6240.SourceFunctionType.VOLTAGE, ADCMT6240.OutputModeType.DC)
    adcmt6240.configure_limiter(ADCMT6240.SourceFunctionType.VOLTAGE, 0.03) #limit 30mA
    adcmt6240.set_output_value(ADCMT6240.SourceFunctionType.VOLTAGE, 1) #output 0V
    adcmt6240.configure_trigger(ADCMT6240.TriggerMode.HOLD)  # trigger mode hold
    adcmt6240.configure_measurement(ADCMT6240.MeasurementType.CURRENT)  # current measurement
    adcmt6240.operate_output() # output on

# %%
