# AndoLabInstruments

A collection of Python libraries for experimental instrument control used at the Ando Lab, Department of Applied Physics and Physico-Informatics, Keio University.
Based on [PyMeasure](https://pymeasure.readthedocs.io/), this package adds lab-specific instruments.

## 🛠 Requirements
* **OS:** Windows 10/11 (Recommended)
* **Python:** 3.8 or higher
* **Backend:** NI-VISA (or PyVISA-py)

### Required Libraries
* `numpy`, `pandas`
* `pyvisa`
* `pymeasure`

## 🚀 Installation

Install the latest version.

```bash
pip install https://github.com/Ando-Lab-APPI-Keio/AndoLabInstruments.git
```

## 💻 Usage
### Basic Instrument Connection
```
from AndoLabInstruments.keithley2182 import Keithley2182

if __name__ == "__main__":
    keithley2182 = Keithley2182('GPIB0::5::INSTR')
    keithley2182.initialize()
    keithley2182.configure_analog_filter(Keithley2182.Channel.VOLTAGE_CHANNEL_1, False)
    keithley2182.configure_measurement(Keithley2182.Channel.VOLTAGE_CHANNEL_1, 1, Keithley2182.RateUnit.LINE_CYCLES, 1)
    keithley2182.initiate_measurement(Keithley2182.InitiateType.IMMIDIATE)
    print(keithley2182.fetch())
```


## 📂 Directory Structure
```text
AndoLabInstruments/
├── setup.py
├── README.md
├── requirements.txt
└── andolab_instruments/       <-- Main Package Folder
    ├── __init__.py
    ├── ZNB20.py
    ├── adcmt6240.py
    ├── agilentn5171b.py
    ├── ... (other drivers)
```

## 👤 Author
* [Naoki Yano / Ando lab](https://github.com/naoki-cpp)
