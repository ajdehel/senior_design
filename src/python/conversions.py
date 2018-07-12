"""
Conversion functions specific to sensors used by plumbintelligent

Sensors used:
* internal pressure
* external pressure (via conductive fabric)
* vibration

"""
def to_internal_pressure(voltage):
    """"""
    pressure = 1.2 * (((voltage / 1024) * 4) - 0.5) / 4
    return pressure
