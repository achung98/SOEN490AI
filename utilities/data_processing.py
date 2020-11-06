# Contains utility functions for data access

# Import statements
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import PIL

# returns a usable format of the input data.  Input (str): path to fil to be loaded, type (str): type of file input
def get_data(path, type = 'csv'):
    if type == 'csv':
        return pd.read_csv(path).to_numpy()
    if type == 'npy':
        return np.load(path)
    else:
        print('type must be \'csv\' or \'npy\'')

''' checks the dataset is balanced, prints out the input dictionary updated with the total amount of each class
in the training set.
Input:
dict(dictionary): initialized with all of the classes with their total count set to 0. ex. class:0
labels(numpy array):  array containing all the labels of the training set instances'''
def check_balance(dict, labels):
    total = 0
    for y in labels:
        dict[int(y)] += 1
        total += 1
    print(dict)

'''given an image path, the function returns a numpy array of a greyscaled image with pixel values normalized between 
0 and 1'''
def preprocess_image(img_path):
    img = PIL.Image.open(img_path).convert("L")
    return np.array(img) / 255.0

'''reformat y to one-hot-vector-format'''
def one_hot_vector(y, num_classes):
    reformat_y = np.zeros((len(y), num_classes))
    j = 0
    while j < len(y):
        reformat_y[j][y[j]] = 1
        j += 1
    return reformat_y