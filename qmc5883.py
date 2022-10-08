import time
class QMC5883:
    def __init__(self,i2c,irq=False,slvAddr=0x0D,autoScale=True):
        self.i2c=i2c
        self.slvAddr=slvAddr
        self.autoScale=autoScale#True: read status-OVL every measurement, change range when need, False:use 8Gauss range only
        time.sleep_us(400)
        self.i2c_writereg(0x0A,b'\x80')#software reset
        self.i2c_writereg(0x0B,b'\x01')#SET/RESET Period Register, recommanded value
        if(irq):
            self.i2c_writereg(0x0A,b'\x40')#40: enable pointer roll over and interrupt 41:enable pointer roll over
        else:
            self.i2c_writereg(0x0A,b'\x41')
        """if(irq):
            self.ctrlR2=b'\x40'
        else:
            self.ctrlR2=b'\x41'"""
        if(not self.autoScale):
            self.i2c_writereg(0x09,b'\x19')#OSR=00(00:512 01:256),range=00(00:2Gauss/01:8Gauss),ODR=10(10:100Hz 11:200Hz),MODE=01(start continuous measure)
        else:
            self.i2c_writereg(0x09,b'\x09')
        #wait data ready
        self.status=self.i2c_readregs(0x06,1)#byte, &0x01:data ready, &0x02:over range, &0x04:data skipped
        i=0
        while(self.status[0]&0x01==0x00):
            i+=5
            time.sleep_ms(5)
            self.status=self.i2c_readregs(0x06,1)
            print("Mag:delayed %d ms befor data ready"%(i))
            
    def i2c_readregs(self,regAddr,bytenum):#int,int,int
        self.i2c.writeto(self.slvAddr,bytes([regAddr]))
        return self.i2c.readfrom(self.slvAddr,bytenum)

    def i2c_writereg(self,regAddr,buff):#int,int,bytes
        self.i2c.writeto(self.slvAddr,bytes([regAddr])+buff)
    
    def measure(self):
        xyz=[0,0,0]
        mag=bytearray(6)
        if(not self.autoScale):#8gauss range, doesn't consider over range situation
            mag=self.i2c_readregs(0x00,6)
        else:
            self.status=self.i2c_readregs(0x06,1)
            if(self.status[0]&0x02==0x00):#not over range
                mag=self.i2c_readregs(0x00,6)
            else:
                self.i2c_writereg(0x09,b'\x19')#8Gauss range
                #skip a measurement
                i=0
                while(self.status[0]&0x01==0x00):#data not ready
                    i+=1
                    time.sleep_ms(1)
                    self.status=self.i2c_readregs(0x06,1)
                    print("Mag:skip data!delayed %d ms waitting next data..."%(i))
                mag=self.i2c_readregs(0x00,6)
                self.i2c_writereg(0x09,b'\x09')#back to 2Gauss range
        x=mag[0]+(mag[1]<<8)
        xyz[0]=x if (x&0x8000==0) else x-65536#complementry to ordinary,65536=2**16
        y=mag[2]+(mag[3]<<8)
        xyz[1]=y if (y&0x8000==0) else y-65536
        z=mag[4]+(mag[5]<<8)
        xyz[2]=z if (z&0x8000==0) else z-65536
        return xyz
