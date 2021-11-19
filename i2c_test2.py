import smbus
import time
from time import sleep

# initiate bus object from SMBus
bus=smbus.SMBus(1)

#switch from sleep mode to normal mode ACC_CONFIG0
bus.write_byte_data(0x15,0x019,0x02)

#wait for the sensor to start up
time.sleep(1.5)

data1 = [0,0,0]
while 1:  
  time.sleep(0.1)
  # read the data from the gyro
  data=bus.read_i2c_block_data(0x15,0x04,6)

  
  data1[0] = data[0] + (data[1]*256)
  data1[1] = data[2] + (data[3]*256)
  data1[2] = data[4] + (data[5]*256)

  for xyz in data:
        xyz = (xyz / 4096.0) * 180

  print(data1)

