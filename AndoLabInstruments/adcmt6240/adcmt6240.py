from pymeasure.instruments import Instrument
from enum import Enum

class ADCMT6240(Instrument):
    
    def __init__(self, adapter, name="ADCMT6240", **kwargs):
        super().__init__(
            adapter,
            name,
            includeSCPI = False,
            **kwargs
        )
    
    def initialize(self):
        self.write('C,*RST')
        return
    
    class SourceFunctionType(Enum):
        VOLTAGE = 0
        CURRENT = 1
    
    class OutputModeType(Enum):
        DC = 0
        PULSE = 1
        SWEEP = 2
        PULSE_SWEEP = 3

    
    def configure_output(self, source_function:SourceFunctionType, output_mode:OutputModeType):
        source_map = {
            self.SourceFunctionType.VOLTAGE: 'VF',
            self.SourceFunctionType.CURRENT: 'IF'
        }
        output_map = {
            self.OutputModeType.DC:         'MD0',
            self.OutputModeType.PULSE:      'MD1',
            self.OutputModeType.SWEEP:      'MD2',
            self.OutputModeType.PULSE_SWEEP:'MD3'
        }
        self.write(source_map[source_function])
        self.write(output_map[output_mode])
        return
    
    def set_output_value(self, source_function:SourceFunctionType, outputvalue:float):
        source_map = {
            self.SourceFunctionType.VOLTAGE: 'SOV',
            self.SourceFunctionType.CURRENT: 'SOI'
        }
        self.write(source_map[source_function] + str(outputvalue))
        return
    
    def get_output_value(self, source_function:SourceFunctionType):
        source_map = {
            self.SourceFunctionType.VOLTAGE: 'SOV',
            self.SourceFunctionType.CURRENT: 'SOI'
        }
        self.write(source_map[source_function] + '?')
        return float(self.read().strip()[3:])

    def configure_limiter(self, source_function:SourceFunctionType, limiter_value:float):
        """
        If Source Function is Voltage then Limiter function is Current
        """
        source_map = {
            self.SourceFunctionType.VOLTAGE: 'LMI',
            self.SourceFunctionType.CURRENT: 'LMV'
        }
        self.write(source_map[source_function] + str(limiter_value))
        return


    def operate_output(self):
        self.write('OPR')
        return
    
    def suspend_output(self):
        self.write('SUS')
        return
    
    def standby_output(self):
        self.write('SBY')
        return
    
    class TriggerMode(Enum):
        AUTO = 0
        HOLD = 1
    
    def configure_trigger(self, trigger_mode:TriggerMode):
        trigger_map = {
            self.TriggerMode.AUTO:  'M0',
            self.TriggerMode.HOLD:  'M1'
        }
        self.write(trigger_map[trigger_mode])
        return

    class MeasurementType(Enum):
        OFF = 0
        VOLTAGE = 1
        CURRENT = 2
        RESISTANCE = 3
    
    def configure_measurement(self, measurement_type:MeasurementType):
        measurement_map = {
            self.MeasurementType.OFF:       'F0',
            self.MeasurementType.VOLTAGE:   'F1',
            self.MeasurementType.CURRENT:   'F2',
            self.MeasurementType.RESISTANCE:'F3'
        }
        self.write(measurement_map[measurement_type])
        return
