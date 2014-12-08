__author__ = 'copycat'



class filter:

    file = 'delegated-apnic-20140601.txt'
    gateway = '192.168.31.1'
    output = 'setroute.bat'

    def load(self):
        fp = open(self.file,'r')
        fo = open(self.output, 'w')
        c=0
	#print 'route delete %s' % self.gateway
        for line in fp:
            #(x,country,type,ip,mask,x,x)
            list = line.split('|')
            if len(list) == 7:
                if list[1] == 'CN' and list[2]=='ipv4':
                    mask = self.convert( list[4])
                    out =  'route add %s mask %s %s\r\n' % (list[3], mask, self.gateway)
                    fo.write(out)
                    c+=1
        print 'total= %d' % c
        fo.close()
        fp.close()


    def convert(self, mask):
        mask = int(mask) -1
        d4 = (~ mask & 0xff)
        d3 = (~ mask >> 8  & 0xff)
        d2 = (~ mask >> 16 & 0xff)
        d1 = (~ mask >> 32 & 0xff)
        return "%s.%s.%s.%s" % (d1,d2,d3,d4)



f = filter()
#print f.convert(32768)
f.load()
