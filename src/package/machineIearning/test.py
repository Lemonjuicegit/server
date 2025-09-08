import numpy as np
import matplotlib.pylab as plt
import tensorflow as tf  # 引入tensorflow只是为了导入mnist数据集


# 下面一大段都是定义函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_grad(x):
    return (1.0 - sigmoid(x)) * sigmoid(x)


def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    # grad = np.zeros(x)
    # grad[x>=0] = 1
    x = np.where(x >= 0, 1, 0)
    return x


def softmax(x):
    if x.ndim == 2:
        x = x.T
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)
        return y.T

    x = x - np.max(x)  # 溢出对策
    return np.exp(x) / np.sum(np.exp(x))


def mean_squared_error(y, t):
    return 0.5 * np.sum((y - t) ** 2)


def cross_entropy_error(y, t):
    """
    计算交叉熵误差。
    
    参数:
    y -- 预测的概率分布，形状为(batch_size, num_classes)。
         如果输入为一维数组，则将其转换为形状为(1, num_classes)的二维数组。
    t -- 正确解标签，可以是一维数组或与预测概率分布形状相同的二维one-hot向量。
         如果输入为一维数组，则保持原样；如果是二维one-hot向量，则转换为正确解标签的索引的一维数组。
    
    返回:
    一批样本的平均交叉熵误差。
    """
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)

    # 监督数据是one-hot-vector的情况下，转换为正确解标签的索引
    if t.size == y.size:
        t = t.argmax(axis=1)

    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size


def softmax_loss(X, t):
    y = softmax(X)
    return cross_entropy_error(y, t)


