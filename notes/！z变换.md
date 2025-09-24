## Z变换

### 定义
- **双边Z变换**：
$$
X(z) = \sum_{n=-\infty}^{\infty} x[n] z^{-n}
$$

   上式中取 $z=e^{j\omega}$，即为离散 Fourier 变换。

- **单边Z变换**:
  $$
  X(z) = \sum_{n=0}^{\infty} x[n] z^{-n}
  $$

   它是 Laplace 变换 $ F(s) = \mathcal{L}\{f(t)\} = \int_{0}^{\infty} f(t)e^{-st}  dt $ 的离散化（$z=e^{s}$）.

### 收敛域 (ROC)

  - 有限长序列：ROC 为整个 Z 平面，除 $z=0$ 与 $z=\infty$.
  - 右边序列（因果信号）：$|z| > R_-$
  - 左边序列（反因果信号）：$|z| < R_+$
  - 双边序列：环形区域 $R_- < |z| < R_+$

### 常用性质
| 性质          | 表达式                                                                                 |
| ------------- | -------------------------------------------------------------------------------------- |
| 线性          | $a x_1[n] + b x_2[n] \leftrightarrow a X_1(z) + b X_2(z)$                              |
| 时移          | $x[n-k] \leftrightarrow z^{-k}X(z)$                                                    |
| 尺度变换      | $a^n x[n] \leftrightarrow X(z/a)$                                                      |
| 微分性质      | $nx(n) \leftrightarrow -z X'(z)$                                                       |
| 时间倒置      | $x[-n] \leftrightarrow X(1/z)$                                                         |
| 时域卷积      | $x_1[n] * x_2[n] \leftrightarrow X_1(z)X_2(z)$                                         |
| 初值定理      | 对因果信号，$x[0] = \lim_{z\to\infty} X(z)$                                            |
| 终值定理      | $\lim_{n\to\infty} x[n] = \lim_{z\to1} (z-1)X(z)$（需 ROC 含单位圆周）                 |
| 复卷积定理    | $x_1[n] x_2[n] \leftrightarrow \frac{1}{2\pi j} \oint_C X_1(v)X_2(z/v) v^{-1} dv$      |
| Paserval 定理 | $\sum_{n=-\infty}^{\infty} \|x[n]\|^2 = \frac{1}{2\pi j} \oint_C \|X(z)\|^2 z^{-1} dz$ |

### 逆Z变换方法
1. **部分分式展开**（最常用）：
   $$
   X(z) = K_0+\sum \frac{K_i z}{z - z_i} \rightarrow x[n] = K_0\delta (n)+\sum K_i (z_i)^n u[n].
   $$

   注：有重根的情况：
   $$
   \frac{Kz}{(z-z_0)^i} \rightarrow x[n]
   = K \frac{n(n-1)\cdots(n-i+2)}{(i-1)!} (z_0)^{n-i+1} u[n].
   $$

2. **幂级数展开**（长除法）：
   将 $X(z)$ 展开为 $z^{-1}$ 的幂级数，$z^{-n}$ 项的系数即 $x[n]$.
3. **留数定理**：
   $$
   x[n] = \frac{1}{2\pi j} \oint_C X(z) z^{n-1} dz = \sum \text{Residues}
   $$

   回忆：$f$ 的 $m$ 重极点 $z=z_0$ 处的留数为
   $$\text{Res}(f,z_0) = \lim_{z\to z_0} \frac{1}{(m-1)!} \frac{d^{m-1}}{dz^{m-1}}[(z-z_0)^m f(z)].$$


逆变换的存在唯一性由 $X(z)$ 在某一区域的洛朗级数确保。不同区域的洛朗级数展开会不同。一般来说，若 $X(z)$ 在 $\{R_1\leq|z-z_0|\leq R_2\}$ 内单值解析，则在 $z_0$ 处存在唯一洛朗展开。

### 典型变换对
| 序列 $x[n]$            | Z变换 $X(z)$                                                |
| ---------------------- | ----------------------------------------------------------- |
| $\delta[n]$            | $1$                                                         |
| $u[n]$                 | $\frac{1}{1-z^{-1}}$                                        |
| $a^n u[n]$             | $\frac{1}{1-az^{-1}}$                                       |
| $-a^n u[-n-1]$         | $\frac{1}{1-az^{-1}}$                                       |
| $n a^n u[n]$           | $\frac{az^{-1}}{(1-az^{-1})^2}$                             |
| $\cos(\omega_0 n)u[n]$ | $\frac{1-z^{-1}\cos\omega_0}{1-2z^{-1}\cos\omega_0+z^{-2}}$ |
| $\sin(\omega_0 n)u[n]$ | $\frac{z^{-1}\sin\omega_0}{1-2z^{-1}\cos\omega_0+z^{-2}}$   |
| $e ^{j\omega_0 n}u[n]$ | $\frac{1}{1-e^{j\omega_0}z^{-1}}$                           |

### 应用示例：差分方程求解
**系统方程**：
$$
y[n] - 0.6y[n-1] = x[n]
$$
取Z变换：
   $$
   Y(z) - 0.6z^{-1}Y(z) = X(z)
   $$

求系统函数：
   $$
   H(z) = \frac{Y(z)}{X(z)} = \frac{1}{1 - 0.6z^{-1}} \quad (|z|>0.6)
   $$

可得系统的单位脉冲响应：
   $$
   h[n] = (0.6)^n u[n]
   $$