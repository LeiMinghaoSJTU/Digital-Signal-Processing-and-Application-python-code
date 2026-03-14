# LTI 离散系统的时域分析

## LTI 离散系统的基本概念

线性时不变（LTI）离散系统具有两个基本特性：线性性和时不变性

**线性性**
系统满足叠加原理。数学表述为：如果系统对输入 $x_1[n]$ 的响应是 $y_1[n]$，对输入 $x_2[n]$ 的响应是 $y_2[n]$，那么对于任意常数 $a$ 和 $b$，系统对输入 $a \cdot x_1[n] + b \cdot x_2[n]$ 的响应就是 $a \cdot y_1[n] + b \cdot y_2[n]$

**时不变性**
系统的特性不随时间变化。如果输入 $x[n]$ 产生输出 $y[n]$，那么输入 $x[n-k]$ 将产生输出 $y[n-k]$，其中 $k$ 是任意整数时移

## 单位脉冲响应

单位脉冲响应 $h[n]$ 是 LTI 离散系统最基本、最重要的特征，定义为系统对单位脉冲序列 $\delta[n]$ 的零状态响应

单位脉冲序列 $\delta[n]$ 的定义为：
$$
\delta[n] = 
\begin{cases} 
1 & n = 0 \\
0 & n \neq 0 
\end{cases}
$$

**单位脉冲响应的重要性**
- 完全表征了 LTI 系统的输入输出特性
- 任意离散时间信号都可以表示为加权、延时脉冲的线性组合：
  $$
  x[n] = \sum_{k=-\infty}^{\infty} x[k]\delta[n-k]
  $$

**通过 $h[n]$ 分析系统特性**
```python
# 判断系统性质的伪代码示例
def check_system_properties(h):
    # 因果性检查
    causal = all(h[n] == 0 for n < 0)
    
    # 稳定性检查
    stable = sum(abs(h[n]) for all n) < float('inf')
    
    return causal, stable
```

## 卷积和

卷积和是计算 LTI 离散系统对任意输入响应的基本运算

**卷积和定义**
对于输入序列 $x[n]$ 和系统脉冲响应 $h[n]$，输出 $y[n]$ 定义为：
$$
y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k] \cdot h[n-k]
$$

**卷积计算步骤**
1. **反折**：将 $h[k]$ 反折得到 $h[-k]$
2. **平移**：将 $h[-k]$ 平移 $n$ 得到 $h[n-k]$
3. **相乘**：将 $x[k]$ 与 $h[n-k]$ 相乘
4. **求和**：对乘积序列求和得到 $y[n]$ 在 $n$ 时刻的值
5. **重复**：对每个 $n$ 值重复上述过程

**卷积和性质**
| 性质   | 数学表达式                                                 |
| ------ | ---------------------------------------------------------- |
| 交换律 | $x[n] * h[n] = h[n] * x[n]$                                |
| 结合律 | $(x[n] * h_1[n]) * h_2[n] = x[n] * (h_1[n] * h_2[n])$      |
| 分配律 | $x[n] * (h_1[n] + h_2[n]) = x[n] * h_1[n] + x[n] * h_2[n]$ |
| 恒等性 | $x[n] * \delta[n] = x[n]$                                  |
| 时移性 | $x[n] * \delta[n-k] = x[n-k]$                              |

## 差分方程表示

LTI 离散系统常用线性常系数差分方程描述

**一般形式**
$$
\sum_{k=0}^{N} a_k y[n-k] = \sum_{m=0}^{M} b_m x[n-m]
$$

**系统分类**
- **递归系统（IIR 系统）**：
  $$
  y[n] = \sum_{m=0}^{M} b_m x[n-m] - \sum_{k=1}^{N} a_k y[n-k]
  $$
- **非递归系统（FIR 系统）**：
  $$
  y[n] = \sum_{m=0}^{M} b_m x[n-m]
  $$

**差分方程求解方法**
- **经典法**：求齐次解和特解
  - 齐次解：对应齐次方程 $\sum a_k y[n-k] = 0$ 的解
  - 特解：满足原非齐次方程的解
- **迭代法**：直接递归计算输出值
- **零输入/零状态法**：分别求零输入响应和零状态响应

**一阶系统示例**
$$
y[n] - a y[n-1] = b x[n]
$$
解为：
$$
y[n] = \frac{b}{1-a} \cdot x[n] + C \cdot a^n \quad (\text{当 } |a| < 1 \text{ 且 } n \to \infty \text{ 时特解存在})
$$

## 系统的性质

**因果性**
系统输出只取决于当前和过去的输入值。对于 LTI 系统，因果性的充分必要条件是：
$$
h[n] = 0 \quad \text{当 } n < 0
$$

**稳定性**
有界输入产生有界输出（BIBO 稳定）。对于 LTI 系统，稳定性的充分必要条件是：
$$
\sum_{n=-\infty}^{\infty} |h[n]| < \infty
$$

**可逆性**
存在逆系统 $h_{\text{inv}}[n]$，使得：
$$
h[n] * h_{\text{inv}}[n] = \delta[n]
$$
可逆性的条件是系统函数 $H(z)$ 的零点与极点都不在单位圆上

**记忆性**
- 无记忆系统：输出只取决于当前输入，$h[n] = K\delta[n]$
- 有记忆系统：输出取决于多个时刻的输入

**系统性质判断示例**
```python
def analyze_system(h):
    # 因果性判断
    is_causal = all(h[n] == 0 for n in range(-100, 0))
    
    # 稳定性判断
    is_stable = sum(abs(h[n]) for n in range(-1000, 1000)) < float('inf')
    
    # 记忆性判断
    is_memoryless = all(h[n] == 0 for n != 0) and h[0] != 0
    
    return {
        'causal': is_causal,
        'stable': is_stable,
        'memoryless': is_memoryless
    }
```