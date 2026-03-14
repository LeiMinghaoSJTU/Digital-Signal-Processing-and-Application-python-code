"""
离散信号与卷积运算实现
包含内容：
- 典型离散信号生成（单位脉冲、单位阶跃、指数序列等）
- 离散卷积计算
- 差分方程求解
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter


def unit_impulse(n_min, n_max, n0=0):
    """
    生成单位脉冲序列 δ[n-n0]
    
    参数:
        n_min, n_max: 序列范围
        n0: 脉冲位置
    返回:
        n: 时间索引数组
        x: 信号值数组
    """
    n = np.arange(n_min, n_max + 1)
    x = (n == n0).astype(float)
    return n, x


def unit_step(n_min, n_max, n0=0):
    """
    生成单位阶跃序列 u[n-n0]
    
    参数:
        n_min, n_max: 序列范围
        n0: 阶跃起始位置
    返回:
        n: 时间索引数组
        x: 信号值数组
    """
    n = np.arange(n_min, n_max + 1)
    x = (n >= n0).astype(float)
    return n, x


def exponential_sequence(a, n_min, n_max):
    """
    生成指数序列 a^n
    
    参数:
        a: 指数底数
        n_min, n_max: 序列范围
    返回:
        n: 时间索引数组
        x: 信号值数组
    """
    n = np.arange(n_min, n_max + 1)
    x = np.power(a, n)
    return n, x


def sinusoidal_sequence(A, omega, phi, n_min, n_max):
    """
    生成正弦序列 A*sin(ωn + φ)
    
    参数:
        A: 振幅
        omega: 数字频率
        phi: 初始相位
        n_min, n_max: 序列范围
    返回:
        n: 时间索引数组
        x: 信号值数组
    """
    n = np.arange(n_min, n_max + 1)
    x = A * np.sin(omega * n + phi)
    return n, x


def discrete_convolution(x1, x2):
    """
    计算两个离散序列的卷积和
    
    参数:
        x1, x2: 输入序列
    返回:
        y: 卷积结果
    """
    N1, N2 = len(x1), len(x2)
    N = N1 + N2 - 1
    y = np.zeros(N)
    
    for n in range(N):
        for k in range(N1):
            if 0 <= n - k < N2:
                y[n] += x1[k] * x2[n - k]
    
    return y


def solve_difference_equation(b, a, x, y_init=None):
    """
    求解线性常系数差分方程
    
    差分方程形式：
    a[0]*y[n] + a[1]*y[n-1] + ... + a[N]*y[n-N] = 
    b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M]
    
    参数:
        b: 输入系数数组 [b0, b1, ..., bM]
        a: 输出系数数组 [a0, a1, ..., aN]
        x: 输入信号
        y_init: 初始条件 (可选)
    返回:
        y: 系统输出
    """
    if y_init is not None:
        # 使用初始条件
        y = lfilter(b, a, x, zi=y_init)[0]
    else:
        y = lfilter(b, a, x)
    return y


def system_response_impulse(b, a, N=50):
    """
    计算系统的单位脉冲响应
    
    参数:
        b, a: 差分方程系数
        N: 响应长度
    返回:
        h: 单位脉冲响应
    """
    delta = np.zeros(N)
    delta[0] = 1
    h = lfilter(b, a, delta)
    return h


def check_stability(a):
    """
    根据特征方程系数判断系统稳定性
    （极点是否都在单位圆内）
    
    参数:
        a: 分母多项式系数 [a0, a1, ..., aN]
    返回:
        is_stable: 是否稳定
        poles: 极点位置
    """
    # 求特征方程的根（极点）
    poles = np.roots(a)
    is_stable = all(np.abs(poles) < 1)
    return is_stable, poles


def plot_discrete_signals():
    """绘制典型离散信号示例"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    # 单位脉冲序列
    n, delta = unit_impulse(-5, 10, 0)
    axes[0, 0].stem(n, delta, basefmt=' ')
    axes[0, 0].set_title('Unit Impulse Sequence δ[n]')
    axes[0, 0].set_xlabel('n')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 单位阶跃序列
    n, u = unit_step(-5, 10, 0)
    axes[0, 1].stem(n, u, basefmt=' ', linefmt='r', markerfmt='ro')
    axes[0, 1].set_title('Unit Step Sequence u[n]')
    axes[0, 1].set_xlabel('n')
    axes[0, 1].set_ylabel('Amplitude')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 指数序列
    n, exp_seq = exponential_sequence(0.8, 0, 20)
    axes[0, 2].stem(n, exp_seq, basefmt=' ', linefmt='g', markerfmt='go')
    axes[0, 2].set_title('Exponential Sequence (0.8)^n')
    axes[0, 2].set_xlabel('n')
    axes[0, 2].set_ylabel('Amplitude')
    axes[0, 2].grid(True, alpha=0.3)
    
    # 正弦序列
    n, sin_seq = sinusoidal_sequence(1, 0.3, 0, 0, 50)
    axes[1, 0].stem(n, sin_seq, basefmt=' ', linefmt='m', markerfmt='mo')
    axes[1, 0].set_title('Sinusoidal Sequence sin(0.3n)')
    axes[1, 0].set_xlabel('n')
    axes[1, 0].set_ylabel('Amplitude')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 卷积示例
    x1 = np.array([1, 2, 3, 4])
    x2 = np.array([1, 1, 1])
    y_conv = discrete_convolution(x1, x2)
    n_conv = np.arange(len(y_conv))
    axes[1, 1].stem(n_conv, y_conv, basefmt=' ', linefmt='c', markerfmt='co')
    axes[1, 1].set_title('Convolution: [1,2,3,4] * [1,1,1]')
    axes[1, 1].set_xlabel('n')
    axes[1, 1].set_ylabel('Amplitude')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 系统响应示例
    b = [1]  # 分子系数
    a = [1, -0.8]  # 分母系数: y[n] - 0.8*y[n-1] = x[n]
    h = system_response_impulse(b, a, 30)
    n_h = np.arange(len(h))
    axes[1, 2].stem(n_h, h, basefmt=' ', linefmt='orange', markerfmt='o')
    axes[1, 2].set_title('System Impulse Response (Stable System)')
    axes[1, 2].set_xlabel('n')
    axes[1, 2].set_ylabel('h[n]')
    axes[1, 2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('discrete_signals.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'discrete_signals.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("离散信号与卷积运算演示")
    print("=" * 60)
    
    # 1. 生成单位脉冲序列
    print("\n1. 单位脉冲序列 δ[n]")
    n, delta = unit_impulse(-3, 5, 0)
    print(f"   n = {n}")
    print(f"   δ[n] = {delta}")
    
    # 2. 生成单位阶跃序列
    print("\n2. 单位阶跃序列 u[n]")
    n, u = unit_step(-3, 5, 0)
    print(f"   n = {n}")
    print(f"   u[n] = {u}")
    
    # 3. 卷积计算示例
    print("\n3. 离散卷积计算")
    x1 = np.array([1, 2, 3])
    x2 = np.array([1, 1])
    y = discrete_convolution(x1, x2)
    print(f"   x1 = {x1}")
    print(f"   x2 = {x2}")
    print(f"   x1 * x2 = {y}")
    
    # 与numpy验证
    y_np = np.convolve(x1, x2)
    print(f"   (验证) numpy.convolve = {y_np}")
    
    # 4. 差分方程求解示例
    print("\n4. 差分方程求解")
    print("   差分方程: y[n] - 0.5*y[n-1] = x[n]")
    b = [1]  # x[n]的系数
    a = [1, -0.5]  # y[n]的系数
    x = np.ones(10)  # 输入为单位阶跃
    y = solve_difference_equation(b, a, x)
    print(f"   输入 x[n] = {x}")
    print(f"   输出 y[n] = {y}")
    
    # 5. 稳定性判断
    print("\n5. 系统稳定性判断")
    # 稳定系统
    a_stable = [1, -0.5]
    is_stable, poles = check_stability(a_stable)
    print(f"   系统 H(z)=1/(1-0.5z⁻¹)")
    print(f"   极点: {poles}")
    print(f"   是否稳定: {is_stable}")
    
    # 不稳定系统
    a_unstable = [1, -1.5]
    is_stable, poles = check_stability(a_unstable)
    print(f"\n   系统 H(z)=1/(1-1.5z⁻¹)")
    print(f"   极点: {poles}")
    print(f"   是否稳定: {is_stable}")
    
    # 绘制图形
    print("\n6. 绘制典型离散信号...")
    plot_discrete_signals()


if __name__ == "__main__":
    demo()
