"""
维纳滤波与卡尔曼滤波实现
包含内容：
- 维纳滤波（FIR和IIR形式）
- 因果维纳滤波
- 卡尔曼滤波
- 应用示例（信号去噪、系统辨识）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, correlate
from scipy.linalg import solve_toeplitz, toeplitz, inv


def fir_wiener_filter(x, d, M):
    """
    FIR维纳滤波器设计
    
    最小化 E[(d[n] - y[n])^2]，其中 y[n] = sum_{k=0}^{M-1} h[k] * x[n-k]
    
    参数:
        x: 输入信号
        d: 期望信号
        M: 滤波器阶数
    返回:
        h: 最优滤波器系数
        minimum_mse: 最小均方误差
    """
    N = len(x)
    
    # 估计自相关矩阵R
    r_xx = correlate(x, x, mode='full')
    r_xx = r_xx[N-1:] / N
    R = toeplitz(r_xx[:M])
    
    # 估计互相关向量p
    r_xd = correlate(x, d, mode='full')
    r_xd = r_xd[N-1:N-1+M] / N
    p = r_xd
    
    # 维纳-霍夫方程: R * h = p
    h = np.linalg.solve(R, p)
    
    # 计算最小均方误差
    r_dd = np.mean(d**2)  # 期望信号功率
    minimum_mse = r_dd - np.dot(p, h)
    
    return h, minimum_mse


def wiener_deconvolution(x, h, snr_db=20):
    """
    维纳反卷积（用于去模糊/均衡）
    
    参数:
        x: 观测信号
        h: 系统冲激响应（或点扩散函数）
        snr_db: 信噪比(dB)
    返回:
        y: 恢复信号
    """
    N = len(x)
    
    # 转换到频域
    X = np.fft.fft(x)
    H = np.fft.fft(h, N)
    
    # SNR转换为线性比例
    snr_linear = 10**(snr_db/10)
    
    # 维纳滤波器频域形式
    H_conj = np.conj(H)
    W = H_conj / (np.abs(H)**2 + 1/snr_linear)
    
    # 应用维纳滤波器
    Y = W * X
    y = np.real(np.fft.ifft(Y))
    
    return y


def kalman_filter_1d(z, Q=0.01, R=0.1, x0=0, P0=1):
    """
    一维卡尔曼滤波器
    
    状态方程: x[k+1] = x[k] + w[k]  (w ~ N(0, Q))
    观测方程: z[k] = x[k] + v[k]  (v ~ N(0, R))
    
    参数:
        z: 观测序列
        Q: 过程噪声方差
        R: 观测噪声方差
        x0: 初始状态估计
        P0: 初始误差协方差
    返回:
        x_est: 状态估计
        P: 误差协方差
    """
    N = len(z)
    x_est = np.zeros(N)
    P = np.zeros(N)
    
    # 初始化
    x_est[0] = x0
    P[0] = P0
    
    for k in range(1, N):
        # 预测
        x_pred = x_est[k-1]
        P_pred = P[k-1] + Q
        
        # 更新
        K = P_pred / (P_pred + R)  # 卡尔曼增益
        x_est[k] = x_pred + K * (z[k] - x_pred)
        P[k] = (1 - K) * P_pred
    
    return x_est, P


def kalman_filter_nd(F, H, Q, R, z, x0, P0):
    """
    多维卡尔曼滤波器
    
    状态方程: x[k+1] = F * x[k] + w[k]
    观测方程: z[k] = H * x[k] + v[k]
    
    参数:
        F: 状态转移矩阵
        H: 观测矩阵
        Q: 过程噪声协方差
        R: 观测噪声协方差
        z: 观测序列 (N x m)
        x0: 初始状态
        P0: 初始协方差
    返回:
        x_est: 状态估计序列
        P: 误差协方差序列
    """
    N = len(z)
    n = len(x0)
    
    x_est = np.zeros((N, n))
    P = np.zeros((N, n, n))
    
    x_est[0] = x0
    P[0] = P0
    
    for k in range(1, N):
        # 预测
        x_pred = F @ x_est[k-1]
        P_pred = F @ P[k-1] @ F.T + Q
        
        # 更新
        S = H @ P_pred @ H.T + R
        K = P_pred @ H.T @ inv(S)  # 卡尔曼增益
        x_est[k] = x_pred + K @ (z[k] - H @ x_pred)
        P[k] = (np.eye(n) - K @ H) @ P_pred
    
    return x_est, P


def kalman_smoother(F, H, Q, R, z, x0, P0):
    """
    卡尔曼平滑器（Rauch-Tung-Striebel平滑器）
    
    使用后向递推获得更平滑的估计
    
    参数:
        F, H, Q, R: 同卡尔曼滤波
        z: 观测序列
        x0, P0: 初始条件
    返回:
        x_smooth: 平滑后的状态估计
        P_smooth: 平滑后的协方差
    """
    # 先进行前向卡尔曼滤波
    x_est, P = kalman_filter_nd(F, H, Q, R, z, x0, P0)
    
    N = len(z)
    n = len(x0)
    
    x_smooth = x_est.copy()
    P_smooth = P.copy()
    
    # 后向平滑
    for k in range(N-2, -1, -1):
        # 预测协方差
        P_pred = F @ P[k] @ F.T + Q
        
        # 平滑增益
        C = P[k] @ F.T @ inv(P_pred)
        
        # 平滑估计
        x_smooth[k] = x_est[k] + C @ (x_smooth[k+1] - F @ x_est[k])
        P_smooth[k] = P[k] + C @ (P_smooth[k+1] - P_pred) @ C.T
    
    return x_smooth, P_smooth


def adaptive_lms(x, d, mu, M):
    """
    自适应LMS算法（最小均方算法）
    
    用于在线估计维纳滤波器系数
    
    参数:
        x: 输入信号
        d: 期望信号
        mu: 步长参数
        M: 滤波器阶数
    返回:
        w_history: 滤波器系数历史
        e_history: 误差历史
        y_history: 输出历史
    """
    N = len(x)
    w = np.zeros(M)
    
    w_history = np.zeros((N, M))
    e_history = np.zeros(N)
    y_history = np.zeros(N)
    
    for n in range(M, N):
        # 输入向量
        x_vec = x[n-M:n][::-1]
        
        # 滤波器输出
        y = np.dot(w, x_vec)
        y_history[n] = y
        
        # 误差
        e = d[n] - y
        e_history[n] = e
        
        # LMS更新
        w = w + 2 * mu * e * x_vec
        w_history[n] = w
    
    return w_history, e_history, y_history


def plot_filter_comparison():
    """
    比较不同滤波方法的性能
    """
    np.random.seed(42)
    N = 500
    t = np.linspace(0, 5, N)
    
    # 生成原始信号（缓慢变化）
    s = np.sin(2 * np.pi * 0.5 * t)
    
    # 添加噪声
    noise = 0.5 * np.random.randn(N)
    x = s + noise
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. 维纳滤波
    ax = axes[0, 0]
    h_wiener, _ = fir_wiener_filter(x, s, M=10)
    s_wiener = lfilter(h_wiener, 1, x)
    
    ax.plot(t, s, 'g-', label='Original', linewidth=2)
    ax.plot(t, x, 'b.', alpha=0.3, label='Noisy')
    ax.plot(t, s_wiener, 'r-', label='Wiener Filtered', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Wiener Filtering')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 2. 卡尔曼滤波
    ax = axes[0, 1]
    s_kalman, _ = kalman_filter_1d(x, Q=0.001, R=0.25)
    
    ax.plot(t, s, 'g-', label='Original', linewidth=2)
    ax.plot(t, x, 'b.', alpha=0.3, label='Noisy')
    ax.plot(t, s_kalman, 'r-', label='Kalman Filtered', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Kalman Filtering')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 3. LMS自适应滤波
    ax = axes[1, 0]
    # 参考输入（延迟版本）
    d = s
    x_ref = np.roll(x, 1)
    x_ref[0] = 0
    
    w_history, e_history, y_history = adaptive_lms(x_ref, d, mu=0.01, M=5)
    
    ax.plot(t, s, 'g-', label='Original', linewidth=2)
    ax.plot(t, y_history, 'r-', label='LMS Output', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('LMS Adaptive Filtering')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 4. 误差收敛
    ax = axes[1, 1]
    mse_wiener = np.mean((s[M:] - s_wiener[M:])**2)
    mse_kalman = np.mean((s - s_kalman)**2)
    
    methods = ['No Input', 'Wiener', 'Kalman', 'LMS']
    mses = [np.mean(noise**2), mse_wiener, mse_kalman, np.mean(e_history[M:]**2)]
    
    bars = ax.bar(methods, mses, color=['gray', 'blue', 'green', 'orange'])
    ax.set_ylabel('Mean Square Error')
    ax.set_title('Filtering Performance Comparison')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 在柱状图上添加数值
    for bar, mse in zip(bars, mses):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{mse:.4f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('wiener_kalman_filter.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Figure saved as 'wiener_kalman_filter.png'")


def demo():
    """主演示函数"""
    print("=" * 60)
    print("维纳滤波与卡尔曼滤波演示")
    print("=" * 60)
    
    # 生成测试数据
    np.random.seed(42)
    N = 200
    t = np.linspace(0, 4, N)
    
    # 原始信号
    s = np.sin(2 * np.pi * 0.5 * t) + 0.5 * np.cos(2 * np.pi * 1.5 * t)
    
    # 噪声
    noise = 0.3 * np.random.randn(N)
    x = s + noise
    
    print(f"\n1. 测试信号: 多频率正弦信号 + 高斯噪声")
    print(f"   样本数: {N}")
    print(f"   输入SNR: {10*np.log10(np.var(s)/np.var(noise)):.2f} dB")
    
    # 1. FIR维纳滤波
    print("\n2. FIR维纳滤波")
    M = 10
    h_wiener, mse_min = fir_wiener_filter(x, s, M)
    print(f"   滤波器阶数: {M}")
    print(f"   最优系数: {h_wiener}")
    print(f"   理论最小MSE: {mse_min:.6f}")
    
    # 应用维纳滤波
    s_wiener = lfilter(h_wiener, 1, x)
    mse_wiener = np.mean((s[M:] - s_wiener[M:])**2)
    print(f"   实际MSE: {mse_wiener:.6f}")
    
    # 2. 维纳反卷积
    print("\n3. 维纳反卷积示例")
    # 模拟模糊系统
    blur_kernel = np.ones(5) / 5
    blurred = np.convolve(s, blur_kernel, mode='same')
    blurred_noisy = blurred + 0.1 * np.random.randn(N)
    
    # 维纳反卷积
    restored = wiener_deconvolution(blurred_noisy, blur_kernel, snr_db=20)
    mse_blur = np.mean((s - blurred_noisy)**2)
    mse_restored = np.mean((s - restored)**2)
    print(f"   模糊后MSE: {mse_blur:.6f}")
    print(f"   恢复后MSE: {mse_restored:.6f}")
    
    # 3. 卡尔曼滤波
    print("\n4. 一维卡尔曼滤波")
    s_kalman, P_kalman = kalman_filter_1d(x, Q=0.001, R=0.09)
    mse_kalman = np.mean((s - s_kalman)**2)
    print(f"   过程噪声Q: 0.001")
    print(f"   观测噪声R: 0.09")
    print(f"   最终估计误差协方差: {P_kalman[-1]:.6f}")
    print(f"   MSE: {mse_kalman:.6f}")
    
    # 4. LMS自适应滤波
    print("\n5. LMS自适应滤波")
    # 系统辨识问题
    # 未知系统
    h_unknown = np.array([1, -0.5, 0.25])
    d_clean = lfilter(h_unknown, 1, s)
    d_noisy = d_clean + 0.1 * np.random.randn(N)
    
    w_history, e_history, y_history = adaptive_lms(x, d_noisy, mu=0.01, M=3)
    
    print(f"   未知系统系数: {h_unknown}")
    print(f"   LMS估计系数: {w_history[-1]}")
    print(f"   估计误差: {np.linalg.norm(h_unknown - w_history[-1]):.6f}")
    
    # 绘制比较图
    print("\n6. 绘制滤波器比较图...")
    plot_filter_comparison()


if __name__ == "__main__":
    demo()
