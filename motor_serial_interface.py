import serial

def send_serial(ser, msg):
	#send serial output and return status bool
	clear_byte = 0x00		# clear byte, do not change
	device_byte = 0x00		# device number
	command_byte = 0x04		# MSB cleared command byte, do not change
	data_byte_1 = 0x00		# channel number
	data_byte_2 = 0x70		# target low bits
	data_byte_3 = 0x2E		# target high bits
	#package command bytes into string for sending
	command_string = bytes(chr(clear_byte) + chr(device_byte) + chr(command_byte) + chr(data_byte_1) + chr(data_byte_2) + chr(data_byte_3))
	#write returns the number of bytes written, if that is lessthan or equal to zero we failed so return false
	return ser.write(command_string) > 0

def read_serial(ser):
	#read serial input and return value
	return False

def gather_input():
	#return input
	msg = raw_input()
	return msg

def handle_input(ser, msg):
	#ony check first char, bay life
	if msg.count <= 0
		return False
	if msg[0] == 'X' or  msg[0] == 'x':
		return False
	else
		return send_serial(ser, msg[0])
	return False

def loop():
	#set up serial
	ser = serial.Serial('/dev/ttyACM0')
	#input loop
	send_serial(ser, "nothing here yet, replace later")
	while handle_input(ser, gather_input()):
		pass
	#close serial
	ser.close()

if __name__ == '__main__':
	loop()