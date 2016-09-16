#!/usr/bin/env python

# ROS imports:
import rospy
#from std_msgs.msg import Int16
from geometry_msgs.msg import Point

# Python imports:
import serial
import sys



def callback(pt_msg, ser):
    rospy.loginfo(pt_msg)
    pos_mot_0 = int(pt_msg.x)
    pos_mot_1 = int(pt_msg.y)
    send_serial(ser, chr(0x00) + chr(pos_mot_0))
    send_serial(ser, chr(0x01) + chr(pos_mot_1))


def send_serial(ser, msg):
    #send serial output and return status bool
    clear_byte = 0xFF # clear byte, do not change

    #package command bytes into string for sending
    command_string = bytes(chr(clear_byte) + msg)

    #write returns the number of bytes written, if that is less than or equal to zero we failed so return false
    return ser.write(command_string) > 0


def conrol_loop():
    #set up serial
    ser = serial.Serial('/dev/ttyACM0')
    if not ser.isOpen():
        print "some horrible warning"
        sys.exit(42)

    rospy.init_node('motor_control_node', anonymous=False)
    rospy.Subscriber('motor_commands', Point, callback, ser)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        conrol_loop()
    except rospy.ROSInterruptException:
        if ser.isOpen():
            ser.close()
        sys.exit(99)
        pass
