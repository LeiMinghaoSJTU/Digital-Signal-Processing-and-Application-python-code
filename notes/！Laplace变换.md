## Laplace变换

### 一、Laplace变换定义
函数 f(t)（定义在 t ≥ 0）的Laplace变换定义为：
$$ F(s) = \mathcal{L}\{f(t)\} = \int_{0}^{\infty} f(t)e^{-st}  dt $$

其中 $ s = \sigma + j\omega $ 是复变量。之后用某一函数的大写字母表示这一函数的Laplace变换。

对于某一复变函数 $F(s)=F(\beta+jw)$，其在直线 $\mathrm{Re}\,z=\beta$ 上的路径积分
$$
\frac{1}{2\pi j}\int_{\beta-j\infty}^{\beta+j\infty}F(s)e^{st}\,dt
$$

称为 $F$ 的Laplace逆变换。

### 存在定理

在 $[0,\infty)$ 的任何有限区间上分段连续，且被指数函数 $Me^{ct}$ 控制的函数 $f$ 在半平面 $\mathrm{Re}\,z> c$ 上存在解析的Laplace变换。


### 二、基本性质
线性性：$ \mathcal{L}\{af(t) + bg(t)\} = aF(s) + bG(s) $；

平移变换：$ \mathcal{L}\{f(t-a)u(t-a)\} = e^{-as}F(s) \quad (a > 0) $，其中 $u=\chi_{[0,\infty)}$.

$ \mathcal{L}\{e^{at}f(t)\} = F(s-a) $；

伸缩变换：$ \mathcal{L}\{f(at)\} = \frac{1}{|a|}F\left(\frac{s}{a}\right) \quad (a > 0) $；

#### 衰减性质

$$\lim_{s \to \infty} F(s)=0.$$

####  时域微分性质
- 一阶导数：$ \mathcal{L}\{f'(t)\} = sF(s) - f(0^+) $；
- n阶导数：$ \mathcal{L}\{f^{(n)}(t)\} = s^nF(s) - \sum_{k=1}^{n} s^{n-k}f^{(k-1)}(0^+) $；

#### 时域积分性质
$$ \mathcal{L}\left\{\int_{0}^{t} f(\tau)  d\tau\right\} = \frac{1}{s} F(s). $$

####  s域微分
$$ \frac{d^n}{ds^n}F(s)=(-1)^n \mathcal{L}\{t^n f(t)\} $$

####  s域积分
$$ \int_{s}^{\infty} F(u)  du =\mathcal{L}\left\{\frac{f(t)}{t}\right\} $$

#### 卷积定理
$$ \mathcal{L}\{(f * g)(t)\} = F(s)G(s) $$
其中 $ (f * g)(t) = \int_{0}^{t} f(\tau)g(t-\tau)  d\tau $. 

####  初值定理
$$ \lim_{t \to 0^+} f(t) = \lim_{s \to \infty} sF(s). $$

**证明：** $sF(s)=\mathcal{L}(f')(s)+f(0^+)$，两边取极限，根据衰减性质可得结论成立。

#### 终值定理
$$ \lim_{t \to \infty} f(t) = \lim_{s \to 0} sF(s). $$
*(要求sF(s)的所有极点位于s左半平面)*


**证明：** 在 $sF(s)=\mathcal{L}(f')(s)+f(0^+)$ 两边取 $s\to 0$，得到
$$
\lim_{s \to 0} sF(s)=\int_0^\infty f'(t)\,dt +f(0^+)=f(\infty).
$$

这里交换了极限与积分的顺序： $\int_0^\infty f'(t)\,dt=\lim_{s  \to \infty} \int_0^\infty f'(t)e^{-st}\,dt$，合法性由控制收敛定理确保。

#### 周期函数的 Laplace 变换

设 $f$ 是 $[0,\infty)$ 上的周期函数，且在一个周期内分段光滑。那么
$$
\mathcal{L} (f) (s)=\frac{1}{1-e^{-sT}}\int_0^T f(t)e^{-st}\,dt.
$$


### 三、常见函数的Laplace变换表

| 时域函数 f(t)                 | Laplace变换 F(s)                      | 收敛域 (ROC)   |
| ----------------------------- | ------------------------------------- | -------------- |
| 1. 单位脉冲 δ(t)              | 1                                     | 所有s          |
| 2. 单位阶跃 u(t)              | $ \frac{1}{s} $                       | Re(s) > 0      |
| 3. 常数 A                     | $ \frac{A}{s} $                       | Re(s) > 0      |
| 4. 斜坡函数 t                 | $ \frac{1}{s^2} $                     | Re(s) > 0      |
| 5. $t^n$ (n为正整数)          | $ \frac{n!}{s^{n+1}} $                | Re(s) > 0      |
| 6. $t^a$ (a为正数)            | $ \frac{\Gamma(a+1)}{s^{a+1}} $       | Re(s) > 0      |
| 7. 指数衰减 $e^{-at}$         | $ \frac{1}{s+a} $                     | Re(s) > -Re(a) |
| 8. 指数增长 $e^{at} $         | $ \frac{1}{s-a} $                     | Re(s) > Re(a)  |
| 9. 正弦 $sin(ωt) $            | $ \frac{\omega}{s^2 + \omega^2} $     | Re(s) > 0      |
| 10. 余弦$ cos(ωt) $           | $ \frac{s}{s^2 + \omega^2} $          | Re(s) > 0      |
| 11. 衰减正弦 $e^{-at}sin(ωt)$ | $ \frac{\omega}{(s+a)^2 + \omega^2} $ | Re(s) > -a     |
| 12. 衰减余弦 $e^{-at}cos(ωt)$ | $ \frac{s+a}{(s+a)^2 + \omega^2} $    | Re(s) > -a     |
| 13. 双曲正弦 $sinh(at) $      | $ \frac{a}{s^2 - a^2} $               | Re(s) > \|a\|  |
| 14. 双曲余弦 $cosh(at) $      | $ \frac{s}{s^2 - a^2} $               | Re(s) > \|a\|  |
