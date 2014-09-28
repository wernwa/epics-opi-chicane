


import sys
sys.path.insert(0, './')
from epics import PV
from epics_device import PowerSupply
from physics_device import Magnet
from PV_CONN import PV_CONN
import json
from time import sleep
from time import strftime

relee = None
ps1 = relee = PowerSupply('shicane:zps:relee:volt','shicane:zps:relee:curr')
ps2 =  PowerSupply('shicane:zps:2:volt','shicane:zps:2:curr')
ps3 =  PowerSupply('shicane:zps:3:volt','shicane:zps:3:curr')
ps4 =  PowerSupply('shicane:zps:4:volt','shicane:zps:4:curr')
ps5 =  PowerSupply('shicane:zps:5:volt','shicane:zps:5:curr')
ps6 =  PowerSupply('shicane:zps:6:volt','shicane:zps:6:curr')
ps7 =  PowerSupply('shicane:zps:7:volt','shicane:zps:7:curr')
ps8 =  PowerSupply('shicane:zps:8:volt','shicane:zps:8:curr')
ps9 =  PowerSupply('shicane:zps:9:volt','shicane:zps:9:curr')
ps10 = PowerSupply('shicane:zps:10:volt','shicane:zps:10:curr')

t1 = PV_CONN('shicane:q1:temp', auto_monitor=True )
t2 = PV_CONN('shicane:q2:temp', auto_monitor=True )
t3 = PV_CONN('shicane:q3:temp', auto_monitor=True )
t4 = PV_CONN('shicane:q4:temp', auto_monitor=True )
t5 = PV_CONN('shicane:q5:temp', auto_monitor=True )
t6 = PV_CONN('shicane:q6:temp', auto_monitor=True )
t7 = PV_CONN('shicane:q7:temp', auto_monitor=True )


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
    global ps, relee, ps1, ps2, ps3, ps4, ps5, ps6, ps7, ps8, ps9, ps10

    if (len(ps)==0):
        ps.append(None) # avoid 0 index
        ps.append(relee)# 1
        ps.append(None) # 2
        ps.append(None) # 3
        ps.append(None) # 4
        ps.append(None) # 5
        ps.append(None) # 6
        ps.append(None) # 7
        ps.append(ps8)
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
        ps[i].setVolt(ps_conf['ps%d'%i])
        print 'init ps%d'%i


    global magn
    if (len(magn)==0):
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
    ps_heightV.append(ps1.Volt.get())# 1
    ps_heightV.append(None) # 2
    ps_heightV.append(None) # 3
    ps_heightV.append(None) # 4
    ps_heightV.append(None) # 5
    ps_heightV.append(None) # 6
    ps_heightV.append(None) # 7
    ps_heightV.append(ps8.Volt.get())
    ps_heightV.append(None) # 9
    ps_heightV.append(None) # 10

    print 'starting to demagnetize'

    ''' do demag in steps '''
    steps = 10
    for count in range(1,steps):
        if count%2 > 0:
            relee.Volt.put(relee_val)
        else:
            relee.Volt.put(0)

        for i in range(2,len(ps)):
            if ps[i] == None:
                continue
            volts = ps_heightV[i]-count*ps_heightV[i]/steps
            ps[i].setVolt(volts)
            print '%d %f (ps:%d %f)' %(count,volts,i,ps_heightV[i])
        sleep(1)


    ''' set all ps to 0 '''
    for i in range(2,len(ps)):
        if ps[i] == None:
            continue
        volts = 0
        ps[i].setVolt(volts)
        print '%d %f (ps:%d %f)' %(count,volts,i,ps_heightV[i])

    ''' set relee to 0 '''
    relee.setVolt(0)


log_pvs = None


def log_on_change(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed! %s %0.3f' %(pvname, value)
    fo = open("log.txt", "a")
    string = '%s' %strftime("%Y-%m-%H:%M:%S_%s")
    for i in range(0,len(log_pvs)):
        string += ' %s' %log_pvs[i].get()
    string += '\n';
    fo.write(string)
    fo.close()


def onChanges(pvname=None, value=None, char_value=None, **kw):
    print 'PV Changed! %s %0.3f' %(pvname, value)

write = sys.stdout.write
def onConnectionChange(pvname=None, conn= None, **kws):
    write('PV connection status changed: %s %s\n' % (pvname,  repr(conn)))
    sys.stdout.flush()

def monitor_temp(t):
    t.add_callback(onChanges)

def monitor_ps(powersupply):
    powersupply.Volt.add_callback(onChanges)
    powersupply.Curr.add_callback(onChanges)

def help():
    print '''
------------------------------------------------
    help()          print this info
    init_devices()  initializes the devices with standard values from the config.json file
    ps1 - ps10      global objects to the PowerSupply class. Methods:
                        getVolt(), setVolt(),
                        getCurr(), setCurr()
                    ps1 - ps10 are initialized after calling init_devices()
    demag()         demagnetezising all Magnets at once
    monitor_ps(ps)  Print ampare and volt changes of the given powersupply
    monitor_temp(t) Print temperature changes of the given temp-sensor
------------------------------------------------
    '''


if __name__ == "__main__":
    print 'Initializing Devices'
    load_data_conf()
    help()
    #init_devices()

    #ps[8].setterVolt.add_callback(onChanges)
    #relee.setterVolt.add_callback(onChanges)

