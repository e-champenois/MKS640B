# MKS640B Interface:

Control a MKS640B Pressure Controller using an Arduino and Serial interface, with an additional Python API as well as a PyQT-based GUI.

# Hardware:

1) MKS640B Pressure Controller: https://www.mksinst.com/f/640b-absolute-pressure-controller
2) Arduino UNO Board: https://www.digikey.com/products/en?keywords=1050-1024-ND
3) Dual polarity 15V DC Power Supply: https://www.digikey.com/products/en?keywords=1866-1827-ND
4) I2C/DAC MCP4725 chip: https://www.digikey.com/products/en?keywords=BOB-12918
5) Various wiring...

# Connections:
Note: there may have been small last minute changes in the pin definitions in MKS640.ino...

I. Power Supply DIN5:
1: Common GND
2: Common GND
3: unwired
    4: Common -15V
    5: Common +15V

II. MKS640B DB15:
    1: Arduino D10
    2: Arduino A1
    3: Arduino D8
    4: Arduino D9
    5: Common GND
    6: Common -15V
    7: Common +15V
    8: I2C OUT
    9: unwired
    10: unwired
    11: Common GND
    12: Common GND
    13: Arduino D11
    14: Arduino D12
    15: Common GND

III. I2C chip:
    OUT: DB15 Pin 8
    GND: Common GND
    SCL: Arduino A5
    SDA: Arduino A4
    VCC: Common +5V
    GND: Common GND

IV. Arduino:
    Vin: Common +15V
    GND: Common GND
    A1: DB15 Pin 2
    A4: I2C SDA
    A5: I2C SCL
    D8: DB15 Pin 3
    D9: DB15 Pin 4
    D10: DB15 Pin 1
    D11: DB15 Pin 13
    D12: DB15 Pin 14
    rest: unwired
