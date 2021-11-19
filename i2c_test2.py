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


  OldMin = 500
  OldMax = 3500
  NewMin = 0
  NewMax = 180

  if (4097 > dataOut[1] > 3499) and (0 < dataOut[2] < 550):
        OldValue = dataOut[2]
        #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        
        #angleX = NewValue
        print("1")
        angleX = -90 + ((dataOut[2]) / 520) * 90
        #angleX = ((dataOut[2] - 3500) / 500) * 180
  if (520 > dataOut[1] > 0) and (0 < dataOut[2] < 550):
        angleX = ((dataOut[1]) / 520) * 90
        print("2")
  
  if (520 > dataOut[1] > 0) and (3500 < dataOut[2] < 4000):
        angleX = 180 - ((dataOut[1]) / 520) * 90
        print("3")

  if (4000 > dataOut[1] > 3500) and (3500 < dataOut[2] < 4000):
        angleX = -90 -(((dataOut[1])-3500) / 520) * 90
        print("YES")

  else:
        OldValue = dataOut[2]
        NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        #angleX = NewValue + 270
        

  print(dataOut)
  print(angleX)

