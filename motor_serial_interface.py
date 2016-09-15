import serial

def send_serial(ser, msg):
	#send srial output and return status bool
	
	return false


def read_serial(ser):
	#read serial input and return value
	return false

def loop():
	#set up serial
	ser = serial.Serial('/dev/ttyACM0')
	#input loop

	

	#close serial
	ser.close()



if __name__ == '__main__':
	loop()