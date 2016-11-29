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
import math
import operator
import random

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

def turningRight():
    direction = 'R'
    # n_time = time.time() + 0.95
    cur_time = (time.time() - init_time)/500
    # print cur_time
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

    return total_turn, direction

def turningLeft():
    direction = 'L'
    # n_time = time.time() + 0.95
    cur_time = (time.time() - init_time)/500
    # print cur_time
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

    return total_turn, direction

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

# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group H Control Node...")
    signal.signal(signal.SIGINT, shutdown)
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

    # Number of nearest neighbors
    if len(sys.argv) > 1:
        k = int(sys.argv[1])
    else:
        k = 3

    # initial = getSensorValue(1)
    
    init_time = time.time()

    # Train
    if len(sys.argv) > 1 and int(sys.argv[2]) == 1:
        trainingFile = open('/home/rosuser/ros_workspace/src/eecs301_grp_H/src/trainingData.txt', 'ab')
        # try:
        #     #data = pickle.load('/home/ros_workspace/src/eecs301_grp_H/src/trainingData.pkl')
        #     data = pickle.load(trainingFile)
        #     print data
        #    print "Data successfully retrieved"
        #except:
        data = []

        # initLeft, initRight, initDMS, LorR, finalLeft, finalRight, finalDMS, gyro
        c = 1
        while (c):
            attributes = [0]*9
            attributes[0] = getSensorValue(leftIR_port)
            attributes[1] = getSensorValue(rightIR_port)
            attributes[2] = getSensorValue(DMS_port)

            gyro, direction = turningLeft()
            # gyro, direction = turningRight()

            attributes[3] = direction
            attributes[4] = getSensorValue(leftIR_port)
            attributes[5] = getSensorValue(rightIR_port)
            attributes[6] = getSensorValue(DMS_port)
            attributes[7] = gyro

            attributes[8] = input("How was that turn?  -2 for very underturned, 0 for correct, 2 for very overturned\n")

            print attributes
            data.append(attributes)
            trainingFile.write(str(attributes) + '; \n')
            c = input("Would you like to record another turn? 1 to continue\n")

        #pickle.dump(data,'/home/ros_workspace/src/eecs301_grp_H/src/trainingData.pkl')
        #pickle.dump(data,trainingFile)
        trainingFile.close()

        #shutdown()

    # Test
    if len(sys.argv) > 1 and int(sys.argv[2]) == 2:
        # train = open('/home/rosuser/ros_workspace/src/eecs301_grp_H/src/train.txt')
        # test = open('/home/rosuser/ros_workspace/src/eecs301_grp_H/src/test.txt')
        orig_data = open('/home/rosuser/ros_workspace/src/eecs301_grp_H/src/trainingData_withDiff.csv')

        data = [0]*10
        get_data = []
        # test_data = []
        data[0] = []
        data[1] = []
        data[2] = []
        data[3] = []
        data[4] = []
        data[5] = []
        data[6] = []
        data[7] = []
        data[8] = []
        data[9] = []

        for line in orig_data:
            splitstring = line.split(',')
            for i in range(len(splitstring)):
                splitstring[i] = float(splitstring[i])
            get_data.append(splitstring)

        random.shuffle(get_data)
        data[0] = get_data[:10]
        data[1] = get_data[10:20]
        data[2] = get_data[20:30]
        data[3] = get_data[30:40]
        data[4] = get_data[40:50]
        data[5] = get_data[50:60]
        data[6] = get_data[60:70]
        data[7] = get_data[70:80]
        data[8] = get_data[80:90]
        data[9] = get_data[90:]

        # print train_data

        # for line in test:
        #     splitstring = line.split(',')
        #     for i in range(len(splitstring)):
        #         splitstring[i] = float(splitstring[i])
        #     test_data.append(splitstring)

        # print test_data

        avg_err = 0
        for x in range(10):
            test_set = []
            train_set = []
            test_set = data[x]
            for j in range(10):
                if j != x:
                    train_set += data[j]

            # print train_set[0]
            # print '\n\n\n'
            # print test_set[0]

            labels = []
            for test_pt in test_set:
                dist_vec = []
                for train_pt in train_set:
                    err = 0
                    for i in range(len(train_pt)-1):
                        err += (test_pt[i] - train_pt[i])**2
                    dist_vec.append((train_pt,math.sqrt(err)))
                dist_vec.sort(key=operator.itemgetter(1))
                
                top_neighbors = []
                for x in range(k):
                    top_neighbors.append(dist_vec[x][0])

                potential_label = {-2:0, -1:0, 0:0, 1:0, 2:0}

                # labelSum = 0
                for x in top_neighbors:
                    # labelSum += x[-1]
                    potential_label[x[-1]] += 1
                # print potential_label

                labels.append(max(potential_label.iteritems(), key=operator.itemgetter(1))[0])
                # labels.append(round(labelSum/k)) 

            print labels

            correct = 0
            i = 0
            for test_pt in test_set:
                if test_pt[-1] == labels[i]:
                    correct += 1
                i += 1

            print (correct/float(len(test_set)))*100.0
            avg_err += (correct/float(len(test_set)))*100.0

        print avg_err/10

    # Demo
    if len(sys.argv) > 1 and int(sys.argv[2]) == 3:
        train = open('/home/rosuser/ros_workspace/src/eecs301_grp_H/src/trainingData.csv')

        train_data = []

        for line in train:
            splitstring = line.split(',')
            for i in range(len(splitstring)):
                splitstring[i] = float(splitstring[i])
            train_data.append(splitstring)

        attributes = [0]*8
        attributes[0] = getSensorValue(leftIR_port)
        attributes[1] = getSensorValue(rightIR_port)
        attributes[2] = getSensorValue(DMS_port)

        if len(sys.argv) > 2 and sys.argv[3] == 'L':
            gyro, direction = turningLeft()
        else:
            gyro, direction = turningRight()

        if direction == 'L':
            attributes[3] = -100
        else:
            attributes[3] = 100
        attributes[4] = getSensorValue(leftIR_port)
        attributes[5] = getSensorValue(rightIR_port)
        attributes[6] = getSensorValue(DMS_port)
        attributes[7] = gyro

        test_pt = attributes

        dist_vec = []
        for train_pt in train_data:
            err = 0
            for i in range(len(train_pt)-1):
                err += (test_pt[i] - train_pt[i])**2
            dist_vec.append((train_pt,math.sqrt(err)))
        dist_vec.sort(key=operator.itemgetter(1))
        
        top_neighbors = []
        for x in range(k):
            top_neighbors.append(dist_vec[x][0])

        potential_label = {-2:0, -1:0, 0:0, 1:0, 2:0}

        # labelSum = 0
        for x in top_neighbors:
            # labelSum += x[-1]
            potential_label[x[-1]] += 1
        print potential_label

        print max(potential_label.iteritems(), key=operator.itemgetter(1))[0]

        # print round(labelSum/k)


    while not rospy.is_shutdown():

         # call function to get sensor value
        port = 1
        # sensor_reading = getSensorValue(port)
        # rospy.loginfo("Sensor value at port %d: %f", port, sensor_reading)
        	
        # sleep to enforce loop rate
        r.sleep()
