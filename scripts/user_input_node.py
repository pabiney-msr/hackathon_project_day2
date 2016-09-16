#!/usr/bin/env python

# ROS imports:
import rospy
from std_msgs.msg import Int16

# Python imports:
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


def handle_input(msg, pos_mot_0, pos_mot_1):
    #only check first char, bay life
    motor_Zero = False
    ord_msg = ord(msg)

    if msg.count <= 0:
        return False, pos_mot_0, pos_mot_1

    if msg[0] == 'x' or  msg[0] == 'X':
        return True, pos_mot_0, pos_mot_1

    if msg[0] == 'w' or msg[0] == 'W' or ord_msg == 65:
        pos_mot_1 -= 0x19 # move up
        motor_Zero = False
    elif msg[0] == 's' or msg[0] == 'S' or ord_msg == 66:
        pos_mot_1 += 0x19 # move down
        motor_Zero = False
    elif msg[0] == 'a' or msg[0] == 'A' or ord_msg == 68:
        pos_mot_0 += 0x19 # move left
        motor_Zero = True
    elif msg[0] == 'd' or msg[0] == 'D' or ord_msg == 67:
        pos_mot_0 -= 0x19 # move right
        motor_Zero = True
    else:
        print "User input did not produce valid motor command"

    # # clip motor positions and within boundaries if necessary
    if pos_mot_0 < 1:
        pos_mot_0 = 1
    if pos_mot_0 > 254:
        pos_mot_0 = 254
    if pos_mot_1 < 1:
        pos_mot_1 = 1
    if pos_mot_1 > 254:
        pos_mot_1 = 254

    return False, pos_mot_0, pos_mot_1


def input_loop():
    rospy.init_node('user_input_node', anonymous=False)
    pub = rospy.Publisher('motor_commands', Int16, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    pos_mot_0 = 0x7A
    pos_mot_1 = 0x7A
    while not rospy.is_shutdown():

        msg = getch()
        error, pos_mot_0, pos_mot_1 = handle_input(msg, pos_mot_0, pos_mot_1)
        #handle_input(msg, pos_mot_0, pos_mot_1)

        rospy.loginfo(pos_mot_0)
        pub.publish(pos_mot_0)
        rospy.loginfo(pos_mot_1)
        pub.publish(pos_mot_1)

        rate.sleep()

        if error:
            break


if __name__ == '__main__':
    try:
        input_loop()
    except rospy.ROSInterruptException:
        sys.exit(99)
        pass
