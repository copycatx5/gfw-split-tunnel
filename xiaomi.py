__author__ = 'copycat'



class filter:

    file = 'delegated-apnic-20141208'
    gateway = 'OLDGW'
    DEV = 'DEV'
    output = 'vpnup.sh'

    def load(self):
        fp = open(self.file,'r')
        fo = open(self.output, 'w')
        c=0
	#print 'route delete %s' % self.gateway
	fo.write( """#!/bin/sh
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

OLDGW=`ip route show | grep '^default' | grep 'dev pppoe-wan' | sed -e 's/default via \([^ ]*\).*/\\1/' | head -1`
#OLDGW='192.168.1
if [ $OLDGW == '' ]; then
    exit 0
fi

DEV='pppoe-wan'
""")
        for line in fp:
            #(x,country,type,ip,mask,x,x)
            list = line.split('|')
            if len(list) == 7:
                if list[1] == 'CN' and list[2]=='ipv4':
                    mask = self.con( list[4])
                    out =  'ip route add to %s/%s via $%s dev $%s table vpn\n' % (list[3], mask, self.gateway, self.DEV)
                    fo.write(out)
                    c+=1
        print 'total= %d' % c
	fo.write('route add to 69.167.138.0/24 via $OLDGW dev $DEV table vpn\n')
        fo.close()
        fp.close()


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
