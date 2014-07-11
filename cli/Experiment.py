


import sys
sys.path.insert(0, './')
from epics_device import PowerSupply
from physics_device import Magnet
import json
from time import sleep

relee = None
ps = []         # alias for powersupply
powersupply = ps
magn = []

data_conf = None
def load_data_conf():
    global data_conf
    with open('config.json', 'rb') as fp:
        data_conf = json.load(fp)

    #data_conf = json.load(fp)

def init_devices():
    global relee
    relee = PowerSupply('zpslan01-GetVoltage','zpslan01-SetVoltage',
                        'zpslan01-GetAmpere','zpslan01-SetAmpere')
    global ps
    ps.append(None) # avoid 0 index
    ps.append(relee)# 1
    ps.append(None) # 2
    ps.append(None) # 3
    ps.append(None) # 4
    ps.append(None) # 5
    ps.append(None) # 6
    ps.append(None) # 7
    ps.append(PowerSupply('zpslan08-GetVoltage','zpslan08-SetVoltage','zpslan08-GetAmpere','zpslan08-SetAmpere'))
    ps.append(None) # 9
    ps.append(None) # 10

    ''' initialize powersupplies  '''
    global data_conf
    if data_conf==None:
        load_data_conf()

    ps_conf = data_conf['powersupplies']
    for i in range(len(ps)):
        if ps[i] == None:
            continue
        ps[i].putVolt(ps_conf['ps%d'%i])
        print 'init ps%d'%i


    global magn
    magn.append(None) # avoid 0 index
    magn.append(Magnet(ps[8]))# 1
    magn.append(None) # 2
    magn.append(None) # 3
    magn.append(None) # 4
    magn.append(None) # 5
    magn.append(None) # 6
    magn.append(None) # 7


def demag():
    relee_val = 24
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

    ''' do demag in steps '''
    steps = 10
    for count in range(1,steps):
        if count%2 > 0:
            relee.setterVolt.put(relee_val)
        else:
            relee.setterVolt.put(0)

        for i in range(2,len(ps)):
            if ps[i] == None:
                continue
            volts = ps_heightV[i]-count*ps_heightV[i]/steps
            ps[i].putVolt(volts)
            print '%d %f (ps:%d %f)' %(count,volts,i,ps_heightV[i])
        sleep(1)


    ''' set all ps to 0 '''
    for i in range(2,len(ps)):
        if ps[i] == None:
            continue
        volts = 0
        ps[i].putVolt(volts)
        print '%d %f (ps:%d %f)' %(count,volts,i,ps_heightV[i])

    ''' set relee to 0 '''
    relee.putVolt(0)

def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed! %s %0.3f' %(pvname, value)

if __name__ == "__main__":
    print 'Initializing Devices'
    load_data_conf()
    init_devices()

    #ps[8].setterVolt.add_callback(onChanges)
    #relee.setterVolt.add_callback(onChanges)

