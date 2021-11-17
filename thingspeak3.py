
import time
import serial
import re
import urllib2

def average(givenList):
    print(givenList)
    try:
        theAverage = sum(givenList)/len(givenList)
    except:
        print("No data to make average from!")
        theAverage = 0
    return str(theAverage)

# setup serial communication
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1 )
ser.flushInput()

# declare global variables
counter = 0
Temperature1 = []
Temperature2 = []
Light1 = []
Light2 = []
Accel1 = []
Accel2 = []
Accel3 = []
ParkingSensor = []
faults = 0

# prepare API codes
url1 = 'https://api.thingspeak.com/update?api_key=Q6TAHYAPF8ARTD30'
url2 = 'https://api.thingspeak.com/update?api_key=BUUBCPHRY1132YBZ'
url3 = 'https://api.thingspeak.com/update?api_key=OCKVD5GUF2IUZJGV'
url4 = 'https://api.thingspeak.com/update?api_key=IEU5M69Q0EP9YKUH'

while 1:
    time.sleep(.25)
    data_string = ser.readline() # read data from the serial port
    # filter data from the printed string
    data_num = re.findall('\d+(?:\.\d+)?', data_string)
    print(data_num)

    # does the line contain all required data
    try:
        data_num[5]
    except:
        print("Data has bad format, ignoring")
        continue

    #  if CRC isn't correct or if data is not from our group, ignore completely
    try:
        if data_num[5] == "0":
            print("CRC invalid")
            faults += 1 #keep note on the amount of faults encountered
            continue
    except:
        print("Couldn't find CRC! Is the Serial Connected?")
        continue

    if data_num[0] != "14":
        print("GID invalid")
        continue



    # assign which node is the data from
    NID = data_num[1]
    if NID == "1": # Node one takes comparator light value and temperature of t$
        Temperature1.append(float(data_num[2]))
        Light1.append(float(data_num[3]))
    elif NID == "2": # Node two takes in the temperature outside and the surrou$
        Temperature2.append(float(data_num[2]))
        Light2.append(float(data_num[3]))
    elif NID == "3": # Node three takes in the data from the accelerometer
        Accel1.append(float(data_num[2]))
        Accel2.append(float(data_num[3]))
        Accel3.append(float(data_num[4]))
    elif NID == "4": # Node four takes the data from parking sensors
        ParkingSensor.append(float(data_num[2]))
    counter += 1 # keep note of the amount of taken samples


    if counter >= 60: # once there is enough data captured
        print("Uploading..")
        upload1 = urllib2.urlopen(
                url1+'&field1=0'+average(Temperature1)+"&field2=0"+average(Light1))
        upload1.read()
        upload1.close()
        upload1 = urllib2.urlopen(
                url2+'&field1=0'+average(Temperature2)+"&field2=0"+average(Light2))
        upload1.read()
        upload1.close()
        upload1 = urllib2.urlopen(
            url3+'&field1=0'+average(Accel1)+"&field2=0"+average(Accel2)+"&field3=0"+average(Accel3))
        upload1.read()
        upload1.close()
        upload1 = urllib2.urlopen(
            url4+'&field1=0'+average(ParkingSensor))
        upload1.read()
        upload1.close()
        print("Uploaded!")
        
        print("RS232 Packages lost = " +  str(faults))
        print("RS232 Package loss = %0.2f" % (counter/faults))
        

        #clean all buffers
        counter = 0
        Temperature1 = []
        Temperature2 = []
        Light1 = []
        Light2 = []
        Accel1 = []
        Accel2 = []
        Accel3 = []
        ParkingSensor = []
        #clean the RS232 pipe, this leads to loss of data
        ser.flushInput()
