import smbus
import time
import math
from time import sleep

# initiate bus object from SMBus
bus=smbus.SMBus(1)

#switch from sleep mode to normal mode ACC_CONFIG0
bus.write_byte_data(0x15,0x019,0x02)

#wait for the sensor to start up
time.sleep(1.5)

angleX = 0
angleY = 0
dataOut = [0,0,0]
while 1:  
  time.sleep(0.1)
  # read the data from the gyro
  dataIn=bus.read_i2c_block_data(0x15,0x04,6)

  
  dataOut[0] = dataIn[0] + (dataIn[1]*256)
  dataOut[1] = dataIn[2] + (dataIn[3]*256)
  dataOut[2] = dataIn[4] + (dataIn[5]*256)

  for i in range(3):
        dataOut[i] = (dataOut[i])/22.755
        dataOut[i] = round(dataOut[i])

  print(dataOut)




  #print(round(angleX))
  #print(round(angleY))

"""
  
  x_Buff = dataOut[0]
  y_Buff = dataOut[1]
  z_Buff = dataOut[2]

  angleX = math.atan2(y_Buff , z_Buff) * 57.3;
  angleY = math.atan2((- x_Buff) , math.sqrt(y_Buff * y_Buff + z_Buff * z_Buff)) * 57.3;
  

  if (Bval > dataOut[1] > Cval) and (0 < dataOut[2] < Aval):
        OldValue = dataOut[2]
        #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        
        #angleX = NewValue
        
        angleX = -90 + ((dataOut[2]) / Aval) * 90
        #angleX = ((dataOut[2] - 3500) / 500) * 180
  if (Aval > dataOut[1] > 0) and (0 < dataOut[2] < Aval):
        angleX = ((dataOut[1]) / Aval) * 90
        
  if (Aval > dataOut[1] > 0) and (Cval < dataOut[2] < Bval):
        angleX = 180 - ((dataOut[1]) / Aval) * 90
        
  if (Bval > dataOut[1] > Cval) and (Cval < dataOut[2] < Bval):
        angleX = -90 -(((dataOut[1])-Cval) / Aval) * 90
        


  if (Cval < dataOut[0] < Bval) and (0 < dataOut[2] < Aval):
        angleY = 90-((dataOut[2]) / Aval) * 90
        print("1")

  else:
        OldValue = dataOut[2]
        NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        #angleX = NewValue + 270
        
"""
