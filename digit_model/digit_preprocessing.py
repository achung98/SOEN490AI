import sys, os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utilities.data_processing import preprocess_image, get_training_arr, one_hot_vector, numeric_class
import constants as c

''' takes an input array "digits", containing the directories to be processed and a string fname to save the output under'''
def preprocess_training_images(digits, fname):
    # preprocess images and add them to the input feature array
    digits_X = get_training_arr(fname)
    for digit in digits:
        for root, dirs, files in os.walk(c.TRAIN_DIGIT_IMGS_BASEDIR+digit):
            for name in files:
                print(name)
                px = preprocess_image(os.path.join(root, name))
                row, col, = px.shape

                if row == 200 and col == 200:
                    px = px.reshape(-1, 200, 200)
                    digits_X = np.append(digits_X, px, axis=0)
                else:
                    # pad image
                    add_r = 200 - row
                    add_c = 200 - col

                    if not add_r == 0:
                        px = np.vstack((np.zeros((add_r, col)), px))
                    if not add_c == 0:
                        px = np.hstack((np.zeros((200, add_c)), px))
                    px = px.reshape(-1, 200, 200)
                    digits_X = np.append(digits_X, px, axis=0)

                np.save(fname, digits_X.reshape(-1, 200, 200))
            print(digits_X.shape)

''' determine number of images for each digit, takes digit as a string'''
def get_digit_amount(digit):
    amt = 0
    for root, dirs, files in os.walk(c.TRAIN_DIGIT_IMGS_BASEDIR + digit):
        for _ in files:
            amt += 1
    print(digit+': '+str(amt))
    return amt

'''creates and saves label array in one hot vector format.'''
def create_digit_labels():
    digits_y = np.zeros(get_digit_amount("0"), dtype=int)
    for i in range(1, 10):
        arr = np.full(get_digit_amount(str(i)), i, dtype=int)
        digits_y = np.concatenate((digits_y, arr))

    digits_y = one_hot_vector(digits_y, num_classes=10)
    print(digits_y.shape)
    np.save('digit_labels.npy', digits_y)

''' shuffles and splits set before use. num samples is the number of images processed'''
def shuffle_train_set(train_X, train_y, classes, num_samples):
    train_X = train_X.reshape(num_samples, -1)
    train_y = numeric_class(train_y).reshape(-1, 1)
    xy = np.hstack((train_X, train_y))
    np.random.shuffle(xy)
    train_X, train_y = xy[:, :40000].reshape(-1, 200, 200), xy[:, -1]
    train_y = one_hot_vector(train_y.astype(int), num_classes=classes)
    return train_X, train_y
