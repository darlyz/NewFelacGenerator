\ 双曲型方程算法文件wave.sch(只计算位移、速度不计算加速度)
\ 空间离散后矩阵形式为：
\           [M][A]+[C][V]+[S][U] = [F]
\ 其中 V=dU/dt，A=dV/dt。时间离散后可得
\           [M][^A]+[C][^V]+[S][^U] = [^F]
\ 其中 ^A 记为 A 的前半时刻的值，即 ^A=A(t-Δt/2)，以此类推。首先令
\           ([V]+[ˉV])/2 = ([U]-[ˉU])/Δt
\ 也就是
\           [V] = 2([U]-[ˉU])/Δt-[ˉV]
\ 同时令
\           [^A] = ([V]-[ˉV])/Δt
\           [^V] = ([U]-[ˉU])/Δt
\           [^U] = ([U]+[ˉU])/2
\ 其中 ˉV 记为 V 的前一时刻值，即 ˉV=V(t-Δt)，同理 ˉU，Δt 为时间步长，
\ 带入时间离散后的双曲线方程并整理得到
\    ([S]*Δt*Δt/4+[C]*Δt/2+[M])[U]
\   =[^F]*Δt*Δt/2+[M]*[ˉU]+[M][ˉV]*Δt+[C]*[ˉU]*Δt/2-[S]*[ˉU]*Δt*Δt/4           
\ 为方便计算用 [F] 代替 [^F]
\ -----------------------------------------------------------
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
\.......... 读取解空间中的 u1,v1 作为上一时刻的位移速度 ........./
READ(s,unod) u1,v1
\.................. 线性方程组左端项(分布矩阵) ................../
MATRIX = [s]*(dt/2)*(dt/2)+[c]*dt/2+[m]
\......................... 右端矩阵 ............................./
FORC = [f]*dt*dt/2+[m*u1]+[m*v1]*dt+[c*u1]*dt/2-[s*u1]*dt*dt/4

SOLUTION u
VECT u,u1,v1
$cc // 读取上一时刻位移和速度 u1 v1
READ(s,unod) u1,v1
$cc // 通过 v1 = 2(u-u1)/Δt-v1 计算当前速度
[v1] = [u]/dt*2-[u1]/dt*2-[v1]
[u1] = [u]
$cc // 存储求解的当前时刻位移和速度 u1 v1
WRITE(o,unod) u1,v1

END
