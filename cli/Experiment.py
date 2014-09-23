


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
ps1 = None
ps2 = None
ps3 = None
ps4 = None
ps5 = None
ps6 = None
ps7 = None
ps8 = None
ps9 = None
ps10 = None

t1 = PV_CONN('SHICANE:M1:T', auto_monitor=True )
t2 = PV_CONN('SHICANE:M2:T', auto_monitor=True )
t3 = PV_CONN('SHICANE:M3:T', auto_monitor=True )
t4 = PV_CONN('SHICANE:M4:T', auto_monitor=True )
t5 = PV_CONN('SHICANE:M5:T', auto_monitor=True )
t6 = PV_CONN('SHICANE:M6:T', auto_monitor=True )
t7 = PV_CONN('SHICANE:M7:T', auto_monitor=True )

ps1 = relee = PowerSupply('zpslan01-GetVoltage','zpslan01-SetVoltage',
                        'zpslan01-GetAmpere','zpslan01-SetAmpere')
ps8 = PowerSupply('zpslan08-GetVoltage','zpslan08-SetVoltage','zpslan08-GetAmpere','zpslan08-SetAmpere')

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
        ps[i].putVolt(ps_conf['ps%d'%i])
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
    ps_heightV.append(ps1.getterVolt.get())# 1
    ps_heightV.append(None) # 2
    ps_heightV.append(None) # 3
    ps_heightV.append(None) # 4
    ps_heightV.append(None) # 5
    ps_heightV.append(None) # 6
    ps_heightV.append(None) # 7
    ps_heightV.append(ps8.getterVolt.get())
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


log_pvs = None

def log_records():

    records = ['zpslan01-GetVoltage','zpslan08-GetVoltage']
    global log_pvs
    log_pvs = [PV(records[0], auto_monitor=True ),
           PV(records[1], auto_monitor=True )]

    for i in range(0,len(log_pvs)):
        log_pvs[i].add_callback(log_on_change)

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
    powersupply.setterVolt.add_callback(onChanges)
    powersupply.setterAmp.add_callback(onChanges)

def help():
    print '''
------------------------------------------------
    help()          print this info
    init_devices()  initializes the devices with standard values from the config.json file
    ps1 - ps10      global objects to the PowerSupply class. Methods:
                        getVolt(), putVolt(),
                        getAmpere(), putAmpere()
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

