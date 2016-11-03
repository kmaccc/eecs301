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
	setMotorTargetSpeed(2,target_speed)
	setMotorTargetSpeed(3,target_speed)
	setMotorTargetSpeed(4,target_speed)
	setMotorTargetSpeed(5,target_speed)

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group H Control Node...")

    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    
    # target_val = getMotorPositionCommand(1)
    target_val = 512
    inc = True
    left = True
    right = False
    
    # resetting motor positions before starting movement
    setMotorTargetPositionCommand(7,590)
    setMotorTargetPositionCommand(6,440)
    setMotorTargetPositionCommand(2,370)
    setMotorTargetPositionCommand(3,650)
    setMotorTargetPositionCommand(4,333)
    setMotorTargetPositionCommand(5,663)
    setMotorTargetPositionCommand(1,512)
  
    for i in range(30):
		r.sleep()
    while not rospy.is_shutdown():

        # call function to get sensor value
        port = 1
        sensor_reading = getSensorValue(port)
        # rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
        
        motor_id = 1
        
        # sitting fawn
        if sensor_reading > 250:
    		setMotorTargetSpeed(7,100)
    		setMotorTargetPositionCommand(7,900)
    		setMotorTargetSpeed(6,100)
    		setMotorTargetPositionCommand(6,120)
    		if left:
    			setMotorTargetPositionCommand(2,570)
    			setMotorTargetPositionCommand(3,650)
    		if right:
        		setMotorTargetPositionCommand(2,370)
    			setMotorTargetPositionCommand(3,450)
    		setMotorTargetPositionCommand(4,333)
    		setMotorTargetPositionCommand(5,663)
    	
        	setMotorTargetSpeed(1,50)
        
        	if not(getIsMotorMovingCommand(1)):
    			if inc:
					target_val = 700
					inc = False
					setMotorTargetPositionCommand(3,450)
    			else:
					target_val = 300
					inc = True	
					setMotorTargetPositionCommand(3,450)
			
    		response = setMotorTargetPositionCommand(motor_id, target_val)
    	
    	# walking fawn
        if sensor_reading < 200:

            setMotorTargetPositionCommand(1,getMotorPositionCommand(motor_id))
            setAllFrontMotorTargetSpeeds(100)
            setMotorTargetSpeed(6,150)
            setMotorTargetSpeed(7,150)

            check = getIsMotorMovingCommand(6)
			
            if left and not check:
                setMotorTargetPositionCommand(2,370)
                setMotorTargetPositionCommand(3,500)
                setMotorTargetPositionCommand(5,500)
                setMotorTargetPositionCommand(4,200)
                setMotorTargetPositionCommand(6,515)
                setMotorTargetPositionCommand(7,665)
                right = True
                left = False
            elif right and not check:
                setMotorTargetPositionCommand(2,520)
                setMotorTargetPositionCommand(3,650)
                setMotorTargetPositionCommand(4,500)
                setMotorTargetPositionCommand(5,800)
                setMotorTargetPositionCommand(6,365)
                setMotorTargetPositionCommand(7,515)
                left = True
                right = False
    	
        rospy.loginfo("Motor 1 position: %i", getMotorPositionCommand(1))
        rospy.loginfo("Motor 2 position: %i", getMotorPositionCommand(2))
        rospy.loginfo("Motor 3 position: %i", getMotorPositionCommand(3))
        rospy.loginfo("Motor 4 position: %i", getMotorPositionCommand(4))
        rospy.loginfo("Motor 5 position: %i", getMotorPositionCommand(5))
        rospy.loginfo("Motor 6 position: %i", getMotorPositionCommand(6))
        rospy.loginfo("Motor 7 position: %i", getMotorPositionCommand(7))

        # sleep to enforce loop rate
        r.sleep()
