void samar(double,double *,double,int);
void squr(double *,double *,double *,double *,double *,double *,double *,double *,double *,double *);
void nsxyzw(coorr,coefr,prmt,eqn,emass,edamp,eload,num)
double coefr[12],coorr[12],*prmt,eqn[256];
double emass[17],edamp[17],eload[17];
int num;
{
    int i,j,ncoor,nnode,ncoef,ndisp,ndof;
    double rou,emu,fx,fy,fz,penalty,cccc;
    double un[5],vn[5],wn[5];
    double x[5],y[5],z[5];
    double xc[4],uc[4];
    double fx1[4],fx2[4],fx3[4],fx4[4];
    double fu1[4],fu2[4],fu3[4],fu4[4];
    double x12[4],u12[4],flux12,flux21,flux12r,r12,r21;
    double x13[4],u13[4],flux13,flux31,flux13r,r13,r31;
    double x14[4],u14[4],flux14,flux41,flux14r,r14,r41;
    double x23[4],u23[4],flux23,flux32,flux23r,r23,r32;
    double x24[4],u24[4],flux24,flux42,flux24r,r24,r42;
    double x34[4],u34[4],flux34,flux43,flux34r,r34,r43;
    int mode;
    mode = 1;
    ncoor = 3;
    nnode = 4;
    ncoef = 3;
    ndisp = 4;
    ndof = 16;
    for (i=1; i<=ndof; ++i)
    {
        eload[i]=0.0;
        for (j=1; j<=ndof; ++j)
        {
            eqn[(i-1)*16+j-1]=0.0;
        }
    }
    rou=prmt[1];
    emu=prmt[2];
    fx=prmt[3];
    fy=prmt[4];
    fz=prmt[5];
    penalty=prmt[6];
    for (j=1; j<=nnode; ++j)
    {
        un[j]=coefr[(1-1)*4+j-1];
        vn[j]=coefr[(2-1)*4+j-1];
        wn[j]=coefr[(3-1)*4+j-1];
        x[j]=coorr[(1-1)*4+j-1];
        y[j]=coorr[(2-1)*4+j-1];
        z[j]=coorr[(3-1)*4+j-1];
    }
    xc[1]=(x[1]+x[2]+x[3]+x[4])/4;
    uc[1]=(un[1]+un[2]+un[3]+un[4])/4;
    xc[2]=(y[1]+y[2]+y[3]+y[4])/4;
    uc[2]=(vn[1]+vn[2]+vn[3]+vn[4])/4;
    xc[3]=(z[1]+z[2]+z[3]+z[4])/4;
    uc[3]=(wn[1]+wn[2]+wn[3]+wn[4])/4;
    x12[1]=(x[1]+x[2])/2;
    x13[1]=(x[1]+x[3])/2;
    x14[1]=(x[1]+x[4])/2;
    x23[1]=(x[2]+x[3])/2;
    x24[1]=(x[2]+x[4])/2;
    x34[1]=(x[3]+x[4])/2;
    u12[1]=(un[1]+un[2])/2;
    u13[1]=(un[1]+un[3])/2;
    u14[1]=(un[1]+un[4])/2;
    u23[1]=(un[2]+un[3])/2;
    u24[1]=(un[2]+un[4])/2;
    u34[1]=(un[3]+un[4])/2;
    x12[2]=(y[1]+y[2])/2;
    x13[2]=(y[1]+y[3])/2;
    x14[2]=(y[1]+y[4])/2;
    x23[2]=(y[2]+y[3])/2;
    x24[2]=(y[2]+y[4])/2;
    x34[2]=(y[3]+y[4])/2;
    u12[2]=(vn[1]+vn[2])/2;
    u13[2]=(vn[1]+vn[3])/2;
    u14[2]=(vn[1]+vn[4])/2;
    u23[2]=(vn[2]+vn[3])/2;
    u24[2]=(vn[2]+vn[4])/2;
    u34[2]=(vn[3]+vn[4])/2;
    x12[3]=(z[1]+z[2])/2;
    x13[3]=(z[1]+z[3])/2;
    x14[3]=(z[1]+z[4])/2;
    x23[3]=(z[2]+z[3])/2;
    x24[3]=(z[2]+z[4])/2;
    x34[3]=(z[3]+z[4])/2;
    u12[3]=(wn[1]+wn[2])/2;
    u13[3]=(wn[1]+wn[3])/2;
    u14[3]=(wn[1]+wn[4])/2;
    u23[3]=(wn[2]+wn[3])/2;
    u24[3]=(wn[2]+wn[4])/2;
    u34[3]=(wn[3]+wn[4])/2;
    fx4[1]=(x[1]+x[2]+x[3])/3;
    fx1[1]=(x[2]+x[3]+x[4])/3;
    fx2[1]=(x[3]+x[4]+x[1])/3;
    fx3[1]=(x[4]+x[1]+x[2])/3;
    fu4[1]=(un[1]+un[2]+un[3])/3;
    fu1[1]=(un[2]+un[3]+un[4])/3;
    fu2[1]=(un[3]+un[4]+un[1])/3;
    fu3[1]=(un[4]+un[1]+un[2])/3;
    fx4[2]=(y[1]+y[2]+y[3])/3;
    fx1[2]=(y[2]+y[3]+y[4])/3;
    fx2[2]=(y[3]+y[4]+y[1])/3;
    fx3[2]=(y[4]+y[1]+y[2])/3;
    fu4[2]=(vn[1]+vn[2]+vn[3])/3;
    fu1[2]=(vn[2]+vn[3]+vn[4])/3;
    fu2[2]=(vn[3]+vn[4]+vn[1])/3;
    fu3[2]=(vn[4]+vn[1]+vn[2])/3;
    fx4[3]=(z[1]+z[2]+z[3])/3;
    fx1[3]=(z[2]+z[3]+z[4])/3;
    fx2[3]=(z[3]+z[4]+z[1])/3;
    fx3[3]=(z[4]+z[1]+z[2])/3;
    fu4[3]=(wn[1]+wn[2]+wn[3])/3;
    fu1[3]=(wn[2]+wn[3]+wn[4])/3;
    fu2[3]=(wn[3]+wn[4]+wn[1])/3;
    fu3[3]=(wn[4]+wn[1]+wn[2])/3;
    squr(xc,x12,fx4,fx3,uc,u12,fu4,fu3,&flux12,&flux12r);
    flux12 = rou*flux12;
    flux12r = rou*flux12r;
    samar(flux12r,&r12,emu,mode);
    flux21 = -flux12;
    r21 = 1.0-r12;
    squr(xc,x13,fx2,fx4,uc,u13,fu2,fu4,&flux13,&flux13r);
    flux13 = rou*flux13;
    flux13r = rou*flux13r;
    samar(flux13r,&r13,emu,mode);
    flux31 = -flux13;
    r31 = 1.0-r13;
    squr(xc,x14,fx3,fx2,uc,u14,fu3,fu2,&flux14,&flux14r);
    flux14 = rou*flux14;
    flux14r = rou*flux14r;
    samar(flux14r,&r14,emu,mode);
    flux41 = -flux14;
    r41 = 1.0-r14;
    squr(xc,x23,fx4,fx1,uc,u23,fu4,fu1,&flux23,&flux23r);
    flux23 = rou*flux23;
    flux23r = rou*flux23r;
    samar(flux23r,&r23,emu,mode);
    flux32 = -flux23;
    r32 = 1.0-r23;
    squr(xc,x24,fx1,fx3,uc,u24,fu1,fu3,&flux24,&flux24r);
    flux24 = rou*flux24;
    flux24r = rou*flux24r;
    samar(flux24r,&r24,emu,mode);
    flux42 = -flux24;
    r42 = 1.0-r24;
    squr(xc,x34,fx2,fx1,uc,u34,fu2,fu1,&flux34,&flux34r);
    flux34 = rou*flux34;
    flux34r = rou*flux34r;
    samar(flux34r,&r34,emu,mode);
    flux43 = -flux34;
    r43 = 1.0-r34;
    eqn[(1-1)*16+1-1]=(r12-1.)*flux12+(r13-1.)*flux13+(r14-1.)
                      *flux14;
    eqn[(1-1)*16+5-1]=(1.-r12)*flux12;
    eqn[(1-1)*16+9-1]=(1.-r13)*flux13;
    eqn[(1-1)*16+13-1]=(1.-r14)*flux14;
    eload[1]=0.0;
    eqn[(5-1)*16+5-1]=(r23-1.)*flux23+(r24-1.)*flux24+(r21-1.)
                      *flux21;
    eqn[(5-1)*16+9-1]=(1.-r23)*flux23;
    eqn[(5-1)*16+13-1]=(1.-r24)*flux24;
    eqn[(5-1)*16+1-1]=(1.-r21)*flux21;
    eload[5]=0.0;
    eqn[(9-1)*16+9-1]=(r34-1.)*flux34+(r31-1.)*flux31+(r32-1.)
                      *flux32;
    eqn[(9-1)*16+13-1]=(1.-r34)*flux34;
    eqn[(9-1)*16+1-1]=(1.-r31)*flux31;
    eqn[(9-1)*16+5-1]=(1.-r32)*flux32;
    eload[9]=0.0;
    eqn[(13-1)*16+13-1]=(r41-1.)*flux41+(r42-1.)*flux42+(r43-1.)
                        *flux43;
    eqn[(13-1)*16+1-1]=(1.-r41)*flux41;
    eqn[(13-1)*16+5-1]=(1.-r42)*flux42;
    eqn[(13-1)*16+9-1]=(1.-r43)*flux43;
    eload[13]=0.0;
    eqn[(2-1)*16+2-1]=(r12-1.)*flux12+(r13-1.)*flux13+(r14-1.)
                      *flux14;
    eqn[(2-1)*16+6-1]=(1.-r12)*flux12;
    eqn[(2-1)*16+10-1]=(1.-r13)*flux13;
    eqn[(2-1)*16+14-1]=(1.-r14)*flux14;
    eload[2]=0.0;
    eqn[(6-1)*16+6-1]=(r23-1.)*flux23+(r24-1.)*flux24+(r21-1.)
                      *flux21;
    eqn[(6-1)*16+10-1]=(1.-r23)*flux23;
    eqn[(6-1)*16+14-1]=(1.-r24)*flux24;
    eqn[(6-1)*16+2-1]=(1.-r21)*flux21;
    eload[6]=0.0;
    eqn[(10-1)*16+10-1]=(r34-1.)*flux34+(r31-1.)*flux31+(r32-1.)
                        *flux32;
    eqn[(10-1)*16+14-1]=(1.-r34)*flux34;
    eqn[(10-1)*16+2-1]=(1.-r31)*flux31;
    eqn[(10-1)*16+6-1]=(1.-r32)*flux32;
    eload[10]=0.0;
    eqn[(14-1)*16+14-1]=(r41-1.)*flux41+(r42-1.)*flux42+(r43-1.)
                        *flux43;
    eqn[(14-1)*16+2-1]=(1.-r41)*flux41;
    eqn[(14-1)*16+6-1]=(1.-r42)*flux42;
    eqn[(14-1)*16+10-1]=(1.-r43)*flux43;
    eload[14]=0.0;
    eqn[(3-1)*16+3-1]=(r12-1.)*flux12+(r13-1.)*flux13+(r14-1.)
                      *flux14;
    eqn[(3-1)*16+7-1]=(1.-r12)*flux12;
    eqn[(3-1)*16+11-1]=(1.-r13)*flux13;
    eqn[(3-1)*16+15-1]=(1.-r14)*flux14;
    eload[3]=0.0;
    eqn[(7-1)*16+7-1]=(r23-1.)*flux23+(r24-1.)*flux24+(r21-1.)
                      *flux21;
    eqn[(7-1)*16+11-1]=(1.-r23)*flux23;
    eqn[(7-1)*16+15-1]=(1.-r24)*flux24;
    eqn[(7-1)*16+3-1]=(1.-r21)*flux21;
    eload[7]=0.0;
    eqn[(11-1)*16+11-1]=(r34-1.)*flux34+(r31-1.)*flux31+(r32-1.)
                        *flux32;
    eqn[(11-1)*16+15-1]=(1.-r34)*flux34;
    eqn[(11-1)*16+3-1]=(1.-r31)*flux31;
    eqn[(11-1)*16+7-1]=(1.-r32)*flux32;
    eload[11]=0.0;
    eqn[(15-1)*16+15-1]=(r41-1.)*flux41+(r42-1.)*flux42+(r43-1.)
                        *flux43;
    eqn[(15-1)*16+3-1]=(1.-r41)*flux41;
    eqn[(15-1)*16+7-1]=(1.-r42)*flux42;
    eqn[(15-1)*16+11-1]=(1.-r43)*flux43;
    eload[15]=0.0;
    for (i=2; i<=ndof; ++i)
        for (j=1; j<=i-1; ++j)
        {
            cccc = eqn[(i-1)*16+j-1];
            eqn[(i-1)*16+j-1] = eqn[(j-1)*16+i-1];
            eqn[(j-1)*16+i-1] = cccc;
        }
    return;
}

