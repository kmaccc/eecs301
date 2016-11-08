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

# wrapper function to set left side position when walking straight
def walk():
    setMotorWheelSpeed(6,1475)
    setMotorWheelSpeed(7,530)

# wrapper function for taking num steps forward, with wall following corrections
def step(num = 1):
    k = 0
    while k < num:
        if num == 1:
            n_time = time.time() + 1.9
        else:
            n_time = time.time() + 1.85
        while time.time() < n_time:
            # rospy.loginfo(getSensorValue(5))
            setMotorWheelSpeed(7,910)
            setMotorWheelSpeed(6,1900)
            if getSensorValue(5) > 1700: # DMS too close
                break
            if (getSensorValue(6) > 200 and getSensorValue(2) < 170) or (getSensorValue(2) < 100 and getSensorValue(2) > 20): # rightIR too close or leftIR too far
                setMotorWheelSpeed(7,420)
                # n_time += 0.0075
            if (getSensorValue(2) > 180 and getSensorValue(6) < 190) or (getSensorValue(1) < 100 and getSensorValue(1) > 20): # leftIR too close or rightIR too far
                setMotorWheelSpeed(6,1250)
                # n_time += 0.0075
        k += 1
    setMotorWheelSpeed(6,0)
    setMotorWheelSpeed(7,0)

def turningRight():
    n_time = time.time() + 0.9
    prev_time = time.time()
    total_turn = 0
    while time.time() < n_time and total_turn < 90:
        diff = time.time() - prev_time
        prev_time = time.time()

        gyro = getSensorValue(1)
        if gyro < 1040:
            gdiff = 0.4*(1050 - gyro)

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

    # setMotorWheelSpeed(6,226)
    # setMotorWheelSpeed(7,226)

    # time.sleep(2.65)

    # setMotorWheelSpeed(6,0)
    # setMotorWheelSpeed(7,0)    

def turningLeft():
    n_time = time.time() + 0.9
    prev_time = time.time()
    total_turn = 0
    while time.time() < n_time and total_turn < 90:
        diff = time.time() - prev_time
        prev_time = time.time()

        gyro = getSensorValue(1)
        if gyro > 1060:
            gdiff = 0.3158*(gyro - 1050)

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

    # rospy.loginfo("Gyro: %i\n",getSensorValue(1))
    # setMotorWheelSpeed(6,1250)
    # setMotorWheelSpeed(7,1250)
    # rospy.loginfo("Gyro: %i\n",getSensorValue(1))

    # time.sleep(2.50)
    # rospy.loginfo("Gyro: %i\n",getSensorValue(1))

    # setMotorWheelSpeed(6,0)
    # setMotorWheelSpeed(7,0)
    # rospy.loginfo("Gyro: %i\n",getSensorValue(1))

    # setMotorWheelSpeed(6,530)
    # setMotorWheelSpeed(7,1475)

    # time.sleep(0.75)

    # setMotorWheelSpeed(6,0)
    # setMotorWheelSpeed(7,0)   

def turningAround():
    setMotorTargetSpeed(6,1676)
    setMotorTargetSpeed(7,1676)

    time.sleep(1.4)

    setMotorTargetSpeed(6,0)
    setMotorTargetSpeed(7,0)    

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

    startposx = input("What X coordinate do you want to start at? \n")
    startposy = input("What Y coordinate do you want to start at? \n")
    startheading = input("What heading do you want to start at? \n")
    endposx = input("What X coordinate do you want to end at? \n")
    endposy = input("What Y coordinate do you want to end at? \n")
    endheading = input("What heading do you want to end at? \n")
    follow_path(startposx,startposy, startheading, endposx, endposy, endheading, map0)

    sys.exit(0)


