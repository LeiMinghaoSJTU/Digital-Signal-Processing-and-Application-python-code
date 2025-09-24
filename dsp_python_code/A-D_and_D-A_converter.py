import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
'''
代码实现了以下功能：
1. 模拟信号生成：创建一个包含基波、谐波和噪声的模拟信号
2. A-D转换：将模拟信号量化为数字信号
3. D-A转换：将数字信号重建为模拟信号
4. 性能评估：计算信噪比(SNR)和量化误差

代码会生成以下几个图表：
1. 原始模拟信号：显示生成的模拟信号
2. 数字信号：显示经过A-D转换后的离散数字值
3. 重建信号：显示经过D-A转换后重建的模拟信号，并与原始信号对比
4. 量化误差：显示原始信号与重建信号之间的差异
5. 频谱分析：比较原始信号和重建信号的频谱
6. 不同量化比特数比较：展示不同分辨率下的重建效果
7. SNR与量化比特数关系：显示信噪比随量化精度提高而改善的情况
'''
# 设置字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子以保证结果可重现
np.random.seed(114514)

# 生成一个带有噪声的模拟信号，振幅在-1到1之间
def generate_analog_signal(duration=1.0, sampling_rate=1000, signal_freq=5, noise_level=0.1):
    # 时间向量, endpoint=False确保最后一个点不包含在内
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    # 生成基波信号
    clean_signal = np.sin(2 * np.pi * signal_freq * t)
    # 添加一些谐波
    harmonic1 = 0.3 * np.sin(2 * np.pi * 2 * signal_freq * t + 0.5)
    harmonic2 = 0.2 * np.sin(2 * np.pi * 3 * signal_freq * t + 1.2)
    # 添加噪声, loc=0表示均值为0, scale=1.0表示标准差为1.0,
    # size=t.shape确保噪声与信号长度一致。.shape 返回数组的维度，即(行数,列数)
    noise = noise_level * np.random.normal(loc=0, scale=1.0, size=t.shape)
    analog_signal = clean_signal + harmonic1 + harmonic2 + noise
    return t, analog_signal

# A-D转换（模拟到数字转换）
def analog_to_digital_conversion(analog_signal, bits=8, voltage_range=(-1, 1)):
    # voltage_range是前面模拟信号的电压(振幅)范围
    min_voltage, max_voltage = voltage_range
    # 量化级别数
    quantization_levels = 2 ** bits
    # 量化步长
    step_size = (max_voltage - min_voltage) / quantization_levels
    # 将信号缩放到0到量化级别数-1的范围
    scaled_signal = (analog_signal - min_voltage) / (max_voltage - min_voltage)
    digital_signal = np.round(scaled_signal * (quantization_levels - 1))
    # astype(int)将数组转换为整数类型
    return digital_signal.astype(int), step_size, min_voltage

# D-A转换（数字到模拟转换，零阶保持）
def digital_to_analog_conversion(digital_signal, step_size, min_voltage):
    reconstructed_signal = min_voltage + digital_signal * step_size
    return reconstructed_signal

