from.keithley6221 import Keithley6221

if __name__ == "__main__":
    keithley6221 = Keithley6221("GPIB0::2::INSTR")
    keithley6221.abort()
    keithley6221.set_sinewave_params(30, 2E-3, 0, 'BEST', 20E-3, 'Time', 999999, 1, True, 0, 1)
    keithley6221.arm_waveform_func('SIN')
