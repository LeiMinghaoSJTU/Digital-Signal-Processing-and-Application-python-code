## Shannon-Nyquist 采样公式
假设函数 $f$ 的傅里叶变换 $\hat{f}$ 的支集满足 $\text{supp } \hat{f} \subset [-1, 1]$（即 $\hat{f}(\xi) = 0$ 对于 $|\xi| \geq  1$)，则 $f$ 在任意点 $x$ 处的值可以根据其在采样点 $x_n = \frac{n}{2}$（$n \in \mathbb{Z}$) 处的值重新恢复：
\[
f(x) = \sum_{n \in \mathbb{Z}} f\left(\frac{n}{2}\right) \frac{\sin(2\pi (x - n/2))}{2\pi (x - n/2)}.
\]

这里，$\frac{\sin(2\pi (x - n/2))}{2\pi (x - n/2)}$ 是归一化的 sinc 函数，在 $x = n/2$ 时定义为 1（通过极限）. 

### 证明
证明分为两部分：
1. 证明泊松求和公式（Poisson Summation Formula）. 
2. 使用泊松求和公式证明采样定理. 

傅里叶变换采用以下定义：
\[
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-i2\pi \xi x}  dx, \quad f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{i2\pi \xi x}  d\xi.
\]

---

### 部分 1: 泊松求和公式的证明
**泊松求和公式**：若 $f \in L^1(\mathbb{R})$（即 $f$ 绝对可积），则
\[
\sum_{n \in \mathbb{Z}} f(x + n) = \sum_{k \in \mathbb{Z}} \hat{f}(k) e^{i2\pi k x}.
\]
特别地，当 $x = 0$ 时，$\sum_{n \in \mathbb{Z}} f(n) = \sum_{k \in \mathbb{Z}} \hat{f}(k)$.

**证明**：

定义函数
\[
F(x) = \sum_{n \in \mathbb{Z}} f(x + n).
\]
由于 $f \in L^1(\mathbb{R})$，该级数几乎处处收敛. $F(x)$ 是周期为 1 的函数，因为
\[
F(x + 1) = \sum_{n \in \mathbb{Z}} f(x + 1 + n) = \sum_{n \in \mathbb{Z}} f(x + (n + 1)) = \sum_{m \in \mathbb{Z}} f(x + m) = F(x),
\]
其中令 $m = n + 1$，且求和顺序可交换. 

接下来，计算 $F(x)$ 的傅里叶级数. 由于 $F(x)$ 周期为 1，其傅里叶级数为
\[
F(x) = \sum_{k \in \mathbb{Z}} c_k e^{i2\pi k x},
\]
其中系数 $c_k$ 为
\[
c_k = \int_0^1 F(x) e^{-i2\pi k x}  dx.
\]
代入 $F(x)$ 的定义：
\[
c_k = \int_0^1 \sum_{n \in \mathbb{Z}} f(x + n) e^{-i2\pi k x}  dx.
\]
由于 $f \in L^1(\mathbb{R})$，可应用 Fubini 定理交换求和与积分（控制收敛定理也适用）：
\[
c_k = \sum_{n \in \mathbb{Z}} \int_0^1 f(x + n) e^{-i2\pi k x}  dx.
\]
对每个固定 $n$，作变量替换 $y = x + n$. 当 $x$ 从 0 到 1 时，$y$ 从 $n$ 到 $n+1$，且 $dx = dy$，故
\[
\int_0^1 f(x + n) e^{-i2\pi k x}  dx = \int_n^{n+1} f(y) e^{-i2\pi k (y - n)}  dy = \int_n^{n+1} f(y) e^{-i2\pi k y} e^{i2\pi k n}  dy.
\]
因为 $k, n$ 为整数，$e^{i2\pi k n} = 1$，所以
\[
\int_0^1 f(x + n) e^{-i2\pi k x}  dx = \int_n^{n+1} f(y) e^{-i2\pi k y}  dy.
\]
因此，
\[
c_k = \sum_{n \in \mathbb{Z}} \int_n^{n+1} f(y) e^{-i2\pi k y}  dy = \int_{-\infty}^{\infty} f(y) e^{-i2\pi k y}  dy = \hat{f}(k).
\]
代入傅里叶级数，得
\[
F(x) = \sum_{k \in \mathbb{Z}} \hat{f}(k) e^{i2\pi k x},
\]
即泊松求和公式：
\[
\sum_{n \in \mathbb{Z}} f(x + n) = \sum_{k \in \mathbb{Z}} \hat{f}(k) e^{i2\pi k x}.
\]
特别地，当 $x = 0$ 时，$\sum_{n \in \mathbb{Z}} f(n) = \sum_{k \in \mathbb{Z}} \hat{f}(k)$.

