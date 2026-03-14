"""
离散余弦变换(DCT)与离散正弦变换(DST)实现
包含内容：
- DCT-I, DCT-II, DCT-III, DCT-IV
- DST变换
- DCT快速算法
- 图像压缩应用示例
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct


def dct_ii_direct(x):
    """
    直接计算DCT-II（最常用的DCT类型）
    
    公式: X[k] = sum_{n=0}^{N-1} x[n] * cos(pi/N * (n+0.5) * k)
    
    参数:
        x: 输入序列
    返回:
        X: DCT-II系数
    """
    N = len(x)
    X = np.zeros(N)
    
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.cos(np.pi / N * (n + 0.5) * k)
    
    return X


def idct_ii_direct(X):
    """
    直接计算DCT-III（DCT-II的逆变换）
    
    参数:
        X: DCT系数
    返回:
        x: 重构序列
    """
    N = len(X)
    x = np.zeros(N)
    
    for n in range(N):
        x[n] += X[0] / 2  # k=0项特殊处理
        for k in range(1, N):
            x[n] += X[k] * np.cos(np.pi / N * (n + 0.5) * k)
    
    return x * 2 / N


def dct_via_fft(x):
    """
    使用FFT快速计算DCT-II
    
    利用DCT与DFT的关系进行快速计算
    
    参数:
        x: 输入序列
    返回:
        X: DCT-II系数
    """
    N = len(x)
    
    # 构造对称延拓序列
    y = np.zeros(2 * N)
    y[:N] = x
    y[N:] = x[::-1]
    
    # 计算FFT并取实部
    Y = np.fft.fft(y)
    
    # 提取DCT系数
    X = np.real(Y[:N]) * np.exp(-1j * np.pi * np.arange(N) / (2 * N))
    
    return np.real(X)


def dct_2d(x):
    """
    二维DCT变换
    
    参数:
        x: 输入二维数组
    返回:
        X: DCT系数
    """
    # 先对行做DCT
    X = dct(x, type=2, norm='ortho', axis=0)
    # 再对列做DCT
    X = dct(X, type=2, norm='ortho', axis=1)
    return X


def idct_2d(X):
    """
    二维IDCT变换
    """
    # 先对行做IDCT
    x = idct(X, type=2, norm='ortho', axis=0)
    # 再对列做IDCT
    x = idct(x, type=2, norm='ortho', axis=1)
    return x


def dst_ii_direct(x):
    """
    直接计算DST-II（离散正弦变换）
    
    公式: X[k] = sum_{n=0}^{N-1} x[n] * sin(pi/N * (n+0.5) * (k+1))
    
    参数:
        x: 输入序列
    返回:
        X: DST-II系数
    """
    N = len(x)
    X = np.zeros(N)
    
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.sin(np.pi / N * (n + 0.5) * (k + 1))
    
    return X


def dct_compression_1d(x, keep_ratio=0.5):
    """
    基于DCT的一维信号压缩
    
    参数:
        x: 输入信号
        keep_ratio: 保留的系数比例
    返回:
        x_reconstructed: 重构信号
        compression_ratio: 实际压缩比
    """
    N = len(x)
    
    # DCT变换
    X = dct(x, type=2, norm='ortho')
    
    # 保留前keep_ratio个系数
    keep_count = int(N * keep_ratio)
    X_compressed = np.zeros_like(X)
    X_compressed[:keep_count] = X[:keep_count]
    
    # IDCT重构
    x_reconstructed = idct(X_compressed, type=2, norm='ortho')
    
    # 计算压缩比
    compression_ratio = N / keep_count
    
    return x_reconstructed, compression_ratio


def dct_compression_2d(image, keep_ratio=0.1):
    """
    基于DCT的二维图像压缩（类似JPEG原理）
    
    参数:
        image: 输入图像（灰度）
        keep_ratio: 保留的系数比例
    返回:
        image_reconstructed: 重构图像
        mse: 均方误差
    """
    # DCT变换
    X = dct_2d(image)
    
    # 按幅度排序，保留最大的keep_ratio比例系数
    threshold = np.percentile(np.abs(X), (1 - keep_ratio) * 100)
    X_compressed = X * (np.abs(X) >= threshold)
    
    # IDCT重构
    image_reconstructed = idct_2d(X_compressed)
    
    # 计算MSE
    mse = np.mean((image - image_reconstructed) ** 2)
    
    return image_reconstructed, mse


def plot_dct_analysis():
    """
    绘制DCT分析图
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 1. DCT基函数
    ax = axes[0, 0]
    N = 64
    x = np.zeros(N)
    for k in range(5):
        basis = np.cos(np.pi / N * (np.arange(N) + 0.5) * k)
        ax.plot(basis, label=f'k={k}')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    ax.set_title('DCT-II Basis Functions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 信号DCT变换示例
    ax = axes[0, 1]
    t = np.linspace(0, 1, N)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 15 * t)
    X_dct = dct(signal, type=2, norm='ortho')
    ax.stem(np.arange(N), np.abs(X_dct), basefmt=' ')
    ax.set_xlabel('Frequency Index')
    ax.set_ylabel('DCT Coefficient')
    ax.set_title('DCT Coefficients of Test Signal')
    ax.grid(True, alpha=0.3)
    
    # 3. 压缩效果比较
    ax = axes[0, 2]
    compression_ratios = [0.1, 0.2, 0.5, 0.8]
    mses = []
    for ratio in compression_ratios:
        x_recon, _ = dct_compression_1d(signal, ratio)
        mse = np.mean((signal - x_recon) ** 2)
        mses.append(mse)
    ax.bar(range(len(compression_ratios)), mses)
    ax.set_xticks(range(len(compression_ratios)))
    ax.set_xticklabels([f'{r*100:.0f}%' for r in compression_ratios])
    ax.set_xlabel('Coefficients Retained')
    ax.set_ylabel('MSE')
    ax.set_title('Compression vs Error')
    ax.grid(True, alpha=0.3)
    
    # 4. 信号重构比较
    ax = axes[1, 0]
    ax.plot(t, signal, 'b-', label='Original', linewidth=2)
    for ratio, color in zip([0.2, 0.5], ['r', 'g']):
        x_recon, _ = dct_compression_1d(signal, ratio)
        ax.plot(t, x_recon, color, label=f'{ratio*100:.0f}% coeffs', alpha=0.7)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Signal Reconstruction')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 5. 2D DCT基图像
    ax = axes[1, 1]
    basis_2d = np.zeros((8, 8))
    u, v = 2, 3
    for i in range(8):
        for j in range(8):
            basis_2d[i, j] = np.cos(np.pi / 8 * (i + 0.5) * u) * \
                            np.cos(np.pi / 8 * (j + 0.5) * v)
    im = ax.imshow(basis_2d, cmap='gray')
    ax.set_title(f'2D DCT Basis (u={u}, v={v})')
    plt.colorbar(im, ax=ax)
    
    # 6. 能量压缩特性
    ax = axes[1, 2]
    X_sorted = np.sort(np.abs(X_dct))[::-1]
    energy_cumulative = np.cumsum(X_sorted**2) / np.sum(X_sorted**2)
    ax.plot(np.arange(1, len(energy_cumulative)+1) / len(energy_cumulative), 
            energy_cumulative, linewidth=2)
    ax.axhline(y=0.95, color='r', linestyle='--', label='95% Energy')
    ax.axvline(x=np.where(energy_cumulative >= 0.95)[0][0] / len(energy_cumulative),
               color='r', linestyle='--')
    ax.set_xlabel('Fraction of Coefficients')
    ax.set_ylabel('Cumulative Energy')
    ax.set_title('Energy Compaction Property')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('dct_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'dct_analysis.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("离散余弦变换(DCT)与离散正弦变换(DST)演示")
    print("=" * 60)
    
    # 1. DCT变换类型介绍
    print("\n1. DCT变换类型")
    dct_types = {
        "DCT-I": "常用于数据插值",
        "DCT-II": "最常用，JPEG图像压缩使用",
        "DCT-III": "DCT-II的逆变换",
        "DCT-IV": "用于快速DCT算法"
    }
    for name, usage in dct_types.items():
        print(f"   {name}: {usage}")
    
    # 2. 一维DCT计算
    print("\n2. 一维DCT-II计算")
    N = 8
    x = np.array([1, 2, 3, 4, 3, 2, 1, 0], dtype=float)
    print(f"   输入序列: {x}")
    
    # 直接计算
    X_direct = dct_ii_direct(x)
    print(f"   DCT直接计算: {X_direct}")
    
    # 使用scipy
    X_scipy = dct(x, type=2, norm='ortho')
    print(f"   DCT (scipy): {X_scipy}")
    
    # 逆变换
    x_recon = idct(X_scipy, type=2, norm='ortho')
    print(f"   IDCT重构: {x_recon}")
    print(f"   重构误差: {np.max(np.abs(x - x_recon)):.2e}")
    
    # 3. DST变换
    print("\n3. 离散正弦变换(DST)")
    X_dst = dst_ii_direct(x)
    print(f"   DST-II结果: {X_dst}")
    
    # 4. 能量压缩特性
    print("\n4. DCT的能量压缩特性")
    signal = np.random.randn(128)
    signal = np.sin(2 * np.pi * 5 * np.arange(128) / 128) + 0.1 * signal
    X_dct = dct(signal, type=2, norm='ortho')
    
    # 计算前10%系数保留的能量
    X_top10 = np.zeros_like(X_dct)
    top_indices = np.argsort(np.abs(X_dct))[-13:]  # 前10%
    X_top10[top_indices] = X_dct[top_indices]
    signal_top10 = idct(X_top10, type=2, norm='ortho')
    
    energy_original = np.sum(signal**2)
    energy_top10 = np.sum(signal_top10**2)
    print(f"   原始信号能量: {energy_original:.4f}")
    print(f"   前10%系数重构能量: {energy_top10:.4f}")
    print(f"   能量保留比例: {energy_top10/energy_original*100:.2f}%")
    
    # 5. 信号压缩
    print("\n5. 基于DCT的信号压缩")
    for ratio in [0.1, 0.3, 0.5]:
        _, compression_ratio = dct_compression_1d(signal, ratio)
        print(f"   保留{ratio*100:.0f}%系数 -> 压缩比: {compression_ratio:.1f}:1")
    
    # 绘制分析图
    print("\n6. 绘制DCT分析图...")
    plot_dct_analysis()


if __name__ == "__main__":
    demo()
