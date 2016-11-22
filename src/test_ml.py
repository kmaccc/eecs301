# Python file for testing nearest neighbor
# Will probably need this website:
# http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
import math
import operator

if (__name__ == '__main__'):
    k = 5

    # Test
    train = open('train_expanded.txt')
    test = open('test_expanded.txt')

    train_data = []
    test_data = []

    for line in train:
        splitstring = line.split(',')
        for i in range(len(splitstring)):
            splitstring[i] = float(splitstring[i])
        train_data.append(splitstring)

    # print train_data

    for line in test:
        splitstring = line.split(',')
        for i in range(len(splitstring)):
            splitstring[i] = float(splitstring[i])
        test_data.append(splitstring)

    # print test_data

    labels = []
    for test_pt in test_data:
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

        potential_label = {'-2':0, '-1':0, '0':0, '1':0, '2':0}

        labelSum = 0
        for x in top_neighbors:
            labelSum += x[-1]
            # potential_label[x[-1]] += 1
        # print potential_label

        labels.append(round(labelSum/k)) 

    print labels

    correct = 0
    i = 0
    for test_pt in test_data:
        if test_pt[-1] == labels[i]:
            correct += 1
        i += 1

    print (correct/float(len(test_data)))*100.0