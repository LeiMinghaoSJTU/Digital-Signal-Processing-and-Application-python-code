"""
z变换与逆z变换实现
包含内容：
- z变换计算（符号和数值）
- 部分分式展开法求逆z变换
- 围线积分法求逆z变换
- 系统函数H(z)分析
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import residuez, freqz, zpk2tf
from numpy.polynomial import polynomial as P


def z_transform_polynomial(x, n_start=0):
    """
    将离散序列表示为z变换的多项式形式
    X(z) = sum(x[n] * z^(-n))
    
    参数:
        x: 离散序列
        n_start: 起始时间索引
    返回:
        num: 分子多项式系数（z的降幂）
        den: 分母多项式系数（z的降幂）
    """
    # 分子多项式: x[0]*z^N + x[1]*z^(N-1) + ... + x[N]
    num = x
    # 分母多项式: z^N (对应z^(-N)在分子)
    den = np.zeros(len(x) + n_start + 1)
    den[0] = 1  # z^N 项
    
    return num, den


def partial_fraction_inverse_z(num, den):
    """
    使用部分分式展开法求逆z变换
    
    参数:
        num: 分子多项式系数（按z^(-1)升幂）
        den: 分母多项式系数（按z^(-1)升幂）
    返回:
        r: 留数（部分分式系数）
        p: 极点
        k: 直接项
    """
    r, p, k = residuez(num, den)
    return r, p, k


def inverse_z_time_domain(r, p, k, n):
    """
    根据部分分式展开结果计算时域序列
    
    参数:
        r: 留数数组
        p: 极点数组
        k: 直接项
        n: 时间索引数组
    返回:
        x: 时域序列
    """
    x = np.zeros(len(n))
    
    # 各部分分式的贡献
    for i in range(len(r)):
        x += r[i] * (p[i] ** n)
    
    # 直接项的贡献（脉冲及其延迟）
    for i in range(len(k)):
        if i < len(n):
            x[i] += k[i]
    
    return x


def z_transform_properties():
    """
    展示z变换的主要性质
    """
    properties = {
        "线性性": "Z{a*x[n] + b*y[n]} = a*X(z) + b*Y(z)",
        "时移": "Z{x[n-k]} = z^(-k)*X(z)",
        "指数加权": "Z{a^n*x[n]} = X(z/a)",
        "线性加权": "Z{n*x[n]} = -z*dX(z)/dz",
        "卷积": "Z{x[n]*y[n]} = X(z)*Y(z)",
        "初值定理": "x[0] = lim(z→∞) X(z)",
        "终值定理": "x[∞] = lim(z→1) (z-1)*X(z) (若极限存在)"
    }
    return properties


def common_z_transforms():
    """
    常用序列的z变换对
    """
    pairs = {
        "δ[n] (单位脉冲)": "1",
        "u[n] (单位阶跃)": "1/(1-z^(-1)), |z|>1",
        "a^n*u[n] (指数序列)": "1/(1-a*z^(-1)), |z|>|a|",
        "n*a^n*u[n]": "a*z^(-1)/(1-a*z^(-1))^2, |z|>|a|",
        "cos(ωn)*u[n]": "(1-z^(-1)*cos(ω))/(1-2*z^(-1)*cos(ω)+z^(-2)), |z|>1",
        "sin(ωn)*u[n]": "(z^(-1)*sin(ω))/(1-2*z^(-1)*cos(ω)+z^(-2)), |z|>1"
    }
    return pairs


def system_function_analysis(num, den):
    """
    分析系统函数H(z) = num(z)/den(z)
    
    参数:
        num, den: 分子和分母多项式系数
    返回:
        系统分析结果字典
    """
    # 计算零极点
    zeros = np.roots(num)
    poles = np.roots(den)
    
    # 稳定性判断
    is_stable = all(np.abs(poles) < 1)
    
    # 计算频率响应
    w, h = freqz(num, den, worN=512)
    
    return {
        'zeros': zeros,
        'poles': poles,
        'is_stable': is_stable,
        'frequency': w,
        'magnitude_response': np.abs(h),
        'phase_response': np.angle(h)
    }


def plot_z_domain_analysis(num, den):
    """
    绘制z域分析结果（零极点图和频率响应）
    """
    result = system_function_analysis(num, den)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # 1. 零极点图
    ax = axes[0]
    theta = np.linspace(0, 2*np.pi, 100)
    ax.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5, label='Unit circle')
    ax.scatter(np.real(result['zeros']), np.imag(result['zeros']), 
               marker='o', s=100, facecolors='none', edgecolors='b', label='Zeros')
    ax.scatter(np.real(result['poles']), np.imag(result['poles']), 
               marker='x', s=100, color='r', label='Poles')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Pole-Zero Plot')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    
    # 2. 幅频响应
    ax = axes[1]
    w_norm = result['frequency'] / np.pi
    ax.plot(w_norm, 20*np.log10(result['magnitude_response'] + 1e-10))
    ax.set_xlabel('Normalized Frequency (×π rad/sample)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Magnitude Response')
    ax.grid(True, alpha=0.3)
    
    # 3. 相频响应
    ax = axes[2]
    ax.plot(w_norm, np.unwrap(result['phase_response'])/np.pi)
    ax.set_xlabel('Normalized Frequency (×π rad/sample)')
    ax.set_ylabel('Phase (×π rad)')
    ax.set_title('Phase Response')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('z_transform_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'z_transform_analysis.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("z变换与逆z变换演示")
    print("=" * 60)
    
    # 1. 常用z变换对
    print("\n1. 常用z变换对")
    pairs = common_z_transforms()
    for seq, zt in pairs.items():
        print(f"   {seq}: {zt}")
    
    # 2. z变换性质
    print("\n2. z变换的主要性质")
    props = z_transform_properties()
    for name, formula in props.items():
        print(f"   {name}: {formula}")
    
    # 3. 部分分式展开求逆z变换
    print("\n3. 部分分式展开法求逆z变换")
    print("   示例: X(z) = (1 - 0.5z^(-1)) / ((1 - 0.8z^(-1)) * (1 - 0.4z^(-1)))")
    
    # 展开分子和分母
    num = [1, -0.5]  # 1 - 0.5z^(-1)
    den = np.convolve([1, -0.8], [1, -0.4])  # (1 - 0.8z^(-1))(1 - 0.4z^(-1))
    print(f"   分子系数: {num}")
    print(f"   分母系数: {den}")
    
    r, p, k = partial_fraction_inverse_z(num, den)
    print(f"   留数 r: {r}")
    print(f"   极点 p: {p}")
    print(f"   直接项 k: {k}")
    
    # 验证逆z变换
    n = np.arange(20)
    x_reconstructed = inverse_z_time_domain(r, p, k, n)
    print(f"   重构序列 x[n] (前10点): {x_reconstructed[:10]}")
    
    # 4. 系统函数分析
    print("\n4. 系统函数分析")
    print("   示例系统: H(z) = (1 + 2z^(-1) + z^(-2)) / (1 - 0.5z^(-1) - 0.25z^(-2))")
    num_sys = [1, 2, 1]
    den_sys = [1, -0.5, -0.25]
    
    result = system_function_analysis(num_sys, den_sys)
    print(f"   零点: {result['zeros']}")
    print(f"   极点: {result['poles']}")
    print(f"   系统稳定性: {'稳定' if result['is_stable'] else '不稳定'}")
    
    # 绘制分析结果
    print("\n5. 绘制系统分析结果...")
    plot_z_domain_analysis(num_sys, den_sys)
    
    # 5. 另一个系统示例
    print("\n6. 另一个系统分析")
    print("   低通滤波器: H(z) = (0.15 + 0.3z^(-1) + 0.15z^(-2)) / (1 - 0.7z^(-1) + 0.2z^(-2))")
    num_lp = [0.15, 0.3, 0.15]
    den_lp = [1, -0.7, 0.2]
    result_lp = system_function_analysis(num_lp, den_lp)
    print(f"   零点: {result_lp['zeros']}")
    print(f"   极点: {result_lp['poles']}")
    print(f"   系统稳定性: {'稳定' if result_lp['is_stable'] else '不稳定'}")


if __name__ == "__main__":
    demo()
