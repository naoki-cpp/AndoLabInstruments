import pyvisa as visa
from enum import Enum

class Keithley2182:
    def __init__(self, instrument:visa.Resource):
        self.instrument = instrument
        idn = instrument.query('*IDN?')
        print(idn)
        return
       
    def __del__(self):
        self.instrument.close()
        return
    
    def initialize(self):
        self.instrument.write('*RST;')
        return
    
    class Channel(Enum):
        VOLTAGE_CHANNEL_1 = 0
        VOLTAGE_CHANNEL_2 = 1
        TEMPERATURE_CHANNEL_1 = 2
        TEMPERATURE_CHANNEL_2 = 3

    def configure_analog_filter(self, channel:Channel, enable:bool):
        if(channel == self.Channel.VOLTAGE_CHANNEL_1):
            if(enable):
                self.instrument.write(':SENSe:VOLTage:LPASs ON;')
            else:
                self.instrument.write(':SENSe:VOLTage:LPASs OFF;')
        if(channel == self.Channel.VOLTAGE_CHANNEL_2):
            if(enable):
                self.instrument.write(':SENSe:VOLTage:CHANnel2:LPASs ON;')
            else:
                self.instrument.write(':SENSe:VOLTage:CHANnel2:LPASs OFF;')
        if(channel == self.Channel.TEMPERATURE_CHANNEL_1):
            if(enable):
                self.instrument.write(':SENSe:TEMPerature:LPASs ON;')
            else:
                self.instrument.write(':SENSe:TEMPerature:LPASs OFF;')
        if(channel == self.Channel.TEMPERATURE_CHANNEL_2):
            if(enable):
                self.instrument.write(':SENSe:TEMPerature:CHANnel2:LPASs ON;')
            else:
                self.instrument.write(':SENSe:TEMPerature:CHANnel2:LPASs OFF;')
        return

    class RateUnit(Enum):
        LINE_CYCLES = 0
        SECONDS = 1
    
    def configure_measurement(self, channel:Channel, integration_rate:int, integration_rate_units:RateUnit, sample_count:int):
        if(channel == self.Channel.VOLTAGE_CHANNEL_1):
            self.instrument.write(":SENSe:FUNCtion 'VOLT';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.instrument.write(":SENSe:VOLTage:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.instrument.write(":SENSe:VOLTage:APERture " + str(integration_rate))

        if(channel == self.Channel.VOLTAGE_CHANNEL_2):
            self.instrument.write(":SENSe:FUNCtion 'VOLT';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.instrument.write(":SENSe:VOLTage:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.instrument.write(":SENSe:VOLTage:APERture " + str(integration_rate))

        if(channel == self.Channel.TEMPERATURE_CHANNEL_1):
            self.instrument.write(":SENSe:FUNCtion 'TEMP';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.instrument.write(":SENSe:TEMPerature:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.instrument.write(":SENSe:TEMPerature:APERture " + str(integration_rate))

        if(channel == self.Channel.TEMPERATURE_CHANNEL_2):
            self.instrument.write(":SENSe:FUNCtion 'TEMP';:SENSe:CHANnel 2;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.instrument.write(":SENSe:TEMPerature:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.instrument.write(":SENSe:TEMPerature:APERture " + str(integration_rate))    
        self.instrument.write(':SAMPle:COUNt ' + str(sample_count))
        return
    
    class InitiateType(Enum):
        IMMIDIATE = 0
        CONTINUOUS = 1

    def initiate_measurement(self, initiate_type:InitiateType):
        if(initiate_type == self.InitiateType.IMMIDIATE):
            self.instrument.write(':INIT:CONT OFF;:INIT;')
        if(initiate_type == self.InitiateType.CONTINUOUS):
            self.instrument.write(':INIT:CONT ON')
        return
    
    def fetch(self):
        self.instrument.write(':SENSe:DATA:FRESh?')
        return float(str.strip(self.instrument.read()))