---

### 部分 2: 采样定理的证明
假设 $\text{supp } \hat{f} \subset [-1, 1]$（带宽 $B = 1$). 采样间隔为 $T = 1/(2B) = 1/2$，采样点为 $x_n = nT = n/2$（$n \in \mathbb{Z}$). 目标是证明：
\[
f(x) = \sum_{n \in \mathbb{Z}} f\left(\frac{n}{2}\right) \frac{\sin(2\pi (x - n/2))}{2\pi (x - n/2)}.
\]

**证明**：
由于 $\hat{f}$ 在 $[-1, 1]$ 外为零，可将 $\hat{f}$ 视为区间 $[-1, 1]$ 上的函数. 该区间长度为 $L = 2$，因此考虑 $\hat{f}$ 在 $[-1, 1]$ 上的傅里叶级数展开. 基频为 $1/L = 1/2$，故指数项为 $e^{i2\pi (1/2) k \xi} = e^{i\pi k \xi}$. 傅里叶级数为
\[
\hat{f}(\xi) = \sum_{k \in \mathbb{Z}} c_k e^{i\pi k \xi}, \quad \xi \in [-1, 1],
\]

其中系数 $c_k$ 由下式给出：
\[
c_k = \frac{1}{2} \int_{-1}^{1} \hat{f}(\xi) e^{-i\pi k \xi}  d\xi = \frac{1}{2} \int_{-1}^{1} \hat{f}(\xi) e^{-i2\pi \xi (k/2)}  d\xi.
\]

根据傅里叶逆变换的定义，$\int_{-\infty}^{\infty} \hat{f}(\xi) e^{i2\pi \xi t}  d\xi = f(t)$，故
\[
\int_{-1}^{1} \hat{f}(\xi) e^{-i2\pi \xi k/2}  d\xi = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{-i2\pi \xi k/2}  d\xi = f(-k/2),
\]

即
\[
c_k = \frac{1}{2} f\left(-\frac{k}{2}\right).
\]

代入傅里叶级数：
\[
\hat{f}(\xi) = \sum_{k \in \mathbb{Z}} \frac{1}{2} f\left(-\frac{k}{2}\right) e^{i\pi k \xi} = \sum_{k \in \mathbb{Z}} \frac{1}{2} f\left(-\frac{k}{2}\right) e^{i2\pi \xi (k/2)}.
\]


根据傅里叶逆变换，我们有
\[
f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi) e^{i2\pi \xi x}  d\xi = \int_{-1}^{1} \hat{f}(\xi) e^{i2\pi \xi x}  d\xi 
\]

将 $\hat{f}(\xi)$ 的级数表达式代入：
\[
f(x) = \int_{-1}^{1} \left( \sum_{k \in \mathbb{Z}} \frac{1}{2} f\left(-\frac{k}{2}\right) e^{i2\pi \xi (k/2)} \right) e^{i2\pi \xi x}  d\xi.
\]

交换求和与积分：
\[
f(x) = \sum_{k \in \mathbb{Z}} \frac{1}{2} f\left(-\frac{k}{2}\right) \int_{-1}^{1} e^{i2\pi \xi (x + k/2)}  d\xi.
\]

计算积分（设 $y = x + k/2$):
\[
\int_{-1}^{1} e^{i2\pi \xi y}  d\xi = \left[ \frac{e^{i2\pi \xi y}}{i2\pi y} \right]_{\xi=-1}^{\xi=1} = \frac{e^{i2\pi y} - e^{-i2\pi y}}{i2\pi y} = \frac{2i \sin(2\pi y)}{i2\pi y} = \frac{\sin(2\pi y)}{\pi y}.
\]

因此，
\[
f(x) = \sum_{k \in \mathbb{Z}} \frac{1}{2} f\left(-\frac{k}{2}\right) \frac{\sin(2\pi (x + k/2))}{\pi (x + k/2)} = \sum_{k \in \mathbb{Z}} f\left(-\frac{k}{2}\right) \frac{\sin(2\pi (x + k/2))}{2\pi (x + k/2)}.
\]

令 $n = -k$，代入得
\[
f(x) = \sum_{n \in \mathbb{Z}} f\left(\frac{n}{2}\right) \frac{\sin(2\pi (x - n/2))}{2\pi (x - n/2)}.
\]

这正是采样公式. 