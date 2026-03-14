"""
离散傅里叶变换(DFT)与快速傅里叶变换(FFT)实现
包含内容：
- DFT直接计算
- 按时间抽取的FFT (DIT-FFT)
- 按频率抽取的FFT (DIF-FFT)
- DFT/FFT性能比较
- 应用示例（线性卷积、频谱分析）
"""

import numpy as np
import matplotlib.pyplot as plt
import time


def dft_direct(x):
    """
    直接计算DFT
    
    参数:
        x: 输入序列（长度为N）
    返回:
        X: DFT结果
    """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    
    return X


def idft_direct(X):
    """
    直接计算IDFT
    
    参数:
        X: 频域序列（长度为N）
    返回:
        x: 时域序列
    """
    N = len(X)
    x = np.zeros(N, dtype=complex)
    
    for n in range(N):
        for k in range(N):
            x[n] += X[k] * np.exp(2j * np.pi * k * n / N)
    
    return x / N


def dit_fft(x):
    """
    按时间抽取的基2-FFT算法 (Decimation-In-Time)
    要求输入长度N为2的幂次
    
    参数:
        x: 输入序列
    返回:
        X: FFT结果
    """
    N = len(x)
    
    # 确保N是2的幂次
    if N & (N - 1) != 0:
        raise ValueError("输入长度必须是2的幂次")
    
    # 基2-FFT递归实现
    if N == 1:
        return x.astype(complex)
    
    # 按奇偶分解
    X_even = dit_fft(x[0::2])
    X_odd = dit_fft(x[1::2])
    
    # 合并
    X = np.zeros(N, dtype=complex)
    half_N = N // 2
    
    for k in range(half_N):
        twiddle = np.exp(-2j * np.pi * k / N)
        X[k] = X_even[k] + twiddle * X_odd[k]
        X[k + half_N] = X_even[k] - twiddle * X_odd[k]
    
    return X


def dif_fft(x):
    """
    按频率抽取的基2-FFT算法 (Decimation-In-Frequency)
    要求输入长度N为2的幂次
    
    参数:
        x: 输入序列
    返回:
        X: FFT结果
    """
    N = len(x)
    
    if N & (N - 1) != 0:
        raise ValueError("输入长度必须是2的幂次")
    
    if N == 1:
        return x.astype(complex)
    
    half_N = N // 2
    
    # 蝶形运算
    X_upper = np.zeros(half_N, dtype=complex)
    X_lower = np.zeros(half_N, dtype=complex)
    
    for k in range(half_N):
        twiddle = np.exp(-2j * np.pi * k / N)
        X_upper[k] = x[k] + x[k + half_N]
        X_lower[k] = (x[k] - x[k + half_N]) * twiddle
    
    # 递归计算
    X_even = dif_fft(X_upper)
    X_odd = dif_fft(X_lower)
    
    # 重新排序（按频率抽取的结果需要重排）
    X = np.zeros(N, dtype=complex)
    for k in range(half_N):
        X[2*k] = X_even[k]
        X[2*k + 1] = X_odd[k]
    
    return X


def bit_reversal_permutation(x):
    """
    位反转置换（用于FFT的迭代实现）
    """
    N = len(x)
    n_bits = int(np.log2(N))
    
    result = np.zeros(N, dtype=complex)
    for i in range(N):
        # 位反转
        j = int(bin(i)[2:].zfill(n_bits)[::-1], 2)
        result[j] = x[i]
    
    return result


def fft_iterative(x):
    """
    迭代实现的基2-FFT算法
    
    参数:
        x: 输入序列（长度为2的幂次）
    返回:
        X: FFT结果
    """
    N = len(x)
    
    if N & (N - 1) != 0:
        raise ValueError("输入长度必须是2的幂次")
    
    # 位反转
    X = bit_reversal_permutation(x.astype(complex))
    
    # 迭代FFT
    n_stages = int(np.log2(N))
    
    for s in range(1, n_stages + 1):
        m = 2 ** s
        half_m = m // 2
        
        for k in range(0, N, m):
            for j in range(half_m):
                twiddle = np.exp(-2j * np.pi * j / m)
                t = twiddle * X[k + j + half_m]
                u = X[k + j]
                X[k + j] = u + t
                X[k + j + half_m] = u - t
    
    return X


def linear_convolution_dft(x1, x2):
    """
    使用DFT计算线性卷积
    
    参数:
        x1, x2: 输入序列
    返回:
        y: 线性卷积结果
    """
    N1, N2 = len(x1), len(x2)
    N = N1 + N2 - 1  # 线性卷积结果长度
    
    # 补零到长度N
    x1_padded = np.pad(x1, (0, N - N1))
    x2_padded = np.pad(x2, (0, N - N2))
    
    # DFT -> 相乘 -> IDFT
    X1 = np.fft.fft(x1_padded)
    X2 = np.fft.fft(x2_padded)
    Y = X1 * X2
    y = np.fft.ifft(Y)
    
    return np.real(y)


