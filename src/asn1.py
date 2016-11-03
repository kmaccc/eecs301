#!/usr/bin/env python
import roslib
import rospy
from fw_wrapper.srv import *

# -----------SERVICE DEFINITION-----------
# allcmd REQUEST DATA
# ---------
# string command_type
# int8 device_id
# int16 target_val
# int8 n_dev
# int8[] dev_ids
# int16[] target_vals

# allcmd RESPONSE DATA
# ---------
# int16 val
# --------END SERVICE DEFINITION----------

# ----------COMMAND TYPE LIST-------------
# GetMotorTargetPosition
# GetMotorCurrentPosition
# GetIsMotorMoving
# GetSensorValue
# GetMotorWheelSpeed
# SetMotorTargetPosition
# SetMotorTargetSpeed
# SetMotorTargetPositionsSync
# SetMotorMode
# SetMotorWheelSpeed

# wrapper function to call service to set a motor mode
# 0 = set target positions, 1 = set wheel moving
def setMotorMode(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
    	resp1 = send_command('SetMotorMode', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get motor wheel speed
def getMotorWheelSpeed(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetMotorWheelSpeed', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor wheel speed
def setMotorWheelSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorWheelSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set motor target speed
def setMotorTargetSpeed(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('SetMotorTargetSpeed', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get sensor value
def getSensorValue(port):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetSensorValue', port, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set a motor target position
def setMotorTargetPositionCommand(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
		send_command = rospy.ServiceProxy('allcmd', allcmd)
		resp1 = send_command('SetMotorTargetPosition', motor_id, target_val, 0, [0], [0])
		return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get a motor's current position
def getMotorPositionCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
		send_command = rospy.ServiceProxy('allcmd', allcmd)
		resp1 = send_command('GetMotorCurrentPosition', motor_id, 0, 0, [0], [0])
		return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to check if a motor is currently moving
def getIsMotorMovingCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
		send_command = rospy.ServiceProxy('allcmd', allcmd)
		resp1 = send_command('GetIsMotorMoving', motor_id, 0, 0, [0], [0])
		return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        
# wrapper function to set all motor speeds
def setAllFrontMotorTargetSpeeds(target_speed):
    rospy.wait_for_service('allcmd')
    setMotorTargetSpeed(2,target_speed)
    setMotorTargetSpeed(3,target_speed)
    setMotorTargetSpeed(4,target_speed)
    setMotorTargetSpeed(5,target_speed)

# start positions
def startPosition():
    setMotorTargetPositionCommand(1,512)
    setMotorTargetPositionCommand(2,370)
    setMotorTargetPositionCommand(3,650)
    setMotorTargetPositionCommand(4,333)
    setMotorTargetPositionCommand(5,663)
    setMotorTargetPositionCommand(6,440)
    setMotorTargetPositionCommand(7,590)

# wrapper function to set left side position when walking straight
def leftWalk():
    setMotorTargetPositionCommand(2,370)
    setMotorTargetPositionCommand(3,500)
    setMotorTargetPositionCommand(5,500)
    setMotorTargetPositionCommand(4,200)
    setMotorTargetPositionCommand(6,515)
    setMotorTargetPositionCommand(7,665)

# wrapper function to set right side position when walking straight
def rightWalk():
    setMotorTargetPositionCommand(2,520)
    setMotorTargetPositionCommand(3,650)
    setMotorTargetPositionCommand(4,500)
    setMotorTargetPositionCommand(5,800)
    setMotorTargetPositionCommand(6,365)
    setMotorTargetPositionCommand(7,515)

# wrapper function to set left side position when turning left
def rightTurn():
    setMotorTargetPositionCommand(2,340)
    setMotorTargetPositionCommand(3,500)
    setMotorTargetPositionCommand(4,200)
    setMotorTargetPositionCommand(5,500)
    setMotorTargetPositionCommand(6,530)
    setMotorTargetPositionCommand(7,500)

def rightTurnL():   
    setMotorTargetPositionCommand(2,370)
    setMotorTargetPositionCommand(3,650)
    setMotorTargetPositionCommand(4,333)
    setMotorTargetPositionCommand(5,663)
    setMotorTargetPositionCommand(6,440)
    setMotorTargetPositionCommand(7,590)

# wrapper function to set right side position when turning left
def leftTurn():
    setMotorTargetPositionCommand(2,520)
    setMotorTargetPositionCommand(3,680)
    setMotorTargetPositionCommand(4,500)
    setMotorTargetPositionCommand(5,820)
    setMotorTargetPositionCommand(6,540)
    setMotorTargetPositionCommand(7,490)

def leftTurnR():
    setMotorTargetPositionCommand(2,370)
    setMotorTargetPositionCommand(3,650)
    setMotorTargetPositionCommand(4,333)
    setMotorTargetPositionCommand(5,663)
    setMotorTargetPositionCommand(6,440)
    setMotorTargetPositionCommand(7,590)

def turningLeft(left, right):
    setAllFrontMotorTargetSpeeds(300)
    setMotorTargetSpeed(6,150)
    setMotorTargetSpeed(7,150)

    k = 0

    while k < 20:

        #check = getIsMotorMovingCommand(2) | getIsMotorMovingCommand(3) | getIsMotorMovingCommand(4) | getIsMotorMovingCommand(5) | getIsMotorMovingCommand(6) | getIsMotorMovingCommand(7)
        check = getIsMotorMovingCommand(2)
        if left and not check:
            leftTurn()
            right = True
            left = False
            k += 1
        elif right and not check:
            leftTurnR()
            left = True
            right = False
            k += 1
# single turn to the left
def small_left():
    setAllFrontMotorTargetSpeeds(300)
    setMotorTargetSpeed(6,150)
    setMotorTargetSpeed(7,150)

    for x in range(2):
        leftTurn()
        leftTurnR()

    rospy.loginfo("Turned left. \n")

def turningRight(left, right):
    setAllFrontMotorTargetSpeeds(300)
    setMotorTargetSpeed(6,150)
    setMotorTargetSpeed(7,150)

    k = 0

    while k < 20:

        check = getIsMotorMovingCommand(2)

        if left and not check:
            rightTurn()
            right = True
            left = False
            k += 1
        elif right and not check:
            rightTurnL()
            left = True
            right = False
            k += 1

# single turn to the right
def small_right():
    setAllFrontMotorTargetSpeeds(300)
    setMotorTargetSpeed(6,150)
    setMotorTargetSpeed(7,150)

    for x in range(2):
        rightTurn()
        rightTurnL()

    rospy.loginfo("Turned right. \n")

def turningAround(left, right):
    setAllFrontMotorTargetSpeeds(300)
    setMotorTargetSpeed(6,150)
    setMotorTargetSpeed(7,150)

    k = 0

    while k < 2:
        turningLeft(left, right)
        k += 1

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group H Control Node...")

    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    
    # target_val = getMotorPositionCommand(1)
    head = 1
    rightMax = 769
    leftMax = 253
    mid = 512
    rightIR_port = 1
    leftIR_port = 2
    DMS_port = 5
    inc = True
    left = True
    right = False
    
    # resetting motor positions before starting movement
    # startPosition()

    # for i in range(30):
		# r.sleep()

    k = 0

    initial = getSensorValue(1)
    turningAround(left,right)
    

    while not rospy.is_shutdown():

        # call function to get sensor value
        port = 1
        # sensor_reading = getSensorValue(port)
        # rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
        
        motor_id = 1
    	
    	# walking straight

        motor_pos = getMotorPositionCommand(1)
        # rospy.loginfo(motor_pos)

        setAllFrontMotorTargetSpeeds(200)
        setMotorTargetSpeed(6,150)
        setMotorTargetSpeed(7,150)

        # check = getIsMotorMovingCommand(6)
        setMotorTargetPositionCommand(1,512)

        leftIR = getSensorValue(leftIR_port)
        rightIR = getSensorValue(rightIR_port)
        DMS = getSensorValue(DMS_port)

        rospy.loginfo("Left IR value: %i  \n", leftIR)
        rospy.loginfo("Right IR value: %i \n", rightIR)
        rospy.loginfo("DMS value: %i \n", DMS)

        #walking straight
        if left: #and not check:
            leftWalk()
            right = True
            left = False
        elif right: #and not check:
            rightWalk()
            left = True
            right = False

        # when nothing is blocking the front sensor
        if DMS < 1340:
        # right side of robot is too close
            if rightIR > 140:
                startPosition()
                rospy.loginfo("Too close to right wall. Turning left. \n")
                small_left()
        # right side of robot is too far
            elif rightIR < 80 and rightIR > 5:
                startPosition()
                rospy.loginfo("Too far away from right wall. Turning right. \n")
                small_right()
        # left side of robot is too close
            if leftIR > 115:
                startPosition()
                rospy.loginfo("Too close to left wall. Turning right. \n")
                small_right()
        # left side of robot is too far
            elif leftIR < 50 and leftIR > 5:
                startPosition()
                rospy.loginfo("Too far away from left wall. Turning left. \n")
                small_left()
        # something is blocking the front sensor
        elif DMS > 1360:
        # Right and left sensors are also blocked. Turning around
            if leftIR > 75 and rightIR > 110:
                rospy.loginfo("Blocked in front, left, and right. Turning around. \n")
                turningAround(left, right)
        # Only left sensor is blocked. Turning right.
            elif leftIR > 75:
                rospy.loginfo("Blocked in front and left. Turning right. \n")
                turningRight(left, right)
            else:
        # Only right sensor is blocked. Turning left.
                rospy.loginfo("Blocked in front and right. Turning left. \n")
                turningLeft(left, right)

        # turning left
        # turningLeft(left, right)
        # rospy.loginfo("Turned left. \n")
        # turning right
        # turningRight(left, right)
        # rospy.loginfo("Turned right. \n")
        # turning around
        # turningAround(left, right)
        # rospy.loginfo("Turning around. \n")
    	
        # rospy.loginfo("Motor 1 position: %i", getMotorPositionCommand(1))
        # rospy.loginfo("Motor 2 position: %i", getMotorPositionCommand(2))
        # rospy.loginfo("Motor 3 position: %i", getMotorPositionCommand(3))
        # rospy.loginfo("Motor 4 position: %i", getMotorPositionCommand(4))
        # rospy.loginfo("Motor 5 position: %i", getMotorPositionCommand(5))
        # rospy.loginfo("Motor 6 position: %i", getMotorPositionCommand(6))
        # rospy.loginfo("Motor 7 position: %i", getMotorPositionCommand(7))

        # sleep to enforce loop rate
        r.sleep()
