from pymeasure.instruments import Instrument
from enum import Enum

class Keithley2182(Instrument):
    def __init__(self, adapter, name="Keithley2182", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('*RST;')
        return
    
    class Channel(Enum):
        VOLTAGE_CHANNEL_1 = 0
        VOLTAGE_CHANNEL_2 = 1
        TEMPERATURE_CHANNEL_1 = 2
        TEMPERATURE_CHANNEL_2 = 3

    def configure_analog_filter(self, channel:Channel, enable:bool):
        if(channel == self.Channel.VOLTAGE_CHANNEL_1):
            if(enable):
                self.write(':SENSe:VOLTage:LPASs ON;')
            else:
                self.write(':SENSe:VOLTage:LPASs OFF;')
        if(channel == self.Channel.VOLTAGE_CHANNEL_2):
            if(enable):
                self.write(':SENSe:VOLTage:CHANnel2:LPASs ON;')
            else:
                self.write(':SENSe:VOLTage:CHANnel2:LPASs OFF;')
        if(channel == self.Channel.TEMPERATURE_CHANNEL_1):
            if(enable):
                self.write(':SENSe:TEMPerature:LPASs ON;')
            else:
                self.write(':SENSe:TEMPerature:LPASs OFF;')
        if(channel == self.Channel.TEMPERATURE_CHANNEL_2):
            if(enable):
                self.write(':SENSe:TEMPerature:CHANnel2:LPASs ON;')
            else:
                self.write(':SENSe:TEMPerature:CHANnel2:LPASs OFF;')
        return

    class RateUnit(Enum):
        LINE_CYCLES = 0
        SECONDS = 1
    
    def configure_measurement(self, channel:Channel, integration_rate:int, integration_rate_units:RateUnit, sample_count:int):
        if(channel == self.Channel.VOLTAGE_CHANNEL_1):
            self.write(":SENSe:FUNCtion 'VOLT';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.write(":SENSe:VOLTage:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.write(":SENSe:VOLTage:APERture " + str(integration_rate))

        if(channel == self.Channel.VOLTAGE_CHANNEL_2):
            self.write(":SENSe:FUNCtion 'VOLT';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.write(":SENSe:VOLTage:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.write(":SENSe:VOLTage:APERture " + str(integration_rate))

        if(channel == self.Channel.TEMPERATURE_CHANNEL_1):
            self.write(":SENSe:FUNCtion 'TEMP';:SENSe:CHANnel 1;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.write(":SENSe:TEMPerature:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.write(":SENSe:TEMPerature:APERture " + str(integration_rate))

        if(channel == self.Channel.TEMPERATURE_CHANNEL_2):
            self.write(":SENSe:FUNCtion 'TEMP';:SENSe:CHANnel 2;")
            if(integration_rate_units == self.RateUnit.LINE_CYCLES):
                self.write(":SENSe:TEMPerature:NPLCycles " + str(integration_rate))
            if(integration_rate_units == self.RateUnit.SECONDS):
                self.write(":SENSe:TEMPerature:APERture " + str(integration_rate))    
        self.write(':SAMPle:COUNt ' + str(sample_count))
        return
    
    class InitiateType(Enum):
        IMMIDIATE = 0
        CONTINUOUS = 1

    def initiate_measurement(self, initiate_type:InitiateType):
        if(initiate_type == self.InitiateType.IMMIDIATE):
            self.write(':INIT:CONT OFF;:INIT;')
        if(initiate_type == self.InitiateType.CONTINUOUS):
            self.write(':INIT:CONT ON')
        return
    
    def fetch(self):
        self.write(':SENSe:DATA:FRESh?')
        return float(str.strip(self.read()))