# 计算信噪比(SNR)
def calculate_snr(original, reconstructed):
    signal_power = np.mean(original ** 2)
    noise_power = np.mean((original - reconstructed) ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# 主函数
def main():
    # 参数设置
    duration = 1.0  # 信号持续时间(秒)
    sampling_rate = 1000  # 采样率(Hz)
    signal_freq = 5  # 信号基频(Hz)
    noise_level = 0.1  # 噪声水平
    bits = 8  # ADC分辨率(比特)
    voltage_range = (-1, 1)  # 电压范围
    
    # 生成模拟信号
    t, analog_signal = generate_analog_signal(duration, sampling_rate, signal_freq, noise_level)
    
    # A-D转换
    digital_signal, step_size, min_voltage = analog_to_digital_conversion(
        analog_signal, bits, voltage_range)
    
    # D-A转换
    reconstructed_signal = digital_to_analog_conversion(digital_signal, step_size, min_voltage)
    
    # 计算信噪比
    snr = calculate_snr(analog_signal, reconstructed_signal)
    
    # 绘制结果
    plt.figure(figsize=(12, 10))
    
    # 原始模拟信号
    plt.subplot(2, 2, 1)
    plt.plot(t, analog_signal, 'b-', label='原始模拟信号')
    plt.title('原始模拟信号')
    plt.xlabel('时间 (s)')
    plt.ylabel('幅度')
    plt.grid(True)
    plt.legend()
    
    # 数字信号（量化后）
    plt.subplot(2, 2, 2)
    # stem为杆状图, 'r-'表示红色实线, markerfmt='ro'表示红色圆点, basefmt=' '表示不显示基线
    # 这里为了更清晰地显示数字信号, 只绘制每隔20个点的样本. 
    # t[start:stop:step]表示从start到stop每隔step取一个点，这里省略了start和stop，表示从头到尾
    plt.stem(t[::20], digital_signal[::20], markerfmt='ro', basefmt=' ', linefmt='r-')
    plt.title(f'数字信号 ({bits}位量化)')
    plt.xlabel('时间 (s)')
    plt.ylabel('数字值')
    plt.grid(True)
    
    # 重建的模拟信号
    plt.subplot(2, 2, 3)
    plt.plot(t, analog_signal, 'b-', alpha=0.5, label='原始信号')
    plt.plot(t, reconstructed_signal, 'r-', label='重建信号')
    plt.title(f'重建的模拟信号 (SNR: {snr:.2f} dB)')
    plt.xlabel('时间 (s)')
    plt.ylabel('幅度')
    plt.grid(True)
    plt.legend()
    
    # 绘制量化误差
    plt.subplot(2, 2, 4)
    quantization_error = analog_signal - reconstructed_signal
    plt.plot(t, quantization_error, 'g-')
    plt.title('量化误差')
    plt.xlabel('时间 (s)')
    plt.ylabel('误差幅度')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # 绘制频域分析
    plt.figure(figsize=(12, 8))
    
    # 原始信号频谱
    plt.subplot(2, 1, 1)
    f_orig, Pxx_orig = signal.welch(analog_signal, fs=sampling_rate, nperseg=1024)
    plt.semilogy(f_orig, Pxx_orig)
    plt.title('原始信号频谱')
    plt.xlabel('频率 [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.grid(True)
    
    # 重建信号频谱
    plt.subplot(2, 1, 2)
    f_recon, Pxx_recon = signal.welch(reconstructed_signal, fs=sampling_rate, nperseg=1024)
    plt.semilogy(f_recon, Pxx_recon)
    plt.title('重建信号频谱')
    plt.xlabel('频率 [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # 不同量化比特数的比较
    bits_list = [2, 4, 6, 8]
    snr_list = []
    
    plt.figure(figsize=(12, 8))
    # 对每个比特数进行A-D和D-A转换，并计算SNR; 这里 i 是索引（初始为0）, b是比特数。
    # enumerate() 函数接受一个可迭代对象（如列表、元组等），它返回一个枚举对象，每次迭代产生一个包含两个元素的元组：第一个元素是索引（从0开始），第二个元素是对应的值。
    for i, b in enumerate(bits_list):
        digital_signal_b, step_size_b, min_voltage_b = analog_to_digital_conversion(
            analog_signal, b, voltage_range)
        reconstructed_signal_b = digital_to_analog_conversion(
            digital_signal_b, step_size_b, min_voltage_b)
        snr_b = calculate_snr(analog_signal, reconstructed_signal_b)
        snr_list.append(snr_b)
        
        plt.subplot(2, 2, i+1)
        plt.plot(t, analog_signal, 'b-', alpha=0.3, label='原始信号')
        plt.plot(t, reconstructed_signal_b, 'r-', label=f'{b}位量化')
        plt.title(f'{b}位量化 (SNR: {snr_b:.2f} dB)')
        plt.xlabel('时间 (s)')
        plt.ylabel('幅度')
        plt.grid(True)
        plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    # 绘制SNR随量化比特数变化
    plt.figure(figsize=(10, 6))
    plt.plot(bits_list, snr_list, 'bo-')
    plt.title('SNR随量化比特数变化')
    plt.xlabel('量化比特数')
    plt.ylabel('SNR (dB)')
    plt.grid(True)
    plt.xticks(bits_list)
    plt.show()

if __name__ == "__main__":
    main()