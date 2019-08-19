\ 双曲型方程算法文件 waveU.sch（先求位移再求速度，粘性阻尼）：
\ 空间离散后矩阵形式为
\                  [M][A]+[C][V]+[S][U] = [F]
\ 其中 V=dU/dt，A=dV/dt。对加速度 A 和速度 V 进行时间向后差分，
\            [M]([V]-[ˉV])+[C]([U]-[ˉU])+[S][U]*Δt = [F]*Δt
\ 其中 ˉV 记为 V 的前一时刻值，即 ˉV=V(t-Δt)，Δt 为时间步长。
\ 对V再次进行时间向后差分并整理得
\ ([M]+[C]*Δt+[S]*Δt*Δt)[U] = [F]*Δt*Δt+([M]+[C]*Δt)[ˉU]+[M][ˉV]*Δt
\ -----------------------------------------------------------------
DEFI
STIF s
MASS m
DAMP c
LOAD f
TYPE w
MDTY l
INIT 2

EQUATION
VECT u1,v1
\.......... 读取解空间中的 u,v 作为上一时刻的位移和速度 .........../
READ(s,unod) u1,v1
\................... 线性方程组左端项(分布矩阵) .................../
MATRIX = [s]*dt*dt+[c]*dt+[m]
\....................... 线性方程组右端项 ........................./
FORC = [f]*dt*dt+[m*u1]+[m*v1]*dt+[c*u1]*dt

SOLUTION u
VECT u,u1,v1
$cc // 读取上一时刻位移和速度 u1 v1
READ(s,unod) u1,v1
$cc // 通过 v1 = (u-u1)/Δt 计算当前速度
[v1] = [u]-[u1]
[v1] = [v1]/dt
[u1] = [u]
$cc // 存储求解得到的当前时刻位移和速度 u1 v1
WRITE(o,unod) u1,v1

END