def follow_path(si, sj, h, gi, gj, final_heading, map0):
    for x in range(8):
            for y in range(8):
                map0.setCost(x, y, 99)

    map0.setCost(gi,gj,0)
    
    q = Queue.Queue()
    q.put([gi, gj, 0])

    while map0.getCost(si,sj) == 99 and not q.empty():
        current_node = q.get()
        for direction in range(1,5):
            # rospy.loginfo('Checking direction %i \n', direction)
            if map0.getNeighborCost(current_node[0], current_node[1], direction) == 99:
                if not map0.getNeighborObstacle(current_node[0], current_node[1], direction):
                    map0.setNeighborCost(current_node[0], current_node[1], direction, current_node[2] + 1)
                    neighbori = current_node[0]
                    neighborj = current_node[1]
                    neighborCost = current_node[2] + 1
                    if direction == 1: #North
                        neighbori -= 1
                    elif direction == 2: #East
                        neighborj += 1
                    elif direction == 3: #South
                        neighbori += 1
                    elif direction == 4: #West
                        neighborj -= 1
                    q.put([neighbori, neighborj, neighborCost])

    path = []
    path.append([si, sj])
    current_cost = map0.getCost(si, sj)
    map0.printCostMap()

    if current_cost != 99:
        while current_cost != 0:
            curr_node = path[-1]
            for direction in range(1,5):
                # rospy.loginfo('Checking path %i \n', direction)
                if not map0.getNeighborObstacle(curr_node[0],curr_node[1], direction):
                    if map0.getNeighborCost(curr_node[0],curr_node[1], direction) < current_cost:
                        neighbori = curr_node[0]
                        neighborj = curr_node[1]
                        if direction == 1: #North
                            neighbori -= 1
                        elif direction == 2: #East
                            neighborj += 1
                        elif direction == 3: #South
                            neighbori += 1
                        elif direction == 4: #West
                            neighborj -= 1
                        path.append([neighbori, neighborj])
                        current_cost = map0.getCost(neighbori, neighborj)
                        break

    print path

    heading = h
    robot_pos = [si, sj]

    path = path[1:]
    while robot_pos != [gi, gj] and len(path) > 0:
        k = 1
        if heading == 3:
            if path[0][0] > robot_pos[0]:
                while len(path) > 1 and path[1][0] > path[0][0]:
                    path = path[1:]
                    k += 1
                step(k)
                heading = 3
                robot_pos[0] += k
                path = path[1:]
            elif path[0][0] < robot_pos[0]:
                turningAround()
                heading = 1
            else:
                if path[0][1] > robot_pos[1]:
                    turningLeft()
                    heading = 2
                elif path[0][1] < robot_pos[1]:
                    turningRight()
                    heading = 4
        elif heading == 4:
            if path[0][0] > robot_pos[0]:
                turningLeft()
                heading = 3
            elif path[0][0] < robot_pos[0]:
                turningRight()
                heading = 1
            else:
                if path[0][1] > robot_pos[1]:
                    turningAround()
                    heading = 2
                elif path[0][1] < robot_pos[1]:
                    while len(path) > 1 and path[1][1] < path[0][1]:
                        path = path[1:]
                        k += 1
                    step(k)
                    heading = 4
                    robot_pos[1] -= k
                    path = path[1:]
        elif heading == 1:
            if path[0][0] > robot_pos[0]:
                turningAround()
                heading = 3
            elif path[0][0] < robot_pos[0]:
                while len(path) > 1 and path[1][0] < path[0][0]:
                        path = path[1:]
                        k += 1
                step(k)
                heading = 1
                robot_pos[0] -= k
                path = path[1:]
            else:
                if path[0][1] > robot_pos[1]:
                    turningRight()
                    heading = 2
                elif path[0][1] < robot_pos[1]:
                    turningLeft()
                    heading = 4
        elif heading == 2:
            if path[0][0] > robot_pos[0]:
                turningRight()
                heading = 3
            elif path[0][0] < robot_pos[0]:
                turningLeft()
                heading = 1
            else:
                if path[0][1] > robot_pos[1]:
                    while len(path) > 1 and path[1][1] > path[0][1]:
                        path = path[1:]
                        k += 1
                    step(k)
                    heading = 2
                    robot_pos[1] += k
                    path = path[1:]
                elif path[0][1] < robot_pos[1]:
                    turningAround()
                    heading = 4
        rospy.loginfo("New robot position: ")
        rospy.loginfo(robot_pos)

    if heading != final_heading:
            if heading == 3:
                if final_heading == 1:
                    turningAround()
                    heading = 1
                if final_heading == 2:
                    turningLeft()
                    heading = 2
                if final_heading == 4:
                    turningRight()
                    heading = 4
            elif heading == 4:
                if final_heading == 3:
                    turningLeft()
                    heading = 3
                if final_heading == 1:
                    turningRight()
                    heading = 1
                if final_heading == 2:
                    turningAround()
                    heading = 2
            elif heading == 1:
                if final_heading == 3:
                    turningAround()
                    heading = 3
                if final_heading == 2:
                    turningRight()
                    heading = 2
                elif final_heading == 4:
                    turningLeft()
                    heading = 4
            elif heading == 2:
                if final_heading == 3:
                    turningRight()
                    heading = 3
                if final_heading == 1:
                    turningLeft()
                    heading = 1
                if final_heading == 4:
                    turningAround()
                    heading = 4

    print "Heading: ",heading
    return heading, robot_pos


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
    
    if len(sys.argv) > 1 and int(sys.argv[1]) == 3:
        rospy.loginfo('Building a map of the world. \n')

        map0 = EECSMap()
        map0.clearObstacleMap()
        map0.printObstacleMap() # DEBUG

        heading = 3

        for x in range(8):
            for y in range(8):
                map0.setCost(x, y, -1)

        stack = [[0,0]]
        while len(stack) > 0:
            
            position = stack[0]
            # print "Position: ",position
            stack = stack[1:]
            map0.setCost(position[0],position[1],0)

            for direction in range(1,5):
                addNeighbor = False
                # rospy.loginfo('Checking direction %i \n', direction)
                if direction % 4 == heading % 4:
                    if getSensorValue(5) > 1500:
                        map0.setObstacle(position[0], position[1], 1, direction)
                    else:
                        if map0.getNeighborCost(position[0], position[1], direction) == -1:
                            addNeighbor = True                            
                elif direction % 4 == (heading + 1) % 4:
                    if getSensorValue(6) > 20:
                        map0.setObstacle(position[0], position[1], 1, direction)
                    else:
                        if map0.getNeighborCost(position[0], position[1], direction) == -1:
                            addNeighbor = True                            
                elif direction % 4 == (heading -1) % 4:
                    if getSensorValue(2) > 20:
                        map0.setObstacle(position[0], position[1], 1, direction)
                    else:
                        if map0.getNeighborCost(position[0], position[1], direction) == -1:
                            addNeighbor = True                            
                
                if addNeighbor:
                    map0.setNeighborCost(position[0], position[1], direction, 0)
                    neighbori = position[0]
                    neighborj = position[1]
                    if direction == 1: #North
                        neighbori -= 1
                    elif direction == 2: #East
                        neighborj += 1
                    elif direction == 3: #South
                        neighbori += 1
                    elif direction == 4: #West
                        neighborj -= 1
                    stack.insert(0,[neighbori, neighborj])

            # move to next position
            try:
                new_pos = stack[0]
                # print "new_pos: ",new_pos
            except:
                new_pos = position

            # print "Creating queue"
            q = Queue.Queue()
            q.put([new_pos[0], new_pos[1], 0])
            for x in range(8):
                for y in range(8):
                    if map0.getCost(x,y) > -1:
                        map0.setCost(x,y,99)
            map0.setCost(new_pos[0],new_pos[1],0)

            # print "Setting costs"
            while map0.getCost(position[0],position[1]) == 99 and not q.empty():
                current_node = q.get()
                for direction in range(1,5):
                    if map0.getNeighborCost(current_node[0], current_node[1], direction) == 99:
                        if not map0.getNeighborObstacle(current_node[0], current_node[1], direction):
                            map0.setNeighborCost(current_node[0], current_node[1], direction, current_node[2] + 1)
                            neighbori = current_node[0]
                            neighborj = current_node[1]
                            neighborCost = current_node[2] + 1
                            if direction == 1: #North
                                neighbori -= 1
                            elif direction == 2: #East
                                neighborj += 1
                            elif direction == 3: #South
                                neighbori += 1
                            elif direction == 4: #West
                                neighborj -= 1
                            q.put([neighbori, neighborj, neighborCost])

            # print "Creating path"
            path = []
            path.append([position[0], position[1]])
            current_cost = map0.getCost(position[0], position[1])
            # map0.printCostMap()

            # print "Finding path"
            while current_cost != 0:
                curr_node = path[-1]
                for direction in range(1,5):
                    # rospy.loginfo('Checking path %i \n', direction)
                    if not map0.getNeighborObstacle(curr_node[0],curr_node[1], direction):
                        if map0.getNeighborCost(curr_node[0],curr_node[1], direction) < current_cost and map0.getNeighborCost(curr_node[0],curr_node[1], direction) >= 0:
                            neighbori = curr_node[0]
                            neighborj = curr_node[1]
                            if direction == 1: #North
                                neighbori -= 1
                            elif direction == 2: #East
                                neighborj += 1
                            elif direction == 3: #South
                                neighbori += 1
                            elif direction == 4: #West
                                neighborj -= 1
                            path.append([neighbori, neighborj])
                            current_cost = map0.getCost(neighbori, neighborj)
                            break

            # print path

            robot_pos = [position[0], position[1]]

            path = path[1:]
            while robot_pos != [new_pos[0], new_pos[1]] and len(path) > 0:
                k = 1
                if heading == 3:
                    if path[0][0] > robot_pos[0]:
                        while len(path) > 1 and path[1][0] > path[0][0]:
                            path = path[1:]
                            k += 1
                        step(k)
                        heading = 3
                        robot_pos[0] += k
                        path = path[1:]
                    elif path[0][0] < robot_pos[0]:
                        turningAround()
                        heading = 1
                    else:
                        if path[0][1] > robot_pos[1]:
                            if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                                while getSensorValue(DMS_port) < 1700:
                                    step(1)
                            turningLeft()
                            heading = 2
                        elif path[0][1] < robot_pos[1]:
                            if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                                while getSensorValue(DMS_port) < 1700:
                                    step(1)
                            turningRight()
                            heading = 4
                elif heading == 4:
                    if path[0][0] > robot_pos[0]:
                        if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                            while getSensorValue(DMS_port) < 1700:
                                step(1)
                        turningLeft()
                        heading = 3
                    elif path[0][0] < robot_pos[0]:
                        if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                            while getSensorValue(DMS_port) < 1700:
                                step(1)
                        turningRight()
                        heading = 1
                    else:
                        if path[0][1] > robot_pos[1]:
                            turningAround()
                            heading = 2
                        elif path[0][1] < robot_pos[1]:
                            while len(path) > 1 and path[1][1] < path[0][1]:
                                path = path[1:]
                                k += 1
                            step(k)
                            heading = 4
                            robot_pos[1] -= k
                            path = path[1:]
                elif heading == 1:
                    if path[0][0] > robot_pos[0]:
                        turningAround()
                        heading = 3
                    elif path[0][0] < robot_pos[0]:
                        while len(path) > 1 and path[1][0] < path[0][0]:
                                path = path[1:]
                                k += 1
                        step(k)
                        heading = 1
                        robot_pos[0] -= k
                        path = path[1:]
                    else:
                        if path[0][1] > robot_pos[1]:
                            if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                                while getSensorValue(DMS_port) < 1700:
                                    step(1)
                            turningRight()
                            heading = 2
                        elif path[0][1] < robot_pos[1]:
                            if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                                while getSensorValue(DMS_port) < 1700:
                                    step(1)
                            turningLeft()
                            heading = 4
                elif heading == 2:
                    if path[0][0] > robot_pos[0]:
                        if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                            while getSensorValue(DMS_port) < 1700:
                                step(1)
                        turningRight()
                        heading = 3
                    elif path[0][0] < robot_pos[0]:
                        if map0.getNeighborObstacle(robot_pos[0], robot_pos[1],heading):
                            while getSensorValue(DMS_port) < 1700:
                                step(1)
                        turningLeft()
                        heading = 1
                    else:
                        if path[0][1] > robot_pos[1]:
                            while len(path) > 1 and path[1][1] > path[0][1]:
                                path = path[1:]
                                k += 1
                            step(k)
                            heading = 2
                            robot_pos[1] += k
                            path = path[1:]
                        elif path[0][1] < robot_pos[1]:
                            turningAround()
                            heading = 4
                # rospy.loginfo("New robot position: ")
                # rospy.loginfo(robot_pos)

            for x in range(8):
                for y in range(8):
                    if map0.getCost(x,y) > 0:
                        map0.setCost(x, y, 0)

            # map0.printCostMap()
            map0.printObstacleMap()

        rospy.loginfo("Final obstacle map")
        map0.printObstacleMap()

    else:
        map0 = EECSMap()
        map0.printObstacleMap()

    setMotorMode(7,1)
    setMotorMode(6,1)

    i = 0
    j = 0

    # Localization
    if len(sys.argv) > 1 and int(sys.argv[1]) == 1:
        rospy.loginfo('Walking to destination. \n')
        i = int(sys.argv[2])
        j = int(sys.argv[3])

        rospy.loginfo("i: %i  \n", i)
        rospy.loginfo("j: %i  \n", j)

        step(i)
        if j > 0:
            turningLeft()
        step(j)
    
    # Planning
    if len(sys.argv) > 1 and int(sys.argv[1]) == 2:
        rospy.loginfo('Following path to destination. \n')
        si = int(sys.argv[2])
        sj = int(sys.argv[3])
        h = int(sys.argv[4])
        gi = int(sys.argv[5])
        gj = int(sys.argv[6])
        final_heading = int(sys.argv[7])
   
        heading, robot_pos = follow_path(si, sj, h, gi, gj, final_heading, map0)

        rospy.loginfo("Final robot position: ")
        rospy.loginfo(robot_pos)
        rospy.loginfo("Final robot heading: %i\n",heading)

    while not rospy.is_shutdown():

        # turningAround()
        # rospy.loginfo("Gyro: %i\n",getSensorValue(1))
        startposx = input("What X coordinate do you want to start at? \n")
        startposy = input("What Y coordinate do you want to start at? \n")
        startheading = input("What heading do you want to start at? \n")
        endposx = input("What X coordinate do you want to end at? \n")
        endposy = input("What Y coordinate do you want to end at? \n")
        endheading = input("What heading do you want to end at? \n")
        follow_path(startposx,startposy, startheading, endposx, endposy, endheading, map0)

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
