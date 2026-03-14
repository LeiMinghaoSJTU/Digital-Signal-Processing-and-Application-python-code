import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# 设置中文字体
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

# 创建图像
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('小波函数及其函数族', fontsize=16)

# 定义Harr小波函数
def harr_wavelet(x):
    result = np.zeros_like(x)
    result[(x >= 0) & (x < 0.5)] = 1
    result[(x >= 0.5) & (x < 1)] = -1
    return result

# 定义小波缩放平移函数
def scaled_wavelet(x, j, k, wavelet_func):
    scale = 2**(-j)
    return scale**(-0.5) * wavelet_func((x - scale*k) / scale)

# 绘制Harr小波
x = np.linspace(-0.5, 2, 1000)
axes[0, 0].plot(x, harr_wavelet(x), 'b-', linewidth=2)
axes[0, 0].set_title('Harr小波母函数')
axes[0, 0].set_xlabel('x')
axes[0, 0].set_ylabel('ψ(x)')
axes[0, 0].grid(True)

# 绘制Harr小波函数族
x_family = np.linspace(-1, 3, 1000)
for j in range(2):
    for k in range(2):
        scale = 2**(-j)
        label = f'j={j}, k={k}'
        axes[0, 1].plot(x_family, scaled_wavelet(x_family, j, k, harr_wavelet), 
                       label=label, linewidth=2)

axes[0, 1].set_title('Harr小波函数族')
axes[0, 1].set_xlabel('x')
axes[0, 1].set_ylabel('ψ_{j,k}(x)')
axes[0, 1].legend()
axes[0, 1].grid(True)

# 定义Shannon小波的频域表示
def shannon_freq(ksi):
    K = np.zeros_like(ksi)
    K[(ksi >= -2*np.pi) & (ksi <= -np.pi)] = 1
    K[(ksi >= np.pi) & (ksi <= 2*np.pi)] = 1
    return K

# 通过傅里叶逆变换计算Shannon小波的时域表示
def shannon_wavelet(x):
    result = np.zeros_like(x, dtype=complex)
    for i, xi in enumerate(x):
        # 计算傅里叶逆变换
        integrand = lambda ksi: shannon_freq(ksi) * np.exp(1j * ksi * xi) / (2*np.pi)
        result[i] = integrate.quad(integrand, -2*np.pi, 2*np.pi, limit=1000)[0]
    return result.real

# 绘制Shannon小波频域表示
ksi = np.linspace(-3*np.pi, 3*np.pi, 1000)
axes[1, 0].plot(ksi, shannon_freq(ksi), 'r-', linewidth=2)
axes[1, 0].set_title('Shannon小波频域表示')
axes[1, 0].set_xlabel('ξ')
# axes[1, 0].set_ylabel('$\hat{\psi}(\xi)$')
axes[1, 0].grid(True)

# 绘制Shannon小波时域表示
x_shannon = np.linspace(-5, 5, 1000)
# 由于计算傅里叶逆变换较慢，我们可以使用已知的解析形式
# Shannon小波时域形式为: ψ(x) = (sin(2πx) - sin(πx))/(πx)
psi_shannon = (np.sin(2*np.pi*x_shannon) - np.sin(np.pi*x_shannon)) / (np.pi*x_shannon)
# 处理x=0处的奇点
psi_shannon[np.isnan(psi_shannon)] = 1  # 当x=0时，极限为1

axes[1, 1].plot(x_shannon, psi_shannon, 'r-', linewidth=2)
axes[1, 1].set_title('Shannon小波时域表示')
axes[1, 1].set_xlabel('x')
axes[1, 1].set_ylabel('ψ(x)')
axes[1, 1].grid(True)
axes[1, 1].set_xlim(-5, 5)

plt.tight_layout()
plt.show()