
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class fittedFun:
    """
    拟合函数:
        线性函数: linear
        指数函数: exponential
        对数函数: logarithm
        幂指数函数: power
        多项式函数: polynomial
    """
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHM = "logarithm"
    POWER = "power"
    POLYNOMIAL = "polynomial"
    
    
def fitted(data: List[List[float]], fitted_fun: str, titlel:str,):
    def linear_func(x, A, B):
        return A * x + B
     
    def polynomial_func(x, A, B, C, D):
        return A * (x**3) + B * (x**2) + C * x + D
    

    def exponential_func(x, A, B):
        return A * np.exp(x) + B

    def logarithm_func(x, A, B):
        return A * np.log(x) + B

    def power_func(x, A, B, C):
        return A * (x**B) + C
    
    fitted_fun = None
    
    match fitted_fun:
        case fittedFun.LINEAR:
            fitted_fun = linear_func
        case fittedFun.EXPONENTIAL:
            fitted_fun = exponential_func
        case fittedFun.LOGARITHM:
            fitted_fun = logarithm_func
        case fittedFun.POWER:
            fitted_fun = power_func
        case fittedFun.POLYNOMIAL:
            fitted_fun = polynomial_func
        case _:
            pass
            
    
    

    # 拟合数据
    x_data = [i[0] for i in data]
    y_data = [i[1] for i in data]

    popt, pcov = curve_fit(fitted_fun, x_data, y_data)

    # 绘制数据和拟合曲线
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=(8, 6))
    plt.scatter(x_data, y_data, label=r"数据点", color="blue")
    plt.plot(x_data, fitted_fun(x_data, *popt), "r-", label="拟合曲线")
    plt.legend()
    plt.title(titlel)
    plt.show()
