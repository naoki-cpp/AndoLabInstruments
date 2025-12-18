from keithley2000 import Keithley2000

if __name__ == "__main__":
    keithley2000 = Keithley2000('GPIB0::14::INSTR')
    keithley2000.initialize()
    keithley2000.configure_DC_volts()
    keithley2000.configure_trigger(Keithley2000.TriggerSource.IMMEDIATE)
    keithley2000.initiate_measurement()
    voltage, _, _ = keithley2000.read_single()
    print(voltage)
    #Thermocouple
    keithley2000.initialize()
    keithley2000.configure_thermocouple(Keithley2000.THERMOCOUPLE_TYPE.T, Keithley2000.REFERENCE_JUNCTION_TYPE.SIMULATED, 30)
    keithley2000.configure_temperature(Keithley2000.RESOLUTION._6_5_Digits,Keithley2000.TEMPERATURE_UNITS.KELVIN,Keithley2000.DIGITAL_FILTER.OFF,Keithley2000.REFERENCE_TYPE.OFF)
    keithley2000.initiate_measurement()
    voltage, unit, channel = keithley2000.read_single()
    print(voltage)
    print(unit)
    print(channel)
    
