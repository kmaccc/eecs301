# Python file for testing nearest neighbor
# Will probably need this website:
# http://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
import math

if (__name__ == '__main__'):

    # Test
    train = open('train.txt')
    test = open('test.txt')

    train_data = []
    test_data = []

    for line in train:
        splitstring = line.split(',')
        for i in range(len(splitstring)):
            splitstring[i] = float(splitstring[i])
        train_data.append(splitstring)

    print train_data

    for line in test:
        splitstring = line.split(',')
        for i in range(len(splitstring)):
            splitstring[i] = float(splitstring[i])
        test_data.append(splitstring)

    print test_data

    labels = []
    for test_pt in test_data:
        error_vec = []
        for train_pt in train_data:
            err = 0
            for i in range(len(train_pt)):
                err += (test_pt[i] - train_pt[i])**2
            error_vec.append(math.sqrt(err))

        top_5 = [999]*5
        for err in error_vec:
            if err < min(top_5):
                top_5[top_5.index(min(top_5))] = err

        potential_label = {'-2':0, '-1':0, '0':0, '1':0, '2':0}

        for x in top_5:
            val = potential_label[str(x[7])] + 1
            potential_label[x[7]] = val


        labels.append(max(potential_label.values()))
