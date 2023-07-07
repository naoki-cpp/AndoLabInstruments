#%%
from li5650 import LI5650
import pyvisa as visa
#%%
if __name__ == "__main__":
    rm=visa.ResourceManager() 
    li5650 = LI5650(rm.open_resource("GPIB0::7::INSTR"))
    li5650.initialize()
    li5650.data(False, 31) #set read data format. STATUS, DATA1, DATA2, DATA3, DATA4
    #Data Format
    li5650.set_detect_mode(False, 'DUAL1') #2-frequency harmonic mode
    li5650.set_data_format('REAL', 'IMAGinary', 'REAL2', 'IMAGinary2')
    #Input settings
    li5650.set_sig('AC', 'GND', 'IE6', 'A')
    li5650.dynamic_reserve(False, 'HIGH')
    #Reference signal settings
    li5650.reference_source(False, 'RINPut')
    li5650.reference_type(False, 'TPOS')
    #Primary detector settings
    li5650.phase_shift(False, LI5650.Detector.PRIMARY, 0)
    li5650.set_sensitivity(LI5650.Detector.PRIMARY,1)
    li5650.filter_type(False, LI5650.Detector.PRIMARY, 'EXPonential')
    li5650.filter_time_constant(False, LI5650.Detector.PRIMARY, 1)
    li5650.filter_slope(False, LI5650.Detector.PRIMARY, 24)
    li5650.enable_harmonics(False, LI5650.Detector.PRIMARY, 'ON', 1)
    #Secondary detector settings
    li5650.phase_shift(False, LI5650.Detector.SECONDARY, 0)
    li5650.set_sensitivity(LI5650.Detector.SECONDARY,200E-6)
    li5650.filter_type(False, LI5650.Detector.SECONDARY, 'EXPonential')
    li5650.filter_time_constant(False, LI5650.Detector.SECONDARY, 1)
    li5650.filter_slope(False, LI5650.Detector.SECONDARY, 24)
    li5650.enable_harmonics(False, LI5650.Detector.SECONDARY, 'ON', 2)

    li5650.data_transfer_format(False, 'ASCii')

    print(li5650.read_data())
