import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import spectrogram, windows
import matplotlib.colors as colors
from matplotlib import rcParams
config = {
        "font.family": 'serif',
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['SimSun'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
rcParams.update(config)


# 参数设置
fs = 1000          # 采样频率 (Hz)
duration = 1       # 信号时长 (秒)
t = np.arange(0, duration, 1/fs)  # 时间向量

# 创建线性调频信号
f0 = 1             # 起始频率 (Hz)
f1 = 10            # 结束频率 (Hz)
k = (f1 - f0)/duration  # 调频率 (Hz/s)

# 生成线性调频信号
s = np.cos(2 * np.pi * (f0 * t + 0.5 * k * t**2))

# 加窗傅里叶变换参数
window_length = 128    # 窗长度
overlap = window_length // 2  # 重叠长度
nfft = 1024            # FFT点数

# 计算加窗傅里叶变换（使用矩形窗）
window = windows.boxcar(window_length)  # 矩形窗
f, t_spec, Sxx = spectrogram(s, fs=fs, window=window, 
                             nperseg=window_length, 
                             noverlap=overlap, 
                             nfft=nfft, 
                             mode='magnitude')

# 绘制原函数图像
plt.figure(figsize=(6, 5))

plt.subplot(2, 1, 1)
plt.plot(t, s)
plt.xlabel('时间 (s)')
plt.ylabel('幅度')
plt.title('线性调频信号 (Chirp Signal)')
plt.grid(True)
plt.xlim([0, duration])

# 绘制时频分布图像
plt.subplot(2, 1, 2)
# 转换为分贝尺度
# Sxx_db = 10 * np.log10(Sxx + 1e-10)  # 加上小值避免log10(0)
Sxx_db = Sxx
# 创建图像
im = plt.pcolormesh(t_spec, f, Sxx_db, shading='gouraud', 
                   norm=colors.Normalize(vmin=np.min(Sxx_db), vmax=np.max(Sxx_db)),
                   cmap='jet')
plt.xlabel('时间 (s)')
plt.ylabel('频率 (Hz)')
plt.title('加窗傅里叶变换时频分布 (矩形窗)')
plt.colorbar(im, label='功率谱密度 (dB)')
plt.xlim([0, duration])
plt.ylim([0, 10])

# 添加理论频率变化曲线
theoretical_freq = f0 + k * t_spec
plt.plot(t_spec, theoretical_freq, 'w--', linewidth=1.5, label='理论频率变化')
plt.legend()

plt.tight_layout()


# 如果想要保存图像
plt.savefig('chirp_analysis.svg', dpi=300, format='svg')
plt.show()