from machine import Pin, I2C
import time
from qmc5883 import QMC5883

i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=400_000)
mag=QMC5883(i2c)
a=[]
while(True):
    time.sleep_ms(100)
    a=mag.measure()
    print("magnet on x-axis:%05d, y-axis:\t %05d, z-axis:\t %05d"%(a[0],a[1],a[2]))