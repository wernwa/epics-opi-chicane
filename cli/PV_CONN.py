
import sys
sys.path.insert(0, './')
import epics
#from epics_device import PowerSupply
#from physics_device import Magnet
#import json

class PV_CONN(epics.PV):
    def __init__(self, *args, **kwargs):
        super(PV_CONN, self).__init__(*args, **kwargs)
        self.conn=False
        self.connection_callbacks.append(self.onConnectionChange)

    def onConnectionChange(self, pvname=None, conn= None, **kws):
        #sys.stdout.write('PV connection status changed: %s %s\n' % (pvname,  repr(conn)))
        #sys.stdout.flush()
        self.conn=conn

    def get(self, *args, **kwargs):
        if self.conn==True:
            return super(PV_CONN, self).get(*args, **kwargs)
        else:
            return None




