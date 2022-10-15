# QMC5883-3-Axis-magnetic-Sensor-micropython
A simple micropython library (class) to drive QMC5883 (a 3-Axis magnetic Sensor or digital compass), interrut (optional), automatically chosing measurement range for good resolution(optional).

the output is a list [x,y,z] of the intensity of magnetic field in 3 axises.

There are 2 types of QMC5883, which is the QMC5883L and QMC5883P, they have different register map, QMC5883P can measure up to 30 gauss field intensity, QMC5883L can only up to 8 Gauss, but seems to have higher resolution? (maybe is just a bug in my QMC5883P code... if you find that, please pull a issue)
