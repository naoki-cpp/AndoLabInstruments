from keithley2000 import Keithley2000
if __name__ == "__main__":
    keithley2000 = Keithley2000('GPIB0::14::INSTR')
    #DC Voltage measurement
    keithley2000.initialize()
    keithley2000.configure_DC_volts()
    keithley2000.configure_trigger(Keithley2000.Source.IMMEDIATE)
    voltage, unit, channel = keithley2000.read_single(Keithley2000.SOURCE.FUNCTION)
    print(voltage)
    print(unit)
    print(channel)
    #Thermocouple example
    keithley2000.initialize()
    keithley2000.configure_thermocouple(Keithley2000.THERMOCOUPLE_TYPE.T, Keithley2000.REFERENCE_JUNCTION_TYPE.SIMULATED, 0)
    keithley2000.close_single_channel(1)
    keithley2000.configure_temperature(Keithley2000.RESOLUTION._6_5_Digits, Keithley2000.TEMPERATURE_UNITS.CELSIUS, Keithley2000.DIGITAL_FILTER.OFF, Keithley2000.REFERENCE_TYPE.ACQUIRE)
    keithley2000.close_single_channel(2)
    keithley2000.configure_trigger(Keithley2000.Source.IMMEDIATE)
    voltage, unit, channel = keithley2000.read_single(Keithley2000.SOURCE.FUNCTION)
    print(voltage)
    print(unit)
    print(channel)
