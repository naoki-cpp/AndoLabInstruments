from .li5650 import LI5650
import pyvisa as visa

if __name__ == "__main__":
    rm=visa.ResourceManager() 
    li5650 = LI5650(rm.open_resource("GPIB0::7::INSTR"))
    li5650.initialize()
    li5650.data(False, 31)
    #Data Format
    li5650.set_detect_mode(False, 'DUAL1')
    li5650.set_data_format('REAL', 'IMAGinary', 'REAL2', 'IMAGinary2')
    #Input settings
    li5650.set_sig('AC', 'GND', 'IE6', 'A')
    li5650.dynamic_reserve(False, 'HIGH')
    #Reference signal settings
    li5650.reference_source(False, 'RINPut')
    li5650.reference_type(False, 'TPOS')
    li5650.phase_shift(False, 1, 0)
    #Primary detector settings
    li5650.set_sensitivity(1,1)
    li5650.filter_type(False, 1, 'EXPonential')
    li5650.filter_time_constant(False, 1, 1)
    li5650.filter_slope(False, 1, 24)
    li5650.enable_harmonics(False, 1, 'ON', 1)
    #Secondary detector settings
    li5650.set_sensitivity(2,200E-6)
    li5650.filter_type(False, 2, 'EXPonential')
    li5650.filter_time_constant(False, 2, 1)
    li5650.filter_slope(False, 2, 24)
    li5650.enable_harmonics(False, 2, 'ON', 2)
    li5650.data_transfer_format(False, 'ASCii')

    print(li5650.read_data())
