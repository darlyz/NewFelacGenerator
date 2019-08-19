\ 双曲型方程算法文件 newmark.sch(计算位移、速度、加速度，粘性阻尼)
\ 空间离散后矩阵形式为：
\                   [M][A]+[C][V]+[S][U] = [F]
\ 其中 V=dU/dt，A=dV/dt。基于 newmark-β 法，令 t+Δt 时刻的 Uˉ,Vˉ 为：
\                    Vˉ = V+((1-β)*A+β*Aˉ)*Δt
\               Uˉ = U+V*Δt+((1/2-γ)*A+γ*Aˉ)*Δt*Δt
\ 由此可以得到右端不含 Vˉ,Aˉ 的表达式：
\           Vˉ = (Uˉ-U)*β/(γ*Δt)  +V*(1-β/γ) +A*(1-β/(2*γ))*Δt
\           Aˉ = (Uˉ-U)/(γ*Δt*Δt) -V/(γ*Δt)  -A*(1/(2*γ)-1)
\ 带入到空间离散后的双曲型方程并整理得到：
\         ( [S] +[M]/(γ*Δt*Δt) +[C]*β/(γ*Δt) )[Uˉ] = [Fˉ]
\         + [M]( [U]/(γ*Δt*Δt) +[V]/(γ*Δt)  +[A]*(1/(2*γ)-1)    )
\         + [C]( [U]*β/(γ*Δt)  +[V]*(β/γ-1) +[A]*(β/(2*γ)-1)*Δt )
\ 当 β=0.5,γ=0.25 时 newmark-β 为常平均加速法，即每一时间段内：
\                     (Vˉ-V)/Δt = (Aˉ+A)/2
\ 当 β≥0.5,γ≥0.25*(0.5+β)*(0.5+β)时，newmark-β 是无条件稳定的隐格式算法。
\ -----------------------------------------------------------------------
DEFI
STIF s
MASS m
DAMP c
LOAD f
TYPE w
MDTY l
INIT 3

EQUATION
VECT u1,v1,w1
\................ 读取解空间中的 u1,v1,w1 作为上一时刻的位移、速度、加速度 ................/
READ(s,unod) u1,v1,w1
\............................... 线性方程组左端项(分布矩阵) .............................../
MATRIX = [s]+[m]*a0+[c]*a1
\................................... 线性方程组右端项 ...................................../
FORC = [f]+[m*u1]*a0+[m*v1]*a2+[m]*[w1]*a3+[c*u1]*a1+[c]*[v1]*a4+[c]*[w1]*a5

SOLUTION u
VECT u,v,w,,u1,v1,w1
$cc // 读取上一时刻的位移、速度、加速度 u1 v1 w1
READ(s,unod) u1,v1,w1
$cc // 通过 w = (u-u1)/(γ*Δt*Δt)-v1/(γ*Δt)-w1*(1/(2*γ)-1) 计算当前加速度
[w] = ([u]-[u1])*a0-[v1]*a2-[w1]*a3
$cc // 通过 v = v1+((1-β)*w+β*w1)*Δt 计算当前速度
[v] = [v1]+[w]*a7+[w1]*a6
$cc // 存储求解的当前时刻位移、速度、加速度 u v w
WRITE (o,unod) u,v,w

@BEGIN
 double o,a0,a1,a2,a3,a4,a5,a6,a7,aa;
        o = 0.5;                     // o := β
        aa = 0.25*(.5+o)*(.5+o);     // aa:= γ = (1/2+β)*(1/2+β)/4
        a0 = 1./(dt*dt*aa);          // a0 = 1/(γ*Δt*Δt)
        a1 = o/(aa*dt);              // a1 = β/(γ*Δt)
        a2 = 1./(aa*dt);             // a2 = 1/(γ*Δt)
        a3 = 1./(2*aa)-1.;           // a3 = 1/(2*γ)-1
        a4 = o/aa-1.;                // a4 = β/γ-1
        a5 = dt/2*(o/aa-2.);         // a5 = (β/(2*γ)-1)*Δt
        a6 = dt*(1.-o);              // a6 = (1-β)*Δt
        a7 = dt*o;                   // a7 = β*Δt

END
