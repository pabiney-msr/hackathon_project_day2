import serial
import sys

def send_serial(ser, msg):
	#send serial output and return status bool
	clear_byte = 0xFF		# clear byte, do not change
	channel_byte = 0x00		# device's channel number
	command_byte = 0x7A		# servo position controlled with this

	#package command bytes into string for sending
	command_string = bytes(chr(clear_byte) + chr(channel_byte) + chr(command_byte))
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
	if msg.count <= 0:
		return False
	if msg[0] == 'X' or  msg[0] == 'x':
		return False
	else:
		return send_serial(ser, msg[0])
	return False

def loop():
	#set up serial
	ser = serial.Serial('/dev/ttyACM0')
	if not ser.isOpen():
		print "some horrible warning"
		sys.exit(42)
	#input loop
	send_serial(ser, "nothing here yet, replace later")
	while handle_input(ser, gather_input()):
		pass
	#close serial
	ser.close()

if __name__ == '__main__':
	loop()
