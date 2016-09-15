import serial



def send_serial(ser, msg):
	#send serial output and return status bool
	clear_byte = 0x00		# clear byte
	device_byte = 0x00		# device number
	command_byte = 0x04		# MSB cleared command byte
	data_byte_1 = 0x00		# command byte
	data_byte_2 = 0x70		# command byte
	data_byte_3 = 0x2E		# command byte

	command_string = bytes(chr(clear_byte) + chr(device_byte) + chr(command_byte) + chr(data_byte_1) + chr(data_byte_2) + chr(data_byte_3))

	ser.write(command_string)

	return False


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

	return False



if __name__ == '__main__':
	loop()
