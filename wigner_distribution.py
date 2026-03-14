"""
Wigner-Ville分布时频分析
包含内容：
- 连续信号Wigner分布
- 离散信号Wigner分布
- 伪Wigner分布（加窗）
- Wigner分布性质分析
- 与STFT的比较
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import stft, windows


def wigner_ville_continuous_analog(signal, t, f):
    """
    连续信号Wigner-Ville分布（数值近似）
    
    公式: W(t,f) = ∫ x(t+τ/2) * x*(t-τ/2) * exp(-j*2*pi*f*τ) dτ
    
    参数:
        signal: 输入信号
        t: 时间数组
        f: 频率数组
    返回:
        W: Wigner分布矩阵
    """
    N = len(signal)
    M = len(f)
    dt = t[1] - t[0]
    
    W = np.zeros((M, N), dtype=complex)
    
    for n in range(N):
        for tau_idx, tau in enumerate(np.linspace(-t[-1], t[-1], min(2*n, 2*(N-n), 100))):
            if abs(tau) < dt:
                continue
            
            # 找到对应的信号索引
            idx1 = n + int(tau / (2 * dt))
            idx2 = n - int(tau / (2 * dt))
            
            if 0 <= idx1 < N and 0 <= idx2 < N:
                autocorr = signal[idx1] * np.conj(signal[idx2])
                for m, freq in enumerate(f):
                    W[m, n] += autocorr * np.exp(-1j * 2 * np.pi * freq * tau)
    
    return np.real(W)


def wigner_ville_discrete(x, nfft=None):
    """
    离散信号Wigner-Ville分布
    
    参数:
        x: 输入信号
        nfft: FFT点数
    返回:
        W: Wigner分布矩阵 (时间 x 频率)
        f: 频率数组
        t: 时间数组
    """
    N = len(x)
    if nfft is None:
        nfft = N
    
    # 确保nfft是偶数
    if nfft % 2 == 1:
        nfft += 1
    
    # Wigner分布
    W = np.zeros((nfft, N))
    
    for n in range(N):
        # 计算瞬时自相关函数
        for tau in range(-min(n, N-n-1), min(n, N-n-1) + 1):
            if tau == 0:
                R = x[n] * np.conj(x[n])
            else:
                idx1 = n + tau
                idx2 = n - tau
                if 0 <= idx1 < N and 0 <= idx2 < N:
                    R = x[idx1] * np.conj(x[idx2])
                else:
                    R = 0
            
            # 对自相关函数做FFT
            W[:, n] += R * np.exp(-1j * 2 * np.pi * tau * np.arange(nfft) / nfft)
    
    W = np.real(W)
    
    # 只保留正频率部分
    W = W[:nfft//2, :]
    f = np.arange(nfft//2) / nfft
    t = np.arange(N)
    
    return W, f, t


def pseudo_wigner_ville(x, window, nfft=None):
    """
    伪Wigner-Ville分布（加窗WVD）
    
    通过加窗减少交叉项干扰
    
    参数:
        x: 输入信号
        window: 窗函数
        nfft: FFT点数
    返回:
        W: 伪Wigner分布矩阵
        f: 频率数组
        t: 时间数组
    """
    N = len(x)
    L = len(window)
    if nfft is None:
        nfft = L
    
    W = np.zeros((nfft, N))
    
    for n in range(N):
        # 计算加窗的瞬时自相关
        for tau in range(-L//2, L//2):
            window_idx = tau + L//2
            if 0 <= window_idx < L:
                w = window[window_idx]
                idx1 = n + tau
                idx2 = n - tau
                if 0 <= idx1 < N and 0 <= idx2 < N:
                    R = x[idx1] * np.conj(x[idx2]) * w
                    W[:, n] += np.real(R * np.exp(-1j * 2 * np.pi * tau * np.arange(nfft) / nfft))
    
    W = np.real(W)
    
    # 只保留正频率
    W = W[:nfft//2, :]
    f = np.arange(nfft//2) / nfft
    t = np.arange(N)
    
    return W, f, t


def smoothed_pseudo_wigner_ville(x, time_window, freq_window, nfft=None):
    """
    平滑伪Wigner-Ville分布（SPWVD）
    
    同时在时间和频率方向加窗，进一步抑制交叉项
    
    参数:
        x: 输入信号
        time_window: 时间方向窗函数
        freq_window: 频率方向窗函数
        nfft: FFT点数
    返回:
        W: SPWVD矩阵
        f: 频率数组
        t: 时间数组
    """
    N = len(x)
    L_t = len(time_window)
    L_f = len(freq_window)
    
    if nfft is None:
        nfft = L_f
    
    # 首先计算伪WVD
    W_pseudo = np.zeros((nfft, N))
    
    for n in range(N):
        for tau in range(-L_t//2, L_t//2):
            window_idx = tau + L_t//2
            if 0 <= window_idx < L_t:
                w_t = time_window[window_idx]
                idx1 = n + tau
                idx2 = n - tau
                if 0 <= idx1 < N and 0 <= idx2 < N:
                    R = x[idx1] * np.conj(x[idx2]) * w_t
                    W_pseudo[:, n] += np.real(R * np.exp(-1j * 2 * np.pi * tau * np.arange(nfft) / nfft))
    
    # 在频率方向加窗平滑
    W = np.zeros((nfft, N))
    for k in range(nfft):
        for m in range(-L_f//2, L_f//2):
            window_idx = m + L_f//2
            if 0 <= window_idx < L_f:
                idx = (k - m) % nfft
                W[k, :] += W_pseudo[idx, :] * freq_window[window_idx]
    
    W = np.real(W)
    W = W[:nfft//2, :]
    f = np.arange(nfft//2) / nfft
    t = np.arange(N)
    
    return W, f, t


def analyze_wigner_properties():
    """
    分析Wigner分布的性质
    """
    N = 256
    t = np.linspace(0, 1, N)
    
    # 1. 实值性验证
    signal = np.sin(2 * np.pi * 10 * t)
    W, f, t_idx = wigner_ville_discrete(signal)
    is_real = np.allclose(W, np.real(W))
    
    # 2. 能量守恒验证
    energy_time = np.sum(np.abs(signal)**2)
    energy_wigner = np.sum(W) * (t[1]-t[0]) / N
    
    return is_real, energy_time, energy_wigner


def plot_time_frequency_comparison():
    """
    比较不同时频分析方法
    """
    np.random.seed(42)
    fs = 256
    t = np.linspace(0, 2, 2*fs)
    
    # 生成线性调频信号 + 恒定频率信号
    f0, f1 = 10, 50
    chirp_signal = np.sin(2 * np.pi * (f0 * t + (f1-f0) * t**2 / 4))
    constant_signal = np.sin(2 * np.pi * 30 * t)
    
    # 组合信号（有交叉项）
    combined_signal = chirp_signal + 0.5 * constant_signal
    # 添加噪声
    combined_signal += 0.1 * np.random.randn(len(t))
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. STFT
    ax = axes[0, 0]
    f_stft, t_stft, Zxx = stft(combined_signal, fs=fs, nperseg=64, noverlap=32)
    ax.pcolormesh(t_stft, f_stft, 20*np.log10(np.abs(Zxx)+1e-10), 
                   shading='gouraud', cmap='jet')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('STFT Spectrogram')
    ax.set_ylim([0, 100])
    
    # 2. Wigner-Ville分布
    ax = axes[0, 1]
    W, f_wvd, t_wvd = wigner_ville_discrete(combined_signal, nfft=256)
    # 限制频率范围
    freq_limit = int(len(f_wvd) * 100 / (fs/2))
    im = ax.pcolormesh(t_wvd/fs, f_wvd[:freq_limit]*fs, 
                       W[:freq_limit, :], 
                       shading='gouraud', cmap='jet')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Wigner-Ville Distribution')
    ax.set_ylim([0, 100])
    
    # 3. 伪Wigner-Ville分布
    ax = axes[1, 0]
    window = np.hamming(64)
    W_pwvd, f_pwvd, t_pwvd = pseudo_wigner_ville(combined_signal, window, nfft=256)
    im = ax.pcolormesh(t_pwvd/fs, f_pwvd[:freq_limit]*fs, 
                       W_pwvd[:freq_limit, :], 
                       shading='gouraud', cmap='jet')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Pseudo Wigner-Ville Distribution')
    ax.set_ylim([0, 100])
    
    # 4. 方法比较
    ax = axes[1, 1]
    
    # 在某个时间点比较
    t_slice = len(t) // 2
    
    # STFT切片
    stft_slice = np.abs(Zxx[:, len(Zxx[0])//2])
    
    # WVD切片
    wvd_slice = W[:, t_slice]
    
    # 伪WVD切片
    pwvd_slice = W_pwvd[:, t_slice]
    
    freq_stft = f_stft[f_stft < 100]
    ax.plot(freq_stft, 20*np.log10(stft_slice[:len(freq_stft)]+1e-10), 
            'b-', label='STFT', linewidth=2)
    ax.plot(f_wvd[:freq_limit]*fs, 10*np.log10(wvd_slice[:freq_limit]+1e-10), 
            'r--', label='WVD', linewidth=2)
    ax.plot(f_pwvd[:freq_limit]*fs, 10*np.log10(pwvd_slice[:freq_limit]+1e-10), 
            'g-.', label='Pseudo-WVD', linewidth=2)
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Frequency Slice Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 100])
    
    plt.tight_layout()
    plt.savefig('wigner_distribution.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'wigner_distribution.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("Wigner-Ville分布时频分析演示")
    print("=" * 60)
    
    # WVD性质介绍
    print("\n1. Wigner-Ville分布的主要性质")
    properties = [
        "实值性: W(t,f) 总是实数",
        "能量守恒: ∬W(t,f)dtdf = ∫|x(t)|²dt",
        "边缘特性: ∫W(t,f)df = |x(t)|², ∫W(t,f)dt = |X(f)|²",
        "时移和频移: 信号时移/频移对应WVD相应移动",
        "交叉项: 多分量信号会产生交叉项干扰"
    ]
    for prop in properties:
        print(f"   - {prop}")
    
    # 性质验证
    print("\n2. 性质验证")
    is_real, energy_time, energy_wigner = analyze_wigner_properties()
    print(f"   实值性: {'满足' if is_real else '不满足'}")
    print(f"   时域能量: {energy_time:.4f}")
    print(f"   Wigner域能量: {energy_wigner:.4f}")
    print(f"   能量守恒: {'满足' if np.isclose(energy_time, energy_wigner, rtol=0.1) else '近似'}")
    
    # 单分量信号分析
    print("\n3. 单分量信号Wigner分布")
    N = 128
    t = np.linspace(0, 1, N)
    signal = np.sin(2 * np.pi * 10 * t)
    W, f, t_idx = wigner_ville_discrete(signal, nfft=128)
    
    peak_idx = np.unravel_index(np.argmax(W), W.shape)
    peak_freq = f[peak_idx[0]] * N
    print(f"   信号频率: 10 Hz")
    print(f"   WVD峰值频率: {peak_freq:.1f}")
    
    # 交叉项分析
    print("\n4. 交叉项分析")
    print("   当信号包含多个分量时，WVD会产生交叉项")
    print("   交叉项位于各分量时频中心的中点")
    print("   伪WVD通过加窗可以抑制交叉项")
    
    # 绘制时频分析比较
    print("\n5. 绘制时频分析比较图...")
    plot_time_frequency_comparison()


if __name__ == "__main__":
    demo()
