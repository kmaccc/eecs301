#!/usr/bin/env python
import roslib
import rospy
from map import *
# from map2 import *
from fw_wrapper.srv import *
import signal
import sys
import time
import Queue
import pickle

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
        
# start positions
def startPosition():
    setMotorTargetPositionCommand(1,512)
    setMotorTargetPositionCommand(2,347)
    setMotorTargetPositionCommand(3,679)
    setMotorTargetPositionCommand(4,311)
    setMotorTargetPositionCommand(5,723)

def turningRight(direction):
    direction = 1
    # n_time = time.time() + 0.95
    cur_time = (time.time() - init_time)/500
    print cur_time
    n_time = time.time() + 0.93 + cur_time * 0.001
    prev_time = time.time()
    total_turn = 0
    while time.time() < n_time:# and total_turn < 90:
        diff = time.time() - prev_time
        prev_time = time.time()

        gyro = getSensorValue(1)
        if gyro < 1040:
            gdiff = 1050 - gyro

            # print "diff: ",diff
            # print "gyro diff: ",gdiff

            total_turn += (gdiff*diff)
        # print "total turn: ",total_turn

        # rospy.loginfo("Gyro: %i\n",getSensorValue(1))
        # rospy.loginfo(getSensorValue(5))
        setMotorWheelSpeed(7,552)
        setMotorWheelSpeed(6,552)

    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0) 

    return total_turn

def turningLeft(direction):
    direction = -1
    # n_time = time.time() + 0.95
    cur_time = (time.time() - init_time)/500
    print cur_time
    n_time = time.time() + 0.93 + cur_time * 0.001
    prev_time = time.time()
    total_turn = 0
    while time.time() < n_time:# and total_turn < 90:
        diff = time.time() - prev_time
        prev_time = time.time()

        gyro = getSensorValue(1)
        if gyro > 1060:
            gdiff = gyro - 1050

            # print "diff: ",diff
            # print "gyro diff: ",gdiff

            total_turn += (gdiff*diff)
        # print "total turn: ",total_turn

        # rospy.loginfo("Gyro: %i\n",getSensorValue(1))
        # rospy.loginfo(getSensorValue(5))
        setMotorWheelSpeed(7,1576)
        setMotorWheelSpeed(6,1576)

    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0) 

    return total_turn

def turningAround():
    cur_time = (time.time() - init_time)/500
    setMotorTargetSpeed(6,1676)
    setMotorTargetSpeed(7,1676)

    time.sleep(1.4 + 0.001*cur_time)

    setMotorTargetSpeed(6,0)
    setMotorTargetSpeed(7,0)    

    # move backwards to the center of the tile
    setMotorTargetSpeed(6,910)
    setMotorTargetSpeed(7,1900)    

    time.sleep(0.3)

    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0)    

def shutdown(sig, stackframe):
    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0)
    sys.exit(0)

