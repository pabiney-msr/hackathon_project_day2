import serial

# open port /dev/ttyACM0 at 9600 baud, also 8,N,1, (whatever those mean) and no timeout:
ser = serial.Serial('/dev/ttyACM0')  # open serial port
print(ser.name)         # check which port was really used
ser.write(b'hello')     # write a string
ser.close()             # close port
print "got to 1"

# Open named port at "19200,8,N,1", 1s timeout:
# with serial.Serial('/dev/ttyACM0', 19200, timeout=1) as ser:
#     x = ser.read()          # read one byte
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     line = ser.readline()   # read a '\n' terminated line
print "got to 2"

# Open port at "38400,8,E,1", non blocking HW handshaking:
ser = serial.Serial('/dev/ttyACM0', 38400, timeout=0,
parity=serial.PARITY_EVEN, rtscts=1)
s = ser.read(100)       # read up to one hundred bytes
                         # or as much is in the buffer
print "got to 3"

# Get a Serial instance and configure/open it later:
ser = serial.Serial()
ser.baudrate = 19200
ser.port = '/dev/ttyACM0'
ser
ser.open()
#ser.is_open
ser.close()
#ser.is_open

print "got to 4"
