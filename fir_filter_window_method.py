"""
FIR滤波器设计 - 窗函数法
包含内容：
- 常用窗函数（矩形窗、汉宁窗、汉明窗、布莱克曼窗、凯泽窗）
- 窗函数法设计FIR低通、高通、带通、带阻滤波器
- 滤波器性能分析
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, firwin, kaiserord


def rectangular_window(N):
    """矩形窗"""
    return np.ones(N)


def hanning_window(N):
    """汉宁窗 (Hanning Window)"""
    n = np.arange(N)
    return 0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1))


def hamming_window(N):
    """汉明窗 (Hamming Window)"""
    n = np.arange(N)
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))


def blackman_window(N):
    """布莱克曼窗 (Blackman Window)"""
    n = np.arange(N)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))


def kaiser_window(N, beta):
    """
    凯泽窗 (Kaiser Window)
    
    参数:
        N: 窗长度
        beta: 形状参数
    """
    from scipy.special import i0
    n = np.arange(N)
    alpha = (N - 1) / 2
    temp = beta * np.sqrt(1 - ((n - alpha) / alpha) ** 2)
    return i0(temp) / i0(beta)


def fir_lowpass_window(fc, N, window_type='hamming', beta=8.6):
    """
    使用窗函数法设计FIR低通滤波器
    
    参数:
        fc: 截止频率（归一化，0到1，1对应Nyquist频率）
        N: 滤波器阶数（奇数）
        window_type: 窗函数类型
        beta: 凯泽窗参数
    返回:
        h: 滤波器系数
    """
    if N % 2 == 0:
        N += 1  # 确保N为奇数
    
    # 理想低通滤波器的单位脉冲响应
    n = np.arange(N)
    alpha = (N - 1) / 2
    h_ideal = np.sinc(2 * fc * (n - alpha))
    
    # 选择窗函数
    if window_type == 'rectangular':
        w = rectangular_window(N)
    elif window_type == 'hanning':
        w = hanning_window(N)
    elif window_type == 'hamming':
        w = hamming_window(N)
    elif window_type == 'blackman':
        w = blackman_window(N)
    elif window_type == 'kaiser':
        w = kaiser_window(N, beta)
    else:
        raise ValueError(f"Unknown window type: {window_type}")
    
    # 加窗
    h = h_ideal * w
    
    return h


def fir_highpass_window(fc, N, window_type='hamming'):
    """
    使用窗函数法设计FIR高通滤波器
    
    参数:
        fc: 截止频率
        N: 滤波器阶数（奇数）
        window_type: 窗函数类型
    返回:
        h: 滤波器系数
    """
    # 高通 = 全通 - 低通
    h_lp = fir_lowpass_window(fc, N, window_type)
    h_hp = -h_lp
    h_hp[(N - 1) // 2] += 1  # 加上delta函数
    return h_hp


def fir_bandpass_window(fl, fh, N, window_type='hamming'):
    """
    使用窗函数法设计FIR带通滤波器
    
    参数:
        fl, fh: 下、上截止频率
        N: 滤波器阶数
        window_type: 窗函数类型
    返回:
        h: 滤波器系数
    """
    # 带通 = 高通(fl) * 低通(fh) = 两个低通的差
    h_lp1 = fir_lowpass_window(fh, N, window_type)
    h_lp2 = fir_lowpass_window(fl, N, window_type)
    return h_lp1 - h_lp2


def fir_bandstop_window(fl, fh, N, window_type='hamming'):
    """
    使用窗函数法设计FIR带阻滤波器
    
    参数:
        fl, fh: 下、上截止频率
        N: 滤波器阶数
        window_type: 窗函数类型
    返回:
        h: 滤波器系数
    """
    # 带阻 = 全通 - 带通
    h_bp = fir_bandpass_window(fl, fh, N, window_type)
    h_bs = -h_bp
    h_bs[(N - 1) // 2] += 1
    return h_bs


def analyze_filter(h, fs=1.0):
    """
    分析滤波器特性
    
    参数:
        h: 滤波器系数
        fs: 采样频率
    返回:
        分析结果字典
    """
    w, H = freqz(h, worN=8000)
    f = w * fs / (2 * np.pi)
    
    # 转换为dB
    H_db = 20 * np.log10(np.abs(H) + 1e-10)
    
    return {
        'frequency': f,
        'magnitude': np.abs(H),
        'magnitude_db': H_db,
        'phase': np.angle(H)
    }


def plot_window_comparison():
    """
    比较不同窗函数的特性
    """
    N = 51
    windows = {
        'Rectangular': rectangular_window(N),
        'Hanning': hanning_window(N),
        'Hamming': hamming_window(N),
        'Blackman': blackman_window(N),
        'Kaiser (β=8.6)': kaiser_window(N, 8.6)
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 时域波形
    ax = axes[0, 0]
    n = np.arange(N)
    for name, w in windows.items():
        ax.plot(n, w, label=name, linewidth=2)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude')
    ax.set_title('Window Functions in Time Domain')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 频域幅度响应
    ax = axes[0, 1]
    for name, w in windows.items():
        w_padded = np.pad(w, (0, 4096 - N))
        W = np.fft.fftshift(np.fft.fft(w_padded))
        W_db = 20 * np.log10(np.abs(W) + 1e-10)
        freqs = np.linspace(-0.5, 0.5, len(W_db))
        ax.plot(freqs, W_db - np.max(W_db), label=name, linewidth=2)
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Window Functions in Frequency Domain')
    ax.set_ylim([-100, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. 低通滤波器设计比较
    ax = axes[1, 0]
    fc = 0.25
    for name, window_func in [
        ('Rectangular', lambda N: rectangular_window(N)),
        ('Hanning', lambda N: hanning_window(N)),
        ('Hamming', lambda N: hamming_window(N)),
        ('Blackman', lambda N: blackman_window(N))
    ]:
        h = fir_lowpass_window(fc, N, name.lower().replace(' (β=8.6)', ''))
        result = analyze_filter(h)
        ax.plot(result['frequency'], result['magnitude_db'], 
                label=f'{name} (N={N})', linewidth=2)
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Lowpass Filter Design Comparison (fc=0.25)')
    ax.set_ylim([-100, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. 不同阶数的比较（汉明窗）
    ax = axes[1, 1]
    orders = [21, 41, 61]
    for order in orders:
        h = fir_lowpass_window(fc, order, 'hamming')
        result = analyze_filter(h)
        ax.plot(result['frequency'], result['magnitude_db'], 
                label=f'N={order}', linewidth=2)
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Effect of Filter Order (Hamming Window)')
    ax.set_ylim([-100, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fir_filter_windows.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'fir_filter_windows.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("FIR滤波器设计 - 窗函数法演示")
    print("=" * 60)
    
    # 1. 窗函数介绍
    print("\n1. 常用窗函数及其特性")
    windows_info = {
        "矩形窗": "主瓣宽度: 4π/N, 旁瓣衰减: -13 dB",
        "汉宁窗": "主瓣宽度: 8π/N, 旁瓣衰减: -31 dB",
        "汉明窗": "主瓣宽度: 8π/N, 旁瓣衰减: -41 dB",
        "布莱克曼窗": "主瓣宽度: 12π/N, 旁瓣衰减: -57 dB",
        "凯泽窗": "可调参数β，在主瓣宽度和旁瓣衰减之间折中"
    }
    for name, info in windows_info.items():
        print(f"   {name}: {info}")
    
    # 2. 设计低通滤波器
    print("\n2. 设计FIR低通滤波器")
    N = 51
    fc = 0.25  # 归一化截止频率
    
    h_rect = fir_lowpass_window(fc, N, 'rectangular')
    h_hamm = fir_lowpass_window(fc, N, 'hamming')
    h_blck = fir_lowpass_window(fc, N, 'blackman')
    
    print(f"   滤波器阶数: {N}")
    print(f"   截止频率: {fc} (归一化)")
    print(f"   矩形窗系数 (前10个): {h_rect[:10]}")
    print(f"   汉明窗系数 (前10个): {h_hamm[:10]}")
    
    # 3. 设计高通滤波器
    print("\n3. 设计FIR高通滤波器")
    h_hp = fir_highpass_window(0.3, N, 'hamming')
    print(f"   截止频率: 0.3")
    print(f"   滤波器系数 (前10个): {h_hp[:10]}")
    
    # 4. 设计带通滤波器
    print("\n4. 设计FIR带通滤波器")
    h_bp = fir_bandpass_window(0.2, 0.4, N, 'hamming')
    print(f"   通带范围: 0.2 - 0.4")
    print(f"   滤波器系数 (前10个): {h_bp[:10]}")
    
    # 5. 滤波器分析
    print("\n5. 滤波器频率响应分析")
    result = analyze_filter(h_hamm)
    print(f"   最大增益: {np.max(result['magnitude_db']):.2f} dB")
    print(f"   阻带最小衰减: {np.min(result['magnitude_db']):.2f} dB")
    
    # 6. 滤波器应用示例
    print("\n6. 滤波器应用示例")
    # 构造测试信号
    t = np.linspace(0, 1, 1000)
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 200 * t)
    
    # 使用设计的低通滤波器（假设采样率1000Hz）
    from scipy.signal import lfilter
    filtered = lfilter(h_hamm, 1, signal)
    
    print(f"   原始信号: 50Hz + 200Hz 正弦波")
    print(f"   低通滤波器截止频率: {fc * 500}Hz")
    print(f"   滤波后信号能量比: {np.sum(filtered**2) / np.sum(signal**2):.4f}")
    
    # 绘制比较图
    print("\n7. 绘制窗函数和滤波器比较图...")
    plot_window_comparison()


if __name__ == "__main__":
    demo()
