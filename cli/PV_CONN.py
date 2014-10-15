
import sys
sys.path.insert(0, './')
import epics
import time
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

    # increase the values only stepwise 0.1
#    def put(self, new_v,  *args, **kwargs):
#        v = self.value
#        diff = new_v-v
#        if diff<0: step=-0.1
#        elif diff>0: step=0.1
#        else: return 0
#
#        #print 'curr value',v
#        #print 'new value',new_v
#        #print 'diff',diff
#
#        while abs(diff)>=0.1:
#            v+=step
#            ret = super(PV_CONN, self).put(v,*args, **kwargs)
#            diff = v-new_v
#            time.sleep(0.05)
#            #print v
#
#        if diff==0: return ret
#
#        return super(PV_CONN, self).put(new_v,*args, **kwargs)




