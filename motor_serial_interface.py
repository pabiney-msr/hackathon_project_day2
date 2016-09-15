import serial
import sys

try:
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def send_serial(ser, msg):
	#send serial output and return status bool
	clear_byte = 0xFF		# clear byte, do not change
	#package command bytes into string for sending
	command_string = bytes(chr(clear_byte) + msg)
	#write returns the number of bytes written, if that is lessthan or equal to zero we failed so return false
	return ser.write(command_string) > 0

def read_serial(ser):
	#read serial input and return value
	return False

def gather_input():
	#return input
	#msg = raw_input()
	msg = getch()
	return msg

def handle_input(ser, msg, pos_mot_0, pos_mot_1):
	#ony check first char, bay life

	return_bool = False
	motor_Zero = True
	ord_msg = ord(msg)
	if msg.count <= 0:
		return False, pos_mot_0, pos_mot_1
	if msg[0] == 'x' or  msg[0] == 'X':
		return False, pos_mot_0, pos_mot_1
	elif msg[0] == 'w'or msg[0] == 'W' or ord_msg == 65:
		#move up
		pos_mot_1 -= 0x19
		motor_Zero = False
	elif msg[0] == 's'or msg[0] == 'S' or ord_msg == 66:
		#move down
		pos_mot_1 += 0x19
		motor_Zero = False
	elif msg[0] == 'a'or msg[0] == 'A' or ord_msg == 68:
		#move left
		pos_mot_0 += 0x19
		motor_Zero = True
	elif msg[0] == 'd'or msg[0] == 'D' or ord_msg == 67:
		#move right
		pos_mot_0 -= 0x19
		motor_Zero = True
	else:
		return_bool = False
	pos_mot_0 = 0 if (pos_mot_0 <= 1) else (pos_mot_0 if (pos_mot_0 < 254) else 254)
	pos_mot_1 = 0 if (pos_mot_1 <= 1) else (pos_mot_1 if (pos_mot_1 < 254) else 254)
	return_bool = send_serial(ser, chr(0x00)+ chr(pos_mot_0) if motor_Zero else chr(0x01)+ chr(pos_mot_1))
	return return_bool, pos_mot_0, pos_mot_1

def loop():
	#set up serial
	ser = serial.Serial('/dev/ttyACM0')
	if not ser.isOpen():
		print "some horrible warning"
		sys.exit(42)
	#init to default pos
	#channel_byte = 0x00		 device's channel number
	#command_byte = 0x7A		 servo position controlled with this
	pos_mot_0 = 0x7A
	pos_mot_1 = 0x7A
	send_serial(ser, chr(0x00) + chr(pos_mot_0))
	send_serial(ser, chr(0x01) + chr(pos_mot_1))
	val = True
	#input loop
	while val:
		msg = gather_input()
		val, pos_mot_0, pos_mot_1 = handle_input(ser, msg, pos_mot_0, pos_mot_1)

	#close serial
	ser.close()

if __name__ == '__main__':
	loop()
