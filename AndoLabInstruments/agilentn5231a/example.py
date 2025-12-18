from AndoLabInstruments.agilentn5231a import AgilentN5231A
import time

agilentn5231a = AgilentN5231A('GPIB0::16::INSTR')
measurement_name = 'MyMeas'
points = 1000
agilentn5231a.reset()
agilentn5231a.configure_standard_measurement(AgilentN5231A.SCATTERING_PARAMETERS.S11, measurement_name = measurement_name)
agilentn5231a.select_measurement(measurement_name = measurement_name)
agilentn5231a.set_start_frequency(1E9)
agilentn5231a.set_stop_frequency(9E9)
agilentn5231a.configure_sweep(AgilentN5231A.SWEEP_TYPE.LIN, AgilentN5231A.SWEEP_MODE.CHOPPED)
agilentn5231a.configure_sweep_generation(AgilentN5231A.SWEEP_GENERATION_MODE.ANALOG, False, 1, points)
agilentn5231a.configure_trigger_sweep_signal(AgilentN5231A.TRIGGER_SOURCE.MANUAL, AgilentN5231A.TRIGGER_SCOPE.ALL, AgilentN5231A.TRIGGER_LEVEL.LOW, 0)
agilentn5231a.configure_power(1,0)
agilentn5231a.enable_rf_power(True)
agilentn5231a.send_immidiate_trigger()
while(agilentn5231a.query_sweep_complete() == False):
    time.sleep(0.5)
rawdata = agilentn5231a.read_data(data_type = AgilentN5231A.DATA_TYPE.SDATA)
data = [float(s) for s in (rawdata.split(','))]
real = data[0::2]
imag = data[1::2]
print(real)
