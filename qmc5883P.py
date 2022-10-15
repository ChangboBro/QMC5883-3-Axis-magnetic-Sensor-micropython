import time
class QMC5883:
    def __init__(self,i2c,slvAddr=0x2C):
        self.i2c=i2c
        self.slvAddr=slvAddr
        #self.autoScale=autoScale#True: read status-OVL every measurement, change range when need, False:use 8Gauss range only
        time.sleep_us(400)
        self.i2c_writereg(0x0B,b'\x80')#software reset
        self.i2c_writereg(0x29,b'\x06')#define the sign for syz axis
        self.range=3#3:2gauss,2:8gauss,1:12gauss,0:30gauss
        self.i2c_writereg(0x0B,bytes([self.range<<2]))
        self.i2c_writereg(0x0A,b'\xC9')#C:8*8over sample, 9:(100Hz ,normal)/D(200Hz,normal)
        #find suitable range
        self.status=b'\x02'
        while(self.status[0]&0x02!=0x00):
            #self.status=self.i2c_readregs(0x09,1)
            self.waitDRDY()
            self.rangeSel()
            
            
    def i2c_readregs(self,regAddr,bytenum):#int,int,int
        self.i2c.writeto(self.slvAddr,bytes([regAddr]))
        return self.i2c.readfrom(self.slvAddr,bytenum)

    def i2c_writereg(self,regAddr,buff):#int,int,bytes
        self.i2c.writeto(self.slvAddr,bytes([regAddr])+buff)
    
    def rangeSel(self):
        self.status=self.i2c_readregs(0x09,1)
        if(self.status[0]&0x02!=0x00):
            print("data over range!")
            if(self.range==0):
                print("env mag field stronger than 30gauss!")
                return 0
            else:
                self.range-=1
                self.i2c_writereg(0x0B,bytes([self.range<<2]))
        else:
            print("now range grade is:%d"%self.range)
            return 0
        
    def waitDRDY(self):
        i=0
        while(self.status[0]&0x01==0x00):
            i+=5
            time.sleep_ms(5)
            self.status=self.i2c_readregs(0x09,1)
            print("Mag:delayed %d ms befor data ready"%(i))
        return 0
    
    def measure(self):
        xyz=[0,0,0]
        mag=bytearray(6)
        mag=self.i2c_readregs(0x01,6)
        x=mag[0]+(mag[1]<<8)
        xyz[0]=x if (x&0x8000==0) else x-65536#complementry to ordinary,65536=2**16
        y=mag[2]+(mag[3]<<8)
        xyz[1]=y if (y&0x8000==0) else y-65536
        z=mag[4]+(mag[5]<<8)
        xyz[2]=z if (z&0x8000==0) else z-65536
        return xyz

