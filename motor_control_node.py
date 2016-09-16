#!/usr/bin/env python

# ROS imports:
import rospy
from std_msgs.msg import String

# Python imports:
import serial
import sys



def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def send_serial(ser, msg):
    #send serial output and return status bool
    clear_byte = 0xFF # clear byte, do not change

    #package command bytes into string for sending
    command_string = bytes(chr(clear_byte) + msg)

    #write returns the number of bytes written, if that is less than or equal to zero we failed so return false
    return ser.write(command_string) > 0


def conrol_loop():
    rospy.init_node('motor_control_node', anonymous=True)
    rospy.Subscriber('motor_commands', String, callback)
    #set up serial
    ser = serial.Serial('/dev/ttyACM0')
    if not ser.isOpen():
        print "some horrible warning"
        sys.exit(42)
    # NEED TO IMPORT FROM TOPIC pos_mot_0
    # NEED TO IMPORT FROM TOPIC pos_mot_1
    send_serial(ser, chr(0x00) + chr(pos_mot_0))
    send_serial(ser, chr(0x01) + chr(pos_mot_1))

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



# TODO:
# need to import pos_mot_0 and pos_mot_1 from ROS topic
#



if __name__ == '__main__':
    try:
        conrol_loop()
    except rospy.ROSInterruptException:
        if ser.isOpen():
            ser.close()
        sys.exit(99)
        pass
