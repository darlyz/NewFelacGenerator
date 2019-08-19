DEFI
STIF s
MASS m
DAMP c
LOAD f
TYPE w
MDTY l
INIT 3

COEF uu1

EQUATION
VECT u1,v1,w1,u,du,uu1,gu
\ ================================================================
\ =    从指针数组中读取：                                        =
\ =    u1: 上一时间步的位移                                      =
\ =    v1: 上一时间步的速度                                      =
\ =    w1: 上一时间步的加速度                                    =
\ =    u:  上一迭代步的位移                                      =
\ =    du: 上一迭代步的位移增量                                  =
\ =    uu1:当前迭代步与上一时间步的位移差值                      =
\ ================================================================
READ(s,unod) u1,v1,w1,u,du,uu1
MATRIX = [s]+[m]*a0+[c]*a1
FORC=[f]+[s*uu1] \
    +[m*u1]*a0+[m*v1]*a2+[m]*[w1]*a3+[c*u1]*a1+[c]*[v1]*a4+[c]*[w1]*a5

SOLUTION v
VECT u,v,w,,u1,v1,w1,du,ue,uu1,gu
VECT u,v,w,u1,v1,w1,du,ue,uu1
\ ================================================================
\ =    从指针数组中读取：                                        =
\ =    u1: 上一时间步的位移                                      =
\ =    v1: 上一时间步的速度                                      =
\ =    w1: 上一时间步的加速度                                    =
\ =    u:  上一迭代步的位移                                      =
\ =    du: 上一迭代步的位移增量                                  =
\ =    uu1:当前迭代步与上一时间步的位移差值                      =
\ ================================================================
READ(s,unod) u1,v1,w1,u,du,uu1
$CC if (it==1 && itn==1) {               // 如果时间步和迭代步都为第一步
$CC // === 迭代步增量初始化为0 ===
[du]=0.0
$CC }
$CC aa = 0.0;                            // === 初始化aa，ab，bb ===
$CC ab = 0.0;
$CC bb = 0.0;
%NOD
%DOF
$CC // === ue: 当前步结果与上一迭代步的差值，即当前迭代步增量 ===
    [ue] = [v]-[u];
    aa = aa+[ue]*[ue];
	ab = ab+[ue]*[du];
	bb = bb+[du]*[du];
%DOF
%NOD
#sum double aa ab bb
$CC err = aa;                            // err 为当前迭代步误差
$CC if (itn==1) cc = 1.0;                // 迭代第一步取松弛因子为 1
$CC if (itn>1) {                         // 下面每一迭代步都调整松弛因子
$CC rab = sqrt(aa)*sqrt(bb);             // 当前增量UE与上一增量DU模乘积
$CC if (ab>0.5*rab) cc = cc*2.0;         // 若UE与DU夹角小于60°，松弛因子增倍
$CC if (ab>0.8*rab) cc = cc*2.0;         // 若UE与DU夹角小于37°，松弛因子再次增倍
$CC if (ab<0.0) cc = cc*0.5;             // 若UE与DU夹角大于90°，松弛因子减半
$CC if (ab<-0.40*rab) cc = cc*0.5;       // 若UE与DU夹角大于114°，松弛因子再次减半
$CC if (ab<-0.80*rab) cc = cc*0.5;       // 若UE与DU夹角大于143°，松弛因子再次减半
$CC }                                    //
$CC if (cc>1.0) cc = 1.0;                // 控制松弛因子不能大于1
$CC ul = 0.0;
%NOD
%DOF
$CC // === 根据松弛因子(cc)更新迭代步增量 ===
  [ue] = [ue]*cc;
$CC // === 计算本迭代步松弛后的结果v ===
  [v] = [u]+[ue];
$CC // === 计算本迭代步松弛后结果u的模平方的和ul ===
   ul = ul + [u]*[u];
%DOF
%NOD
#sum double ul
$CC // === 将本迭代步位移结果v赋给u ===
[u]=[v]
$CC // === 计算本迭代步的位移结果与上一时间步的位移结果的差值 ===
[uu1]=[u]-[u1]
$CC // ===================================================================
$CC // =    收敛判断                                                     =
$CC // =    err足够小，或者err相对于计算结果的模的平方的和足够小         =
$CC // =    或者迭代步数超出最大迭代步，都会被判断为收敛，停止迭代       =
$CC // =    end为迭代收敛标志变量。                                      =
$CC // ===================================================================
$CC if (err<tolerance || err<tolerance*ul || itn>itnmax) end = 1;
#min int end
$CC if (end==1){                        // 如果收敛
$CC // === 更新位移、速度、加速度结果 ===
[[w]=([u]-[u1])*a0-[v1]*a2-[w1]*a3
[v] =[v1]+[w]*a7+[w1]*a6
[u1]=[u]
[v1]=[v]
[w1]=[w]
$CC itn=1;                              // 迭代步置1
$CC if (time_now<1.5*dt) {                  // 如果是第一时间步
$CC // === 总位移取初值：0.0 === 
[gu]=0.0
$CC // === 将 gu 存储到指针数组 unodg 中 === 
WRITE(n,unodg) gu
$CC } else {                            // 若不是第一步
$CC // === 从 unodg 中读取 gu === 
READ(s,unodg) gu
$CC }
$CC // === 计算当前迭代步总位移 ===
[gu]=[gu]+[u1]
$CC // === 将 gu 存储到指针数组 unodg 中 === 
WRITE(o,unodg) gu
$CC itn=1;                              // 迭代步置1
[du]=0.0
$CC } else {                            // 若不收敛
$CC // === 更新本迭代步与上一迭代步的位移结果差值 ===
[du]=[ue]
$CC itn=itn+1;                          // 更新迭代步
$CC }
$CC // === 将本迭代步最终结果存储到指针数组 unod 中 === 
WRITE(o,unod) u1,v1,w1,u,du,uu1

@SUBET
  double aa,bb,ab,rab,err,ul;
  static double cc;
 
@head
 double *unodg;

@BEGIN
 double o,a0,a1,a2,a3,a4,a5,a6,a7,a8;
        o=0.5;                     // o := β
        a8=0.25*(.5+o)*(.5+o);     // aa:= γ = (1/2+β)*(1/2+β)/4
        a0=1./(dt*dt*a8);          // a0 = 1/(γ*Δt*Δt)
        a1=o/(a8*dt);              // a1 = β/(γ*Δt)
        a2=1./(a8*dt);             // a2 = 1/(γ*Δt)
        a3=1./(2*a8)-1.;           // a3 = 1/(2*γ)-1
        a4=o/a8-1.;                // a4 = β/γ-1
        a5=dt/2*(o/a8-2.);         // a5 = (β/(2*γ)-1)*Δt
        a6=dt*(1.-o);              // a6 = (1-β)*Δt
        a7=dt*o;                   // a7 = β*Δt

end
