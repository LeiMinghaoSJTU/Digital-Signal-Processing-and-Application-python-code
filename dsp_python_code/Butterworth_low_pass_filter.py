# 完整示例 —— 设计模拟 Butterworth 并用双线性变换获得数字 IIR 低通滤波器
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import buttap, bilinear_zpk, zpk2tf, freqz, lfilter

def design_butter_bilinear(N, fc, fs):
    """
    通过以下步骤设计数字低通 IIR（双线性变换法）：
      1) buttap 得到模拟 Butterworth 原型（归一化到 1 rad/s, 即周期为 2 pi）的零点 n，
      极点 p 和增益 k (其中Ha(s)=k * (s-n[0])*(s-n[1])*.../(s-p[0])*(s-p[1])*...)
      2) 对数字截止频率做预畸变（pre-warp）得到模拟截止角频率 Omega_c
      3) 缩放模拟极点并调整增益
      4) 使用 bilinear_zpk 做双线性变换得到数字零极增益
      5) 转换为传递函数系数 b, a
    输入:
      N  - 滤波器阶数
      fc - 数字域截止频率 (Hz)
      fs - 采样率 (Hz)
    返回:
      b, a - 可直接用于 scipy.signal.lfilter 的数字 IIR 系数，列向量，b 是分子系数，a 是分母系数
    """
    # 预畸变（pre-warp）
    Omega_c = 2 * fs * np.tan(np.pi * fc / fs)  # rad/s

    # 模拟原型
    z, p, k = buttap(N)

    # print(f'k={k}\np={p}\nz={z}')

    # 缩放到所需的模拟截止频率
    p = p * Omega_c
    k = k * (Omega_c ** N)


    # 双线性变换 (s -> 2*fs*(1 - z^-1)/(1 + z^-1))
    zd, pd, kd = bilinear_zpk(z, p, k, fs)

    # 转为传递函数系数
    b, a = zpk2tf(zd, pd, kd)
    return b, a

# ---------------------------
# 测试示例
# ---------------------------
if __name__ == "__main__": 
  # 在 `if __name__ == "__main__":` 下面编写测试代码，这样当直接运行该模块时，测试代码会运行；而当模块被导入时，测试代码不会运行，从而不影响导入它的程序。
    fs = 8000        # 采样频率 (Hz)
    fc = 800         # 截止频率 (Hz)
    N = 4            # 滤波器阶数

    b, a = design_butter_bilinear(N, fc, fs)

    print("Filter numerator coefficients (b):")
    print(np.round(b, 6))
    print("\nFilter denominator coefficients (a):")
    print(np.round(a, 6))

    # 频率响应
    worN = 2048
    w, h = freqz(b, a, worN)
    f = w * fs / (2 * np.pi)  # 转成 Hz

    plt.figure()
    plt.title("Frequency response (magnitude in dB)")
    plt.plot(f, 20 * np.log10(np.maximum(np.abs(h), 1e-12)))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.grid(True)
    plt.xlim(0, fs/2)
    plt.show()

    # 构造测试信号：低频 + 高频 + 噪声
    t = np.arange(0, 1.0, 1.0/fs)
    x = 1.0 * np.sin(2*np.pi*100*t) + 0.5 * np.sin(2*np.pi*2000*t) + 0.05 * np.random.randn(len(t))

    # 滤波
    y = lfilter(b, a, x)

    # 时域显示（前 20 ms）
    t_segment = t[:int(0.02*fs)]
    plt.figure()
    plt.title("Time domain (first 20 ms)")
    plt.plot(t_segment, x[:len(t_segment)], label="input")
    plt.plot(t_segment, y[:len(t_segment)], label="output")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 频域（FFT）比较
    nfft = 4096 
    Xf = np.fft.rfft(x, nfft)
    Yf = np.fft.rfft(y, nfft)
    freqs = np.fft.rfftfreq(nfft, 1.0/fs)

    plt.figure()
    plt.title("Magnitude spectrum (before and after filtering)")
    plt.semilogy(freqs, np.abs(Xf), label="input")
    plt.semilogy(freqs, np.abs(Yf), label="output")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.xlim(0, fs/2)
    plt.legend()
    plt.grid(True)
    plt.show()

