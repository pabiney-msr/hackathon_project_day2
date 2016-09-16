#!/usr/bin/env python

# ROS imports:
import rospy
from std_msgs.msg import String

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
        return pos_mot_0, pos_mot_1

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

    # clip motor positions and within boundaries if necessary
    pos_mot_0 = 1 if (pos_mot_0 <= 1) else (pos_mot_0 if (pos_mot_0 < 254) else 254)
    pos_mot_1 = 1 if (pos_mot_1 <= 1) else (pos_mot_1 if (pos_mot_1 < 254) else 254

    return pos_mot_0, pos_mot_1


def input_loop():
    pub = rospy.Publisher('motor_commands', String, queue_size=10)
    rospy.init_node('user_input_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    pos_mot_0 = 0x7A
    pos_mot_1 = 0x7A
    while not rospy.is_shutdown():

        msg = getch()
        pos_mot_0, pos_mot_1 = handle_input(msg, pos_mot_0, pos_mot_1)

        rospy.loginfo(pos_mot_0)
        pub.publish(pos_mot_0)
        rospy.loginfo(pos_mot_1)
        pub.publish(pos_mot_1)

        rate.sleep()


if __name__ == '__main__':
    try:
        input_loop()
    except rospy.ROSInterruptException:
        sys.exit(99)
        pass
