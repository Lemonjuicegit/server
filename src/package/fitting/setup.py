import numpy as np
import matplotlib.pyplot as plt
def fitted(x, y, n):
    """多项式拟合

    Args:
        x (list): 待拟合x数组
        y (list): 待拟合y数组
        n (int): 多项式阶数
    """
    x_array = np.array(x)
    y_array = np.array(y)
    coefficients = np.polyfit(x_array, y_array, n)
    fitted_curve = np.polyval(coefficients, x_array)
    return fitted_curve

def plot(title,x_data, y_data, fitted_value, xlabel, ylabel, scatter_label, plot_label):
    """拟合曲线可视化

    Args:
        title (str): 标题
        x_data (np.array): 待拟合x数组
        y_data (np.array): 待拟合y数组
        fitted_value (np.array): 拟合y值
        xlabel (str): x轴描述
        ylabel (str): y轴描述
        scatter_label (str): 拟合点图例描述
        plot_label (str): 拟合曲线图例描述
    """
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label=scatter_label, color="blue")
    plt.plot(x_data, fitted_value, "r-", label=plot_label)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    A_true = 2.0
    B_true = 3.0
    x_data_ = np.linspace(1, 10, 100)
    y_data_ = A_true * np.log(x_data_) + B_true + np.random.normal(0, 0.2, len(x_data_))
    plot()

