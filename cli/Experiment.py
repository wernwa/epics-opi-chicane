
from epics_device import PowerSupply


relee = None
ps = []         # alias for powersupply
powersupply = ps

def init_devices():
    global relee
    relee = PowerSupply('zpslan01-GetVoltage','zpslan01-SetVoltage',
                        'zpslan01-GetAmpare','zpslan01-SetAmpare')
    global ps
    ps.append(None) # avoid 0 index
    ps.append(relee)# 1
    ps.append(None) # 2
    ps.append(None) # 3
    ps.append(None) # 4
    ps.append(None) # 5
    ps.append(None) # 6
    ps.append(None) # 7
    ps.append(PowerSupply('zpslan08-GetVoltage','zpslan08-SetVoltage','zpslan08-GetAmpare','zpslan08-SetAmpare'))
    ps.append(None) # 9
    ps.append(None) # 10


def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed! ', pvname, char_value

if __name__ == "__main__":
    print 'Initializing Devices'
    init_devices()

    relee.getterVolt.add_callback(onChanges)

