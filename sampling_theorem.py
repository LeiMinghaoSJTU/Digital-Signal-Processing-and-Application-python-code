"""
采样定理与信号重构实现
包含内容：
- 采样过程模拟
- 采样定理验证
- 理想重构
- 零阶保持重构
- 抗混叠滤波
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, resample


def continuous_signal(t, frequencies, amplitudes):
    """
    生成连续时间信号（多个正弦波的叠加）
    
    参数:
        t: 时间数组
        frequencies: 频率列表
        amplitudes: 振幅列表
    返回:
        x: 信号值
    """
    x = np.zeros_like(t)
    for f, A in zip(frequencies, amplitudes):
        x += A * np.sin(2 * np.pi * f * t)
    return x


def sample_signal(x_continuous, t_continuous, fs):
    """
    对连续信号进行采样
    
    参数:
        x_continuous: 连续信号值
        t_continuous: 连续时间
        fs: 采样频率
    返回:
        x_sampled: 采样值
        t_sampled: 采样时间
    """
    dt = 1 / fs
    t_sampled = np.arange(t_continuous[0], t_continuous[-1], dt)
    x_sampled = np.interp(t_sampled, t_continuous, x_continuous)
    return x_sampled, t_sampled


def ideal_reconstruction(x_sampled, t_sampled, t_reconstruct, fs):
    """
    使用sinc函数进行理想重构
    
    公式: x_r(t) = sum_{n=-∞}^{∞} x[n] * sinc((t-nT)/T)
    
    参数:
        x_sampled: 采样值
        t_sampled: 采样时间
        t_reconstruct: 重构时间点
        fs: 采样频率
    返回:
        x_reconstructed: 重构信号
    """
    T = 1 / fs
    x_reconstructed = np.zeros_like(t_reconstruct)
    
    for n, (t_n, x_n) in enumerate(zip(t_sampled, x_sampled)):
        x_reconstructed += x_n * np.sinc((t_reconstruct - t_n) / T)
    
    return x_reconstructed


def zero_order_hold(x_sampled, t_sampled, t_reconstruct):
    """
    零阶保持重构
    
    参数:
        x_sampled: 采样值
        t_sampled: 采样时间
        t_reconstruct: 重构时间点
    返回:
        x_reconstructed: 重构信号
    """
    x_reconstructed = np.zeros_like(t_reconstruct)
    
    for i, t in enumerate(t_reconstruct):
        # 找到最近的采样点
        idx = np.argmin(np.abs(t_sampled - t))
        # 找到实际的前一个采样点
        valid_indices = np.where(t_sampled <= t)[0]
        if len(valid_indices) > 0:
            idx = valid_indices[-1]
            x_reconstructed[i] = x_sampled[idx]
    
    return x_reconstructed


def first_order_hold(x_sampled, t_sampled, t_reconstruct):
    """
    一阶保持（线性插值）重构
    
    参数:
        x_sampled: 采样值
        t_sampled: 采样时间
        t_reconstruct: 重构时间点
    返回:
        x_reconstructed: 重构信号
    """
    return np.interp(t_reconstruct, t_sampled, x_sampled)


def anti_aliasing_filter(x, fs, cutoff):
    """
    抗混叠滤波器
    
    在采样前对信号进行低通滤波，防止混叠
    
    参数:
        x: 输入信号
        fs: 采样频率
        cutoff: 截止频率
    返回:
        x_filtered: 滤波后信号
    """
    # 设计巴特沃斯低通滤波器
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist
    b, a = butter(6, normalized_cutoff, btype='low')
    
    # 零相位滤波
    x_filtered = filtfilt(b, a, x)
    
    return x_filtered


def quantize_signal(x, n_bits):
    """
    信号量化（A/D转换）
    
    参数:
        x: 输入信号
        n_bits: 量化位数
    返回:
        x_quantized: 量化后信号
        quantization_step: 量化步长
    """
    # 确定信号范围
    x_max = np.max(x)
    x_min = np.min(x)
    
    # 量化电平数
    L = 2 ** n_bits
    
    # 量化步长
    delta = (x_max - x_min) / L
    
    # 量化
    x_normalized = (x - x_min) / delta
    x_quantized = np.round(x_normalized) * delta + x_min
    
    return x_quantized, delta


def analyze_sampling_theorem():
    """
    分析采样定理
    验证奈奎斯特准则
    """
    # 生成测试信号
    f_max = 20  # 信号最高频率
    t_fine = np.linspace(0, 1, 10000)  # 高分辨率时间
    
    # 信号包含20Hz和5Hz分量
    x_continuous = np.sin(2 * np.pi * 20 * t_fine) + 0.5 * np.sin(2 * np.pi * 5 * t_fine)
    
    # 不同采样频率
    sampling_rates = [15, 25, 40, 100]  # Hz
    
    results = []
    for fs in sampling_rates:
        x_sampled, t_sampled = sample_signal(x_continuous, t_fine, fs)
        
        # 重构
        x_reconstructed = ideal_reconstruction(x_sampled, t_sampled, t_fine, fs)
        
        # 计算重构误差
        mse = np.mean((x_continuous - x_reconstructed)**2)
        
        results.append({
            'fs': fs,
            'nyquist_ratio': fs / (2 * f_max),
            'sampled': (t_sampled, x_sampled),
            'reconstructed': x_reconstructed,
            'mse': mse,
            'is_adequate': fs >= 2 * f_max
        })
    
    return t_fine, x_continuous, results


def plot_sampling_analysis():
    """
    绘制采样定理分析图
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 采样过程演示
    ax = axes[0, 0]
    t_fine = np.linspace(0, 0.5, 1000)
    f_signal = 10
    x_continuous = np.sin(2 * np.pi * f_signal * t_fine)
    
    # 不同采样频率
    for fs, color in [(15, 'red'), (25, 'green'), (50, 'blue')]:
        x_sampled, t_sampled = sample_signal(x_continuous, t_fine, fs)
        ax.scatter(t_sampled, x_sampled, color=color, s=30, 
                   label=f'fs={fs}Hz (fs/f={fs/f_signal:.1f})', zorder=3)
    
    ax.plot(t_fine, x_continuous, 'k-', alpha=0.3, label='Original', linewidth=2)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Sampling at Different Rates')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 混叠现象
    ax = axes[0, 1]
    t_fine = np.linspace(0, 1, 2000)
    f_high = 25  # 高频信号
    x_high_freq = np.sin(2 * np.pi * f_high * t_fine)
    
    # 欠采样
    fs_low = 30  # 低于奈奎斯特频率
    x_aliased, t_aliased = sample_signal(x_high_freq, t_fine, fs_low)
    
    # 重构的低频信号（混叠结果）
    f_alias = abs(f_high - fs_low)  # 混叠频率
    x_alias_signal = np.sin(2 * np.pi * f_alias * t_fine)
    
    ax.plot(t_fine, x_high_freq, 'b-', alpha=0.5, label=f'Original ({f_high}Hz)', linewidth=2)
    ax.scatter(t_aliased, x_aliased, color='red', s=40, label=f'Sampled (fs={fs_low}Hz)', zorder=3)
    ax.plot(t_fine, x_alias_signal, 'g--', label=f'Aliased ({f_alias}Hz)', linewidth=2)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Aliasing Effect (fs < 2*f_max)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. 重构方法比较
    ax = axes[1, 0]
    fs = 50
    t_fine = np.linspace(0, 0.5, 1000)
    x_continuous = np.sin(2 * np.pi * 5 * t_fine) + 0.3 * np.sin(2 * np.pi * 15 * t_fine)
    
    x_sampled, t_sampled = sample_signal(x_continuous, t_fine, fs)
    
    # 不同重构方法
    x_ideal = ideal_reconstruction(x_sampled, t_sampled, t_fine, fs)
    x_zoh = zero_order_hold(x_sampled, t_sampled, t_fine)
    x_foh = first_order_hold(x_sampled, t_sampled, t_fine)
    
    ax.plot(t_fine, x_continuous, 'k-', alpha=0.5, label='Original', linewidth=2)
    ax.plot(t_fine, x_ideal, 'b--', label='Ideal (Sinc)', linewidth=1.5)
    ax.plot(t_fine, x_zoh, 'r-.', label='Zero-Order Hold', linewidth=1.5)
    ax.plot(t_fine, x_foh, 'g:', label='Linear', linewidth=1.5)
    ax.scatter(t_sampled, x_sampled, color='purple', s=40, zorder=5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Reconstruction Methods Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0.1, 0.3])
    
    # 4. 抗混叠滤波效果
    ax = axes[1, 1]
    t_fine = np.linspace(0, 1, 2000)
    
    # 高频信号
    x_high = np.sin(2 * np.pi * 30 * t_fine) + 0.5 * np.sin(2 * np.pi * 60 * t_fine)
    
    fs = 80  # 采样频率
    
    # 无抗混叠滤波
    x_sampled_no_aa, t_sampled_no_aa = sample_signal(x_high, t_fine, fs)
    
    # 有抗混叠滤波
    x_filtered = anti_aliasing_filter(x_high, fs, cutoff=35)
    x_sampled_aa, t_sampled_aa = sample_signal(x_filtered, t_fine, fs)
    
    # 重构
    x_recon_no_aa = ideal_reconstruction(x_sampled_no_aa, t_sampled_no_aa, t_fine, fs)
    x_recon_aa = ideal_reconstruction(x_sampled_aa, t_sampled_aa, t_fine, fs)
    
    ax.plot(t_fine, x_high, 'b-', alpha=0.3, label='Original (30Hz+60Hz)', linewidth=2)
    ax.plot(t_fine, x_recon_no_aa, 'r--', alpha=0.7, label='No Anti-Aliasing', linewidth=1.5)
    ax.plot(t_fine, x_recon_aa, 'g-', label='With Anti-Aliasing', linewidth=1.5)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Effect of Anti-Aliasing Filter')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sampling_theorem.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'sampling_theorem.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("采样定理与信号重构演示")
    print("=" * 60)
    
    # 采样定理介绍
    print("\n1. 采样定理（奈奎斯特-香农定理）")
    print("   如果一个连续信号x(t)的最高频率为f_max，")
    print("   那么采样频率fs必须满足: fs ≥ 2*f_max")
    print("   才能无失真地从采样中恢复原信号")
    print("   其中，2*f_max称为奈奎斯特频率，f_max称为奈奎斯特率")
    
    # 验证采样定理
    print("\n2. 采样定理验证")
    t_fine, x_continuous, results = analyze_sampling_theorem()
    
    for result in results:
        fs = result['fs']
        ratio = result['nyquist_ratio']
        mse = result['mse']
        adequate = "满足" if result['is_adequate'] else "不满足"
        
        print(f"   采样频率 fs = {fs}Hz")
        print(f"   fs/(2*f_max) = {ratio:.2f} ({adequate}采样定理)")
        print(f"   重构均方误差: {mse:.6f}")
        print()
    
    # 混叠现象
    print("3. 混叠现象")
    print("   当 fs < 2*f_max 时，高频分量会'折叠'到低频区域")
    print("   混叠频率: f_alias = |f - k*fs|，其中k为整数")
    print("   例如: f=25Hz, fs=30Hz -> f_alias = |25-30| = 5Hz")
    
    # 重构方法
    print("\n4. 信号重构方法")
    methods = {
        "理想重构（Sinc插值）": "理论上完美的重构，但计算量大",
        "零阶保持（ZOH）": "简单硬件实现，有阶梯状失真",
        "一阶保持（线性插值）": "比ZOH平滑，计算简单"
    }
    for name, desc in methods.items():
        print(f"   {name}: {desc}")
    
    # 量化
    print("\n5. A/D转换中的量化")
    n_bits_list = [4, 8, 12]
    x_test = np.sin(2 * np.pi * np.linspace(0, 1, 1000))
    
    for n_bits in n_bits_list:
        x_quantized, delta = quantize_signal(x_test, n_bits)
        snr = 6.02 * n_bits + 1.76  # 理论SNR公式
        print(f"   {n_bits}位量化: 量化步长={delta:.6f}, 理论SNR≈{snr:.1f}dB")
    
    # 绘制分析图
    print("\n6. 绘制采样定理分析图...")
    plot_sampling_analysis()


if __name__ == "__main__":
    demo()