def stopmap(sig, stackframe):
    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0)

    choice = input("What would you like to do?  1 to map, 2 to plan, 3 to exit\n")

    if choice == 1:
        restartx = input("What X coordinate are you starting from?\n")
        restarty = input("What Y coordinate are you starting from?\n")
        restarth = input("What heading are you starting from?\n")
        map_func(restartx, restarty, restarth, map0, stack)

    elif choice == 2:
        c = True

        while c:
            # get new planning positions
            startposx = input("What X coordinate do you want to start at? \n")
            startposy = input("What Y coordinate do you want to start at? \n")
            startheading = input("What heading do you want to start at? \n")
            endposx = input("What X coordinate do you want to end at? \n")
            endposy = input("What Y coordinate do you want to end at? \n")
            endheading = input("What heading do you want to end at? \n")
            follow_path(startposx, startposy, startheading, endposx, endposy, endheading, map0)

            c = input("Would you like to enter another path? \n")

    sys.exit(0)

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group H Control Node...")
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTSTP, stopmap)
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    
    # target_val = getMotorPositionCommand(1)
    head = 1
    rightMax = 769
    leftMax = 253
    mid = 512
    gyro = 1
    leftIR_port = 2
    DMS_port = 5
    rightIR_port = 6
    inc = True
    left = True
    right = False
    
    # resetting motor positions before starting movement
    startPosition()

    k = 0    

    # initial = getSensorValue(1)
    
    # if len(sys.argv) > 1 and int(sys.argv[1]) == 3:
    #     rospy.loginfo('Building a map of the world. \n')
    init_time = time.time()

    #     map0 = EECSMap()
    #     map0.clearObstacleMap()
    #     map0.printObstacleMap() # DEBUG

    #     heading = 3

    #     for x in range(8):
    #         for y in range(8):
    #             map0.setCost(x, y, -1)
    
    #     stack = [[0,0]]

    #     map_func(0, 0, heading, map0, stack)

    # else:
    #     map0 = EECSMap()
    #     map0.printObstacleMap()

    # setMotorMode(7,1)
    # setMotorMode(6,1)

    # i = 0
    # j = 0

    # # Localization
    # if len(sys.argv) > 1 and int(sys.argv[1]) == 1:
    #     rospy.loginfo('Walking to destination. \n')
    #     i = int(sys.argv[2])
    #     j = int(sys.argv[3])

    #     rospy.loginfo("i: %i  \n", i)
    #     rospy.loginfo("j: %i  \n", j)

    #     step(i)
    #     if j > 0:
    #         # turningRight()
    #         turningLeft()
    #     step(j)
    
    # # Planning
    # if len(sys.argv) > 1 and int(sys.argv[1]) == 2:
    #     rospy.loginfo('Following path to destination. \n')
    #     si = int(sys.argv[2])
    #     sj = int(sys.argv[3])
    #     h = int(sys.argv[4])
    #     gi = int(sys.argv[5])
    #     gj = int(sys.argv[6])
    #     final_heading = int(sys.argv[7])
   
    #     heading, robot_pos = follow_path(si, sj, h, gi, gj, final_heading, map0)

    #     rospy.loginfo("Final robot position: ")
    #     rospy.loginfo(robot_pos)
    #     rospy.loginfo("Final robot heading: %i\n",heading)

    # trainingFile = open('/home/ros_workspace/src/eecs301_grp_H/src/trainingData.txt', 'r+')
    try:
        data = pickle.load('/home/ros_workspace/src/eecs301_grp_H/src/trainingData.pkl')
        print data
        print "Data successfully retrieved"
    except:
        data = []

    # initLeft, initRight, initDMS, LorR, finalLeft, finalRight, finalDMS, gyro
    c = 1
    while (c):
        attributes = [0]*9
        attributes[0] = getSensorValue(leftIR_port)
        attributes[1] = getSensorValue(rightIR_port)
        attributes[2] = getSensorValue(DMS_port)
        direction = 0 # -1 for left turn, 1 for right turn

        gyro = turningLeft(direction)
        # gyro = turningRight(direction)

        attributes[3] = direction
        attributes[4] = getSensorValue(leftIR_port)
        attributes[5] = getSensorValue(rightIR_port)
        attributes[6] = getSensorValue(DMS_port)
        attributes[7] = gyro

        attributes[8] = input("How was that turn?  -2 for very underturned, 0 for correct, 2 for very overturned\n")

        print attributes
        print data + attributes
        data += attributes

        c = input("Would you like to record another turn? 1 to continue\n")

    pickle.dump(data,'/home/ros_workspace/src/eecs301_grp_H/src/trainingData.pkl')

    # trainingFile.close()

    shutdown()


    while not rospy.is_shutdown():

        # turningAround()
        # rospy.loginfo("Gyro: %i\n",getSensorValue(1))
        # startposx = input("What X coordinate do you want to start at? \n")
        # startposy = input("What Y coordinate do you want to start at? \n")
        # startheading = input("What heading do you want to start at? \n")
        # endposx = input("What X coordinate do you want to end at? \n")
        # endposy = input("What Y coordinate do you want to end at? \n")
        # endheading = input("What heading do you want to end at? \n")
        # follow_path(startposx,startposy, startheading, endposx, endposy, endheading, map0)

        # call function to get sensor value
        port = 1
        # sensor_reading = getSensorValue(port)
        # rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
        	
        # leftIR = getSensorValue(leftIR_port)
        # rightIR = getSensorValue(rightIR_port)
        # DMS = getSensorValue(DMS_port)

        # rospy.loginfo("Left IR value: %i  \n", leftIR)
        # rospy.loginfo("Right IR value: %i \n", rightIR)
        # rospy.loginfo("DMS value: %i \n", DMS)

        # rospy.loginfo("Right wheel speed: %i  \n", getMotorWheelSpeed(6))
        # rospy.loginfo("Left wheel speed: %i  \n", getMotorWheelSpeed(7))

        # rospy.loginfo("Motor 1 position: %i", getMotorPositionCommand(1))
        # rospy.loginfo("Motor 2 position: %i", getMotorPositionCommand(2))
        # rospy.loginfo("Motor 3 position: %i", getMotorPositionCommand(3))
        # rospy.loginfo("Motor 4 position: %i", getMotorPositionCommand(4))
        # rospy.loginfo("Motor 5 position: %i", getMotorPositionCommand(5))
        # rospy.loginfo("Motor 6 position: %i", getMotorPositionCommand(6))
        # rospy.loginfo("Motor 7 position: %i", getMotorPositionCommand(7))

        # sleep to enforce loop rate
        r.sleep()
