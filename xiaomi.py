__author__ = 'copycat.liuATgmail.com'



class filter:

    file = 'delegated-apnic-20150129'
    gateway = 'OLDGW'
    DEV = 'DEV'
    up = 'vpnup.sh'
    down = 'vpndown.sh'
    extraList = [ '69.167.138.0' ] #appannie

    def load(self):
        fp = open(self.file,'r')
        self.foUp = open(self.up, 'w')
        self.foDown = open(self.down, 'w')

        c=0
	#print 'route delete %s' % self.gateway
	self.foUp.write( """#!/bin/sh
# Tested on: XiaoMi Router R1D  version:0.9.36 
# SPLIT_T by Copycat Arts.
# Great Knowledge comes great power.

export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

DEV='pppoe-wan'

OLDGW=`ip route show | grep '^default' | grep 'dev pppoe-wan' | sed -e 's/default via \([^ ]*\).*/\\1/' | head -1`
if [ $OLDGW == '' ]; then
    exit 0
fi

""")
        for line in fp:
            #(x,country,type,ip,mask,x,x)
            list = line.split('|')
            if len(list) == 7:
                if list[1] == 'CN' and list[2]=='ipv4':
                    mask = self.con( list[4])
                    self.writeRules(list[3], mask, self.gateway, self.DEV)
                    c+=1
        print 'total= %d' % c
        for ip in self.extraList:
            self.writeRules( ip, '24', self.gateway, self.DEV )
        self.foUp.close()
        self.foDown.close()
        fp.close()


    def writeRules( self, ip, mask, gate, dev):
        out =  'ip route add to %s/%s via $%s dev $%s table vpn\n' % ( ip, mask, gate, dev )
        self.foUp.write(out)
        out =  'ip route del %s/%s table vpn\n' % (ip, mask)
        self.foDown.write(out)

    def convert(self, mask):
        mask = int(mask)-1 
        d4 = (~ mask & 0xff)
        d3 = (~ mask >> 8  & 0xff)
        d2 = (~ mask >> 16 & 0xff)
        d1 = (~ mask >> 32 & 0xff)
        return "%s.%s.%s.%s" % (d1,d2,d3,d4)

    def con(self, mask):
	c=0
	mask= int(mask)-1
	for i in range(0,32):
	    if( mask & 0x1 == 0 ):
		c=c+1
	    mask=mask>>1
	return c
	

f = filter()
#print f.convert(32768)
f.load()
#print f.con(4096)
