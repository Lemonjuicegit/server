
import numpy as np
def softmax(x):
    x = x - np.max(x)
    return np.exp(x) / np.sum(np.exp(x))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relU(x):
    return np.maximum(0, x)
    