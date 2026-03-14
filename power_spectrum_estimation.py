"""
功率谱估计
包含内容：
- 经典谱估计（周期图法、相关估计法）
- 参数模型谱估计（AR模型）
- Welch方法
- 多窗口法（MTM）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, periodogram, correlate
from scipy.linalg import solve_toeplitz, toeplitz


def periodogram_estimate(x, fs=1.0, window='boxcar'):
    """
    周期图法功率谱估计
    
    公式: P(f) = (1/N) * |sum_{n=0}^{N-1} x[n] * exp(-j*2*pi*f*n)|^2
    
    参数:
        x: 输入信号
        fs: 采样频率
        window: 窗函数类型
    返回:
        f: 频率数组
        P: 功率谱估计
    """
    N = len(x)
    
    # 加窗
    if window == 'boxcar':
        w = np.ones(N)
    elif window == 'hann':
        w = np.hanning(N)
    elif window == 'hamming':
        w = np.hamming(N)
    else:
        w = np.ones(N)
    
    x_windowed = x * w
    
    # 计算周期图
    X = np.fft.fft(x_windowed)
    P = (np.abs(X) ** 2) / N
    
    # 归一化（考虑窗函数能量）
    P = P / (np.sum(w**2) / N)
    
    f = np.fft.fftfreq(N, 1/fs)
    
    # 只返回正频率部分
    positive_freq_idx = f >= 0
    return f[positive_freq_idx], P[positive_freq_idx]


def correlogram_estimate(x, fs=1.0, M=None, window='triangular'):
    """
    相关图法（Blackman-Tukey方法）功率谱估计
    
    通过对自相关函数加窗后做傅里叶变换
    
    参数:
        x: 输入信号
        fs: 采样频率
        M: 最大延迟
        window: 延迟窗类型
    返回:
        f: 频率数组
        P: 功率谱估计
    """
    N = len(x)
    if M is None:
        M = N // 4
    
    # 计算自相关函数
    r = correlate(x, x, mode='full')
    r = r[N-1:] / N  # 取非负延迟部分
    r = r[:M+1]  # 只取前M+1个
    
    # 延迟窗
    if window == 'triangular':
        w = 1 - np.arange(M+1) / (M+1)
    elif window == 'parzen':
        w = 1 - np.abs(np.arange(M+1)) / (M+1)
        w = w ** 2
    else:
        w = np.ones(M+1)
    
    r_windowed = r * w
    
    # 对加窗的自相关函数做FFT
    P = np.fft.rfft(r_windowed, n=2*M)
    P = np.real(P)
    
    f = np.fft.rfftfreq(2*M, 1/fs)
    
    return f, np.abs(P)


def welch_estimate(x, fs=1.0, nperseg=None, noverlap=None, window='hann'):
    """
    Welch方法功率谱估计
    
    将数据分段，对每段做周期图后平均
    
    参数:
        x: 输入信号
        fs: 采样频率
        nperseg: 每段长度
        noverlap: 重叠样本数
        window: 窗函数
    返回:
        f: 频率数组
        P: 功率谱估计
    """
    f, P = welch(x, fs=fs, nperseg=nperseg, noverlap=noverlap, window=window)
    return f, P


def ar_spectrum_estimate(x, order, fs=1.0, nfft=512):
    """
    自回归(AR)模型功率谱估计
    
    使用Yule-Walker方程估计AR模型参数，然后计算功率谱
    
    模型: x[n] = -sum_{k=1}^p a[k] * x[n-k] + e[n]
    
    参数:
        x: 输入信号
        order: AR模型阶数
        fs: 采样频率
        nfft: FFT点数
    返回:
        f: 频率数组
        P: 功率谱估计
        a: AR系数
        sigma2: 白噪声方差
    """
    N = len(x)
    
    # 计算自相关函数
    r = correlate(x, x, mode='full')
    r = r[N-1:] / N
    
    # 构造Toeplitz矩阵和右端向量
    R = toeplitz(r[:order])
    r_vec = -r[1:order+1]
    
    # 求解Yule-Walker方程
    a = solve_toeplitz(r[:order], r_vec)
    a = np.concatenate(([1], a))
    
    # 估计白噪声方差
    sigma2 = r[0] + np.sum(a[1:] * r[1:order+1])
    
    # 计算功率谱
    f = np.linspace(0, fs/2, nfft)
    omega = 2 * np.pi * f / fs
    
    denominator = np.abs(np.sum(a[:, np.newaxis] * 
                               np.exp(-1j * omega[np.newaxis, :] * 
                               np.arange(order+1)[:, np.newaxis]), axis=0)) ** 2
    
    P = sigma2 / denominator
    
    return f, P, a, sigma2


def burg_spectrum_estimate(x, order, fs=1.0, nfft=512):
    """
    Burg算法AR模型功率谱估计
    
    比Yule-Walker方法有更好的频率分辨率
    
    参数:
        x: 输入信号
        order: AR模型阶数
        fs: 采样频率
        nfft: FFT点数
    返回:
        f: 频率数组
        P: 功率谱估计
        a: AR系数
        sigma2: 白噪声方差
    """
    N = len(x)
    
    # 初始化
    f = np.zeros((order+1, N))  # 前向预测误差
    b = np.zeros((order+1, N))  # 后向预测误差
    
    f[0, :] = x
    b[0, :] = x
    
    a = np.zeros(order+1)
    a[0] = 1
    
    sigma2 = np.zeros(order+1)
    sigma2[0] = np.var(x)
    
    # Burg递推
    for m in range(order):
        # 计算反射系数
        numerator = -2 * np.sum(f[m, :-1] * b[m, 1:])
        denominator = np.sum(f[m, :-1]**2 + b[m, 1:]**2)
        k = numerator / (denominator + 1e-10)
        
        # 更新AR系数
        a_prev = a.copy()
        for i in range(m+2):
            if i == 0:
                a[i] = 1
            elif i == m+1:
                a[i] = k
            else:
                a[i] = a_prev[i] + k * a_prev[m+1-i]
        
        # 更新预测误差
        f[m+1, 1:] = f[m, :-1] + k * b[m, 1:]
        b[m+1, 1:] = b[m, :-1] + k * f[m, 1:]
        
        sigma2[m+1] = sigma2[m] * (1 - k**2)
    
    # 计算功率谱
    f_freq = np.linspace(0, fs/2, nfft)
    omega = 2 * np.pi * f_freq / fs
    
    denominator = np.abs(np.sum(a[:, np.newaxis] * 
                               np.exp(-1j * omega[np.newaxis, :] * 
                               np.arange(order+1)[:, np.newaxis]), axis=0)) ** 2
    
    P = sigma2[order] / denominator
    
    return f_freq, P, a, sigma2[order]


def plot_spectrum_comparison():
    """
    比较不同功率谱估计方法
    """
    # 生成测试信号
    np.random.seed(42)
    fs = 1000
    t = np.arange(0, 1, 1/fs)
    
    # 两个正弦信号 + 噪声
    f1, f2 = 100, 250
    x = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t) + 0.3 * np.random.randn(len(t))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 周期图法
    ax = axes[0, 0]
    f_period, P_period = periodogram_estimate(x, fs, window='boxcar')
    f_hann, P_hann = periodogram_estimate(x, fs, window='hann')
    
    ax.semilogy(f_period, P_period, alpha=0.7, label='Rectangular')
    ax.semilogy(f_hann, P_hann, alpha=0.7, label='Hann')
    ax.axvline(f1, color='r', linestyle='--', alpha=0.5)
    ax.axvline(f2, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title('Periodogram Method')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. Welch方法
    ax = axes[0, 1]
    for nperseg, color in [(256, 'blue'), (128, 'green'), (64, 'red')]:
        f_welch, P_welch = welch_estimate(x, fs, nperseg=nperseg, noverlap=nperseg//2)
        ax.semilogy(f_welch, P_welch, color=color, alpha=0.7, 
                    label=f'Segment={nperseg}')
    ax.axvline(f1, color='r', linestyle='--', alpha=0.5)
    ax.axvline(f2, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title('Welch Method')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. AR模型谱估计
    ax = axes[1, 0]
    for order, color in [(4, 'blue'), (8, 'green'), (16, 'red')]:
        f_ar, P_ar, _, _ = ar_spectrum_estimate(x, order, fs)
        ax.semilogy(f_ar, P_ar, color=color, alpha=0.7, label=f'AR({order})')
    ax.axvline(f1, color='r', linestyle='--', alpha=0.5)
    ax.axvline(f2, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title('AR Model Spectrum')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. 方法比较
    ax = axes[1, 1]
    f_period, P_period = periodogram_estimate(x, fs, window='hann')
    f_welch, P_welch = welch_estimate(x, fs, nperseg=128)
    f_ar, P_ar, _, _ = ar_spectrum_estimate(x, 8, fs)
    
    ax.semilogy(f_period, P_period, alpha=0.7, label='Periodogram')
    ax.semilogy(f_welch, P_welch, alpha=0.7, label='Welch')
    ax.semilogy(f_ar, P_ar, alpha=0.7, label='AR(8)')
    ax.axvline(f1, color='r', linestyle='--', alpha=0.5)
    ax.axvline(f2, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power/Frequency (dB/Hz)')
    ax.set_title('Spectrum Estimation Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spectrum_estimation.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'spectrum_estimation.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("功率谱估计演示")
    print("=" * 60)
    
    # 生成测试信号
    np.random.seed(42)
    fs = 1000
    t = np.arange(0, 1, 1/fs)
    f1, f2 = 100, 250
    x = np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t) + 0.3 * np.random.randn(len(t))
    
    print(f"\n1. 测试信号: 正弦波 {f1}Hz + {f2}Hz + 噪声")
    print(f"   采样频率: {fs}Hz")
    print(f"   样本数: {len(x)}")
    
    # 1. 周期图法
    print("\n2. 周期图法功率谱估计")
    f_period, P_period = periodogram_estimate(x, fs, window='hann')
    peak_idx = np.argmax(P_period)
    print(f"   峰值频率: {f_period[peak_idx]:.1f}Hz")
    print(f"   峰值功率: {P_period[peak_idx]:.4f}")
    
    # 2. Welch方法
    print("\n3. Welch方法功率谱估计")
    f_welch, P_welch = welch_estimate(x, fs, nperseg=256)
    print(f"   分段数: {len(x)//128}")
    print(f"   频率分辨率: {f_welch[1]-f_welch[0]:.2f}Hz")
    
    # 3. AR模型
    print("\n4. AR模型功率谱估计")
    f_ar, P_ar, a, sigma2 = ar_spectrum_estimate(x, 8, fs)
    print(f"   AR模型阶数: 8")
    print(f"   AR系数: {a}")
    print(f"   白噪声方差: {sigma2:.4f}")
    
    # 4. Burg算法
    print("\n5. Burg算法功率谱估计")
    f_burg, P_burg, a_burg, sigma2_burg = burg_spectrum_estimate(x, 8, fs)
    print(f"   AR系数: {a_burg}")
    print(f"   白噪声方差: {sigma2_burg:.4f}")
    
    # 绘制比较图
    print("\n6. 绘制谱估计比较图...")
    plot_spectrum_comparison()


if __name__ == "__main__":
    demo()
