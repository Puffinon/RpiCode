import smbus
import time
from time import sleep

# initiate bus object from SMBus
bus=smbus.SMBus(1)

#switch from sleep mode to normal mode ACC_CONFIG0
bus.write_byte_data(0x15,0x019,0x02)

#wait for the sensor to start up
time.sleep(1.5)

dataOut = [0,0,0]
while 1:  
  time.sleep(0.1)
  # read the data from the gyro
  dataIn=bus.read_i2c_block_data(0x15,0x04,6)

  
  dataOut[0] = dataIn[0] + (dataIn[1]*256)
  dataOut[1] = dataIn[2] + (dataIn[3]*256)
  dataOut[2] = dataIn[4] + (dataIn[5]*256)

  for i in range(3):
        dataOut[i] = (dataOut[i])
        dataOut[i] = round(dataOut[i])


if dataOut[1] > 3500 and dataOut[2] < 500:
      angleX = (dataOut[1] / 500) * 180
else:
      angleX = -(dataOut[1] / 500) * 180

print(dataOut)
print(angleX)

