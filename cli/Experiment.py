
from epics_device import PowerSupply
import json
from time import sleep

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

    ''' initialize powersupplies  '''
    with open('config.json', 'rb') as fp:
        data_conf = json.load(fp)
        ps_conf = data_conf['powersupplies']
        for i in range(len(ps)):
            if ps[i] == None:
                continue
            ps[i].setterVolt.put(ps_conf['ps%d'%i])
            ps[i].getterVolt.put(ps_conf['ps%d'%i])
            print 'init ps%d'%i


def demag():
    relee_val = 10
    ps_heightV = []
    ps_heightV.append(None) # avoid 0 index
    ps_heightV.append(ps[1].getterVolt.get())# 1
    ps_heightV.append(None) # 2
    ps_heightV.append(None) # 3
    ps_heightV.append(None) # 4
    ps_heightV.append(None) # 5
    ps_heightV.append(None) # 6
    ps_heightV.append(None) # 7
    ps_heightV.append(ps[8].getterVolt.get())
    ps_heightV.append(None) # 9
    ps_heightV.append(None) # 10

    print 'starting to demagnetize'

    for count in range(2,10):
        if count%2 > 0:
            relee.setterVolt.put(relee_val)
        else:
            relee.setterVolt.put(0)

        for i in range(2,len(ps)):
            if ps[i] == None:
                continue
            volts = float(ps_heightV[i]/count)
            ps[i].setterVolt.put(volts)
            print '%d %f (ps:%d %f)' %(count,volts,i,ps_heightV[i])
        sleep(0.2)


def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed! ', pvname, char_value

if __name__ == "__main__":
    print 'Initializing Devices'
    init_devices()

    ps[8].setterVolt.add_callback(onChanges)
    relee.setterVolt.add_callback(onChanges)

