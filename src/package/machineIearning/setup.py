import numpy as np
import csv
from active import *
from pathlib import Path

class Neure:
    def __init__(self, X, W, B, learning_rate):
        self.X = X
        self.W = W
        self.B = B
        self.Y = None
        self.learning_rate = learning_rate # 学习率
    def active_fun(self, active):
        self.Y = active(
            np.dot(self.W,self.X.T) + self.B
        )

def init_model(w_size,b_size, savapath, scope=[0,1]):
    """随机生成模型参数csv文件

    Args:
        w_size (int): _description_
        b_size (int): _description_
        savapath (str): _description_
        scope (List): _description_. Defaults to [0,1].
    """
    def w():
        return np.random.rand(w_size) * (scope[1] - scope[0]) + scope[0]
    with open(rf"{savapath}\model.csv", "a", encoding="utf-8", newline="") as f:
        b = np.random.rand(b_size) * (scope[1] - scope[0]) + scope[0]
        matrix = [[*w(),v] for v in b]
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)
def read_ubyte(ubyte_images,ubyte_labels):
    """读取ubyte数据
    
    Returns:
        _type_: _description_
    """
    images = np.frombuffer(ubyte_images, np.uint8)[16:].reshape([-1, 28*28])
    labels = np.frombuffer(ubyte_labels, np.uint8)[8:]
    return images,labels

def training(model_csv, images_data, labels_data):
    args = np.loadtxt(model_csv[0],delimiter=",", dtype=float)
    args2 = np.loadtxt(model_csv[1], delimiter=",", dtype=float)
    W = np.array([v[:-1] for v in args])
    B = np.array([v[-1] for v in args])
    W2 = np.array([v[:-1] for v in args2])
    B2 = np.array([v[-1] for v in args2])
    images, labels = read_ubyte(images_data, labels_data)
    Neure1 = Neure(images[0], W,B,0.1)
    Neure1.active_fun(relU)
    Neure2 = Neure(Neure1.Y, W2, B2, 0.1)
    Neure2.active_fun(sigmoid)
    res = softmax(Neure2.Y)
    
    for i in range(100):
        pass

    
if __name__ == "__main__":
    images_data = Path(r"D:\深度学习\MNIST数据集\t10k-images.idx3-ubyte").read_bytes()
    labels_data = Path(r"D:\深度学习\MNIST数据集\t10k-labels.idx1-ubyte").read_bytes()
    csvpath = (
        r"E:\exploitation\collection\server\package\machineIearning\model_args1.csv"
    )
    cs2path = (
        r"E:\exploitation\collection\server\package\machineIearning\model_args2.csv"
    )
    training([csvpath, cs2path], images_data, labels_data)
    # init_model(
    #     32, 10, r"E:\exploitation\collection\server\package\machineIearning",[1,2]
    # )
        