def numerical_gradient(f, x):
    """
    计算并返回给定函数f在输入x处的数值梯度。

    数值梯度是通过微小的变化量来近似函数在某一点上的导数。
    这个函数通过遍历输入x的每一个维度，并使用中心差分方法来计算该维度上的偏导数。

    参数:
    f: 一个接受向量或矩阵输入并返回标量的函数，代表了我们需要求梯度的函数。
    x: 输入向量或矩阵，我们要求f在该点的梯度。

    返回:
    grad: 与x形状相同的数组，表示函数f在x处的梯度。
    """
    h = 1e-4  # 0.0001
    grad = np.zeros_like(x)

    it = np.nditer(x, flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        fxh1 = f(x)  # f(x+h)

        x[idx] = tmp_val - h
        fxh2 = f(x)  # f(x-h)
        grad[idx] = (fxh1 - fxh2) / (2 * h)

        x[idx] = tmp_val  # 还原值
        it.iternext()

    return grad


class TwoLayerNet:
    def __init__(self, input_size, hidden_size, output_size, weight_init_std=0.01):
        """
        初始化神经网络的结构和参数。

        Args:
            input_size (int): 输入层的神经元数量。
            hidden_size (int): 隐藏层的神经元数量。
            output_size (int): 输出层的神经元数量。
            weight_init_std (float, optional): 权重的初始化标准差。默认是0.01。
        """
        self.params = {}
        self.params["W1"] = weight_init_std * np.random.randn(input_size, hidden_size)
        self.params["b1"] = np.zeros(hidden_size)
        self.params["W2"] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params["b2"] = np.zeros(output_size)

    def predict(self, x):
        """
        根据输入数据x进行预测。

        Args:
            x (ndarray): 输入数据。

        Returns:
            ndarray: 预测结果，经过softmax函数处理的概率分布。
        """
        W1, W2 = self.params["W1"], self.params["W2"]
        b1, b2 = self.params["b1"], self.params["b2"]

        a1 = np.dot(x, W1) + b1
        # z1 = sigmoid(a1)
        z1 = relu(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)

        return y

    # x:输入数据, t:监督数据
    def loss(self, x, t):
        """
        计算神经网络的损失函数值。

        Args:
            x (ndarray): 输入数据.
            t (ndarray): 监督数据（正确答案）.

        Returns:
            float: 交叉熵误差。
        """
        y = self.predict(x)

        return cross_entropy_error(y, t)

    def accuracy(self, x, t):
        """
        计算神经网络的准确率。

        Args:
            x (ndarray): 输入数据.
            t (ndarray): 监督数据（正确答案）.

        Returns:
            float: 准确率。
        """
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        t = np.argmax(t, axis=1)

        accuracy = np.sum(y == t) / float(x.shape[0])
        return accuracy

    # x:输入数据, t:监督数据
    def numerical_gradient(self, x, t):
        """
        计算神经网络参数的数值梯度。

        Args:
            x (ndarray): 输入数据.
            t (ndarray): 监督数据（正确答案）.

        Returns:
            dict: 包含各参数的梯度的字典。
        """
        loss_W = lambda W: self.loss(x, t)

        grads = {}
        grads["W1"] = numerical_gradient(loss_W, self.params["W1"])
        grads["b1"] = numerical_gradient(loss_W, self.params["b1"])
        grads["W2"] = numerical_gradient(loss_W, self.params["W2"])
        grads["b2"] = numerical_gradient(loss_W, self.params["b2"])

        return grads

    def gradient(self, x, t):
        """
        计算神经网络参数的梯度（反向传播法）。

        Args:
            x (ndarray): 输入数据.
            t (ndarray): 监督数据（正确答案）.

        Returns:
            dict: 包含各参数的梯度的字典。
        """
        W1, W2 = self.params["W1"], self.params["W2"]
        b1, b2 = self.params["b1"], self.params["b2"]
        grads = {}

        batch_num = x.shape[0]

        # forward
        a1 = np.dot(x, W1) + b1
        # z1 = sigmoid(a1)
        z1 = relu(a1)
        a2 = np.dot(z1, W2) + b2
        y = softmax(a2)

        # backward
        dy = (y - t) / batch_num
        grads["W2"] = np.dot(z1.T, dy)
        grads["b2"] = np.sum(dy, axis=0)

        da1 = np.dot(dy, W2.T)
        # dz1 = sigmoid_grad(a1) * da1
        dz1 = relu_grad(a1) * da1
        grads["W1"] = np.dot(x.T, dz1)
        grads["b1"] = np.sum(dz1, axis=0)

        return grads


def _change_one_hot_label(X):
    T = np.zeros((X.size, 10))
    for idx, row in enumerate(T):
        row[X[idx]] = 1

    return T


# 开搞
# 读入数据
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # 归一化
x_train = x_train.reshape(-1, 784)  # flatten, (60000,28,28)变（60000,784）
x_test = x_test.reshape(-1, 784)  # flatten, (10000,28,28)变（10000,784）
y_train = _change_one_hot_label(
    y_train
)  # 标签变独热码，才能和前向传播softmax之后的结果维度匹配，才能相减算误差
y_test = _change_one_hot_label(y_test)  # 标签变独热码

# 两层DNN(隐藏层50个神经元，784*50*10)，激活函数是relu，可自己改成sigmoid，损失函数是交叉熵误差，输出层是softmax，优化函数是SGD
network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

# 超参数设置
iters_num = 10000
train_size = x_train.shape[0]
batch_size = 512
learning_rate = 0.05

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = max(train_size / batch_size, 1)

# 训练
for i in range(iters_num):
    batch_mask = np.random.choice(train_size, batch_size)
    x_batch = x_train[batch_mask]
    y_batch = y_train[batch_mask]

    # 梯度
    # grad = network.numerical_gradient(x_batch, t_batch)
    grad = network.gradient(x_batch, y_batch)

    # 更新
    for key in ("W1", "b1", "W2", "b2"):
        network.params[key] -= learning_rate * grad[key]

    loss = network.loss(x_batch, y_batch)
    train_loss_list.append(loss)

    # 每一个epoch打印训练和测试的准确率
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train, y_train)
        test_acc = network.accuracy(x_test, y_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print(train_acc, test_acc)

# 绘制 loss 曲线
plt.subplot(1, 2, 1)
plt.title("Loss Function Curve")  # 图片标题
plt.xlabel("Step")  # x轴变量名称
plt.ylabel("Loss")  # y轴变量名称
plt.plot(train_loss_list, label="$Loss$")  # 逐点画出loss值并连线，连线图标是Loss
plt.legend()  # 画出曲线图标

# 绘制 Accuracy 曲线
plt.subplot(1, 2, 2)
plt.title("Acc Curve")  # 图片标题
plt.xlabel("Epoch")  # x轴变量名称
plt.ylabel("Acc")  # y轴变量名称
plt.plot(train_acc_list, label="$train_{acc}$")  # 逐点画出train_acc值并连线
plt.plot(test_acc_list, label="$test_{acc}$")  # 逐点画出test_acc值并连线
plt.legend()
plt.show()