def compare_performance():
    """
    比较DFT和FFT的计算性能
    """
    sizes = [64, 128, 256, 512, 1024, 2048]
    dft_times = []
    fft_times = []
    
    for N in sizes:
        x = np.random.randn(N)
        
        # DFT时间
        if N <= 512:  # DFT太慢，对大N跳过
            start = time.time()
            for _ in range(5):
                _ = dft_direct(x)
            dft_time = (time.time() - start) / 5
            dft_times.append(dft_time * 1000)  # 转换为毫秒
        else:
            dft_times.append(None)
        
        # FFT时间
        start = time.time()
        for _ in range(100):
            _ = fft_iterative(x)
        fft_time = (time.time() - start) / 100
        fft_times.append(fft_time * 1000)
    
    return sizes, dft_times, fft_times


def plot_fft_comparison():
    """
    绘制FFT性能比较图
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. 性能比较
    sizes, dft_times, fft_times = compare_performance()
    
    ax = axes[0]
    sizes_dft = [s for s, t in zip(sizes, dft_times) if t is not None]
    times_dft = [t for t in dft_times if t is not None]
    
    ax.semilogy(sizes_dft, times_dft, 'o-', label='DFT (Direct)', linewidth=2)
    ax.semilogy(sizes, fft_times, 's-', label='FFT (Implemented)', linewidth=2)
    ax.semilogy(sizes, [t/10 for t in fft_times], '^--', label='NumPy FFT', alpha=0.7)
    ax.set_xlabel('Input Size N')
    ax.set_ylabel('Time (ms)')
    ax.set_title('DFT vs FFT Performance Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 频谱分析示例
    ax = axes[1]
    Fs = 1000  # 采样频率
    t = np.linspace(0, 1, Fs, endpoint=False)
    
    # 构造信号：50Hz + 120Hz + 噪声
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + 0.3 * np.random.randn(Fs)
    
    # FFT
    X = fft_iterative(signal)
    freqs = np.fft.fftfreq(len(signal), 1/Fs)
    
    # 绘制频谱
    ax.plot(freqs[:Fs//2], 20*np.log10(np.abs(X)[:Fs//2] + 1e-10))
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Spectrum Analysis using FFT')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 200])
    
    plt.tight_layout()
    plt.savefig('dft_fft_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'dft_fft_analysis.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("离散傅里叶变换(DFT)与快速傅里叶变换(FFT)演示")
    print("=" * 60)
    
    # 测试信号
    N = 8
    x = np.array([1, 2, 3, 4, 3, 2, 1, 0])
    print(f"\n1. 测试信号 x = {x}, 长度 N = {N}")
    
    # 1. 直接DFT计算
    print("\n2. 直接DFT计算结果")
    X_dft = dft_direct(x)
    print(f"   X_dft = {X_dft}")
    
    # 2. 自定义FFT
    print("\n3. 按时间抽取FFT (DIT-FFT)")
    X_dit = dit_fft(x)
    print(f"   X_dit = {X_dit}")
    
    print("\n4. 按频率抽取FFT (DIF-FFT)")
    X_dif = dif_fft(x)
    print(f"   X_dif = {X_dif}")
    
    # 3. 迭代FFT
    print("\n5. 迭代实现FFT")
    X_iter = fft_iterative(x)
    print(f"   X_iter = {X_iter}")
    
    # 4. 与NumPy验证
    print("\n6. 与NumPy FFT比较")
    X_numpy = np.fft.fft(x)
    print(f"   X_numpy = {X_numpy}")
    print(f"   最大误差(DIT): {np.max(np.abs(X_dit - X_numpy)):.2e}")
    print(f"   最大误差(DIF): {np.max(np.abs(X_dif - X_numpy)):.2e}")
    print(f"   最大误差(Iter): {np.max(np.abs(X_iter - X_numpy)):.2e}")
    
    # 5. 逆DFT验证
    print("\n7. 逆DFT验证")
    x_reconstructed = idft_direct(X_dft)
    print(f"   重构信号: {np.real(x_reconstructed)}")
    print(f"   重构误差: {np.max(np.abs(x - np.real(x_reconstructed))):.2e}")
    
    # 6. 线性卷积
    print("\n8. 使用DFT计算线性卷积")
    x1 = np.array([1, 2, 3])
    x2 = np.array([1, 1, 1])
    y_dft = linear_convolution_dft(x1, x2)
    y_np = np.convolve(x1, x2)
    print(f"   x1 = {x1}")
    print(f"   x2 = {x2}")
    print(f"   线性卷积结果(DFT) = {y_dft}")
    print(f"   线性卷积结果(numpy) = {y_np}")
    
    # 7. 性能比较和频谱分析
    print("\n9. 性能比较和频谱分析...")
    plot_fft_comparison()


if __name__ == "__main__":
    demo()
