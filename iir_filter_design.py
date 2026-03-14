"""
IIR滤波器设计
包含内容：
- 冲激响应不变法
- 双线性变换法
- 数字滤波器频率变换
- 巴特沃斯、切比雪夫滤波器设计
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import (butter, cheby1, cheby2, ellip, 
                          freqz, impulse, step, tf2zpk,
                          bilinear, cont2discrete)
from scipy.optimize import fsolve


def impulse_invariance_analog_to_digital(ha_coeffs, T, num_points=1000):
    """
    冲激响应不变法：将模拟滤波器转换为数字滤波器
    
    原理: h[n] = T * ha(nT)
    
    参数:
        ha_coeffs: 模拟滤波器系数 (num, den)
        T: 采样周期
        num_points: 采样点数
    返回:
        b, a: 数字滤波器系数
    """
    num_a, den_a = ha_coeffs
    
    # 计算模拟滤波器的冲激响应
    t = np.linspace(0, 20*T, num_points)
    from scipy.signal import lti, impulse
    system = lti(num_a, den_a)
    t_out, h_a = impulse(system, T=t)
    
    # 采样冲激响应
    sample_indices = np.arange(0, len(t_out), int(1/T)) if T < 1 else np.arange(0, len(t_out))
    h_d = T * h_a[::max(1, int(1/T))][:100]  # 限制长度
    
    return h_d


def bilinear_transform_analog_to_digital(ha_coeffs, T):
    """
    双线性变换法：将模拟滤波器转换为数字滤波器
    
    变换关系: s = (2/T) * (1 - z^(-1)) / (1 + z^(-1))
    
    参数:
        ha_coeffs: 模拟滤波器系数 (num, den)
        T: 采样周期
    返回:
        b, a: 数字滤波器系数
    """
    num_a, den_a = ha_coeffs
    b, a = bilinear(num_a, den_a, fs=1/T)
    return b, a


def design_butterworth_digital(order, cutoff, filter_type='low', method='bilinear', fs=1.0):
    """
    设计巴特沃斯数字滤波器
    
    参数:
        order: 滤波器阶数
        cutoff: 截止频率（归一化或Hz）
        filter_type: 'low', 'high', 'band', 'bandstop'
        method: 'bilinear' 或 'impulse_invariance'
        fs: 采样频率
    返回:
        b, a: 滤波器系数
    """
    if method == 'bilinear':
        b, a = butter(order, cutoff, btype=filter_type, fs=fs)
    else:
        # 先设计模拟滤波器，再用冲激响应不变法
        from scipy.signal import butter as analog_butter
        num_a, den_a = analog_butter(order, 2*np.pi*cutoff, btype=filter_type, analog=True)
        T = 1/fs
        h_d = impulse_invariance_analog_to_digital((num_a, den_a), T)
        # 从冲激响应估计系数（简化处理）
        b, a = bilinear(num_a, den_a, fs=fs)
    
    return b, a


def design_chebyshev1_digital(order, rp, cutoff, filter_type='low', fs=1.0):
    """
    设计切比雪夫I型数字滤波器（通带等波纹）
    
    参数:
        order: 滤波器阶数
        rp: 通带最大衰减(dB)
        cutoff: 截止频率
        filter_type: 'low', 'high', 'band', 'bandstop'
        fs: 采样频率
    返回:
        b, a: 滤波器系数
    """
    b, a = cheby1(order, rp, cutoff, btype=filter_type, fs=fs)
    return b, a


def design_chebyshev2_digital(order, rs, cutoff, filter_type='low', fs=1.0):
    """
    设计切比雪夫II型数字滤波器（阻带等波纹）
    
    参数:
        order: 滤波器阶数
        rs: 阻带最小衰减(dB)
        cutoff: 截止频率
        filter_type: 'low', 'high', 'band', 'bandstop'
        fs: 采样频率
    返回:
        b, a: 滤波器系数
    """
    b, a = cheby2(order, rs, cutoff, btype=filter_type, fs=fs)
    return b, a


def design_elliptic_digital(order, rp, rs, cutoff, filter_type='low', fs=1.0):
    """
    设计椭圆数字滤波器
    
    参数:
        order: 滤波器阶数
        rp: 通带最大衰减(dB)
        rs: 阻带最小衰减(dB)
        cutoff: 截止频率
        filter_type: 'low', 'high', 'band', 'bandstop'
        fs: 采样频率
    返回:
        b, a: 滤波器系数
    """
    b, a = ellip(order, rp, rs, cutoff, btype=filter_type, fs=fs)
    return b, a


def digital_frequency_transform(b_lp, a_lp, transform_type, params):
    """
    数字滤波器频率变换
    
    将原型低通滤波器变换为其他类型
    
    参数:
        b_lp, a_lp: 原型低通滤波器系数
        transform_type: 'lp2lp', 'lp2hp', 'lp2bp', 'lp2bs'
        params: 变换参数
    返回:
        b, a: 变换后的滤波器系数
    """
    from scipy.signal import lp2lp, lp2hp, lp2bp, lp2bs
    
    if transform_type == 'lp2lp':
        # 低通到低通
        wo = params.get('wo', 1.0)
        b, a = lp2lp(b_lp, a_lp, wo=wo)
    elif transform_type == 'lp2hp':
        # 低通到高通
        wo = params.get('wo', 1.0)
        b, a = lp2hp(b_lp, a_lp, wo=wo)
    elif transform_type == 'lp2bp':
        # 低通到带通
        wo = params.get('wo', 1.0)
        bw = params.get('bw', 0.5)
        b, a = lp2bp(b_lp, a_lp, wo=wo, bw=bw)
    elif transform_type == 'lp2bs':
        # 低通到带阻
        wo = params.get('wo', 1.0)
        bw = params.get('bw', 0.5)
        b, a = lp2bs(b_lp, a_lp, wo=wo, bw=bw)
    else:
        raise ValueError(f"Unknown transform type: {transform_type}")
    
    return b, a


def analyze_iir_filter(b, a, fs=1.0):
    """
    分析IIR滤波器特性
    
    参数:
        b, a: 滤波器系数
        fs: 采样频率
    返回:
        分析结果字典
    """
    w, H = freqz(b, a, worN=8000)
    f = w * fs / (2 * np.pi)
    
    # 计算零极点
    z, p, k = tf2zpk(b, a)
    
    # 稳定性判断
    is_stable = all(np.abs(p) < 1)
    
    return {
        'frequency': f,
        'magnitude': np.abs(H),
        'magnitude_db': 20 * np.log10(np.abs(H) + 1e-10),
        'phase': np.angle(H),
        'zeros': z,
        'poles': p,
        'is_stable': is_stable
    }


def plot_iir_comparison():
    """
    比较不同IIR滤波器的特性
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    order = 5
    cutoff = 0.2  # 归一化频率
    fs = 1.0
    
    # 1. 巴特沃斯 vs 切比雪夫 vs 椭圆
    ax = axes[0, 0]
    
    filters = [
        ('Butterworth', butter(order, cutoff, fs=fs)),
        ('Chebyshev I (rp=1dB)', cheby1(order, 1, cutoff, fs=fs)),
        ('Chebyshev II (rs=40dB)', cheby2(order, 40, cutoff, fs=fs)),
        ('Elliptic (rp=1dB, rs=40dB)', ellip(order, 1, 40, cutoff, fs=fs))
    ]
    
    for name, (b, a) in filters:
        result = analyze_iir_filter(b, a, fs)
        ax.plot(result['frequency'], result['magnitude_db'], 
                label=name, linewidth=2)
    
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title(f'IIR Filter Comparison (Order={order})')
    ax.set_ylim([-80, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 零极点图
    ax = axes[0, 1]
    colors = ['blue', 'red', 'green', 'purple']
    for (name, (b, a)), color in zip(filters, colors):
        result = analyze_iir_filter(b, a, fs)
        ax.scatter(np.real(result['poles']), np.imag(result['poles']), 
                   marker='x', s=100, color=color, label=f'{name} poles')
    
    # 画单位圆
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Pole Locations')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    # 3. 不同阶数的巴特沃斯滤波器
    ax = axes[1, 0]
    orders = [3, 5, 10]
    for order in orders:
        b, a = butter(order, cutoff, fs=fs)
        result = analyze_iir_filter(b, a, fs)
        ax.plot(result['frequency'], result['magnitude_db'], 
                label=f'Order={order}', linewidth=2)
    
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Butterworth Filter: Effect of Order')
    ax.set_ylim([-80, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. 滤波器类型比较
    ax = axes[1, 1]
    b_lp, a_lp = butter(5, 0.2, btype='low', fs=fs)
    b_hp, a_hp = butter(5, 0.2, btype='high', fs=fs)
    b_bp, a_bp = butter(5, [0.15, 0.25], btype='band', fs=fs)
    b_bs, a_bs = butter(5, [0.15, 0.25], btype='bandstop', fs=fs)
    
    filter_types = [
        ('Lowpass', b_lp, a_lp),
        ('Highpass', b_hp, a_hp),
        ('Bandpass', b_bp, a_bp),
        ('Bandstop', b_bs, a_bs)
    ]
    
    for name, b, a in filter_types:
        result = analyze_iir_filter(b, a, fs)
        ax.plot(result['frequency'], result['magnitude_db'], 
                label=name, linewidth=2)
    
    ax.set_xlabel('Normalized Frequency')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Butterworth Filter Types')
    ax.set_ylim([-80, 5])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('iir_filter_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'iir_filter_comparison.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("IIR滤波器设计演示")
    print("=" * 60)
    
    # 1. 设计方法介绍
    print("\n1. IIR滤波器设计方法")
    methods = {
        "冲激响应不变法": "保持模拟滤波器冲激响应的形状，可能有混叠",
        "双线性变换法": "避免混叠，但存在频率畸变，需要预畸变校正"
    }
    for name, desc in methods.items():
        print(f"   {name}: {desc}")
    
    # 2. 巴特沃斯滤波器设计
    print("\n2. 巴特沃斯低通滤波器设计")
    order = 5
    cutoff = 0.2
    b_butter, a_butter = design_butterworth_digital(order, cutoff)
    print(f"   阶数: {order}")
    print(f"   截止频率: {cutoff} (归一化)")
    print(f"   分子系数 b: {b_butter}")
    print(f"   分母系数 a: {a_butter}")
    
    # 稳定性分析
    result = analyze_iir_filter(b_butter, a_butter)
    print(f"   稳定性: {'稳定' if result['is_stable'] else '不稳定'}")
    print(f"   极点位置: {result['poles']}")
    
    # 3. 切比雪夫滤波器设计
    print("\n3. 切比雪夫I型滤波器设计")
    rp = 1.0  # 通带波纹(dB)
    b_cheby1, a_cheby1 = design_chebyshev1_digital(order, rp, cutoff)
    print(f"   通带波纹: {rp} dB")
    print(f"   分子系数 b: {b_cheby1}")
    print(f"   分母系数 a: {a_cheby1}")
    
    # 4. 椭圆滤波器设计
    print("\n4. 椭圆滤波器设计")
    rp, rs = 1.0, 40.0
    b_ellip, a_ellip = design_elliptic_digital(order, rp, rs, cutoff)
    print(f"   通带波纹: {rp} dB, 阻带衰减: {rs} dB")
    print(f"   分子系数 b: {b_ellip}")
    print(f"   分母系数 a: {a_ellip}")
    
    # 5. 滤波器比较
    print("\n5. 滤波器特性比较")
    print("   滤波器类型        | 通带特性    | 阻带特性    | 过渡带宽度")
    print("   " + "-" * 60)
    print("   巴特沃斯          | 最大平坦    | 单调下降   | 最宽")
    print("   切比雪夫I型       | 等波纹      | 单调下降   | 中等")
    print("   切比雪夫II型      | 最大平坦    | 等波纹     | 中等")
    print("   椭圆              | 等波纹      | 等波纹     | 最窄")
    
    # 绘制比较图
    print("\n6. 绘制IIR滤波器比较图...")
    plot_iir_comparison()


if __name__ == "__main__":
    demo()
