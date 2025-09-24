//图形程序ege7_3floating.cpp 浮动水平线算法画网格图
//鼠标左击画网格图1，右击画网格图2
# include <graphics.h>
# include "testfunction.h"
void process(double (*f)(double,double),observe3D ob);void process2(double (*f)(double,double),observe3D ob);
int main( ) //与ege7_1.cpp的main函数代码相同
{initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); mouse_msg msg;
Rect rc={0,0,639,479}; point3D::setViewport(rc); point3D::setWindow(-12,12,12,-12); //视区窗口
observe3D ob; ob.lookAt( 1,-1,-2,0,1,0); process2(f1,ob); //设置观察角度
bool leftdown,rightdown;
for( ; is_run( ) ; delay_fps(60))
{leftdown=rightdown=false;
while(mousemsg())
{msg=getmouse();
if(msg.is_left()&&msg.is_down()) leftdown=true;
if(msg.is_right()&&msg.is_down()) rightdown=true;
}
if(leftdown) process2(f1,ob); //鼠标左击画网格图1
else if(rightdown) process2(f2,ob); //鼠标右击画网格图2
}
closegraph();
return 0;
}
int funHide(Point p,int yu[ ],int yL[ ]) //上浮动线上,中,浮动线之间,下浮动线中,下各返回2,1,0,-1,-2
{int k=p.x; if(p.y>=yL[k]) return (p.y>yL[k]?-2:-1);
if(p.y<=yu[k]) return (p.y<yu[k]?2:1); return 0;
}
void Line(Point p0,Point p1,int *yy,int*yy2) //画线p0p1并调整浮动线
{line(p0.x,p0.y,p1.x,p1.y); if(p0.x==p1.x) return;
double kt=double(p1.y-p0.y)/(p1.x-p0.x);
for(int i=p0.x+1; i<=p1.x;i++)
{yy[i]=round(p0.y+(i-p0.x)*kt);if(yy2[i]<0)yy2[i]=yy[i]; } //首次改yu、yL
}
Point inter(Point p0,Point p1,int *yy) //计算p0p1与直线yy[p0.x]-yy[p1.x]交点
{double t,d; d=(p1.y-p0.y)-(yy[p1.x]-yy[p0.x]); //p0.y+t(p1.y-p0.y)=yy[p0.x]+t(yy[p1.x]-yy[p0.x])
if(d==0) return p0;
t=(yy[p0.x]-p0.y)/d; if(t<=0) return p0; if(t>=1) return p1;
p0.x+=round(t*(p1.x-p0.x)); p0.y+=round(t*(p1.y-p0.y)); return p0;
}
void draw(Point p0,Point p1,int yu[ ],int yL[ ]) //画未被遮挡的p0p1网格线
{if(p0.x>=p1.x) return; int v0=funHide(p0,yu,yL),v1=funHide(p1,yu,yL);
if(v0>=-1&&v0<=1&&v1>=-1&&v1<=1) return;
if(v0>=1&&v1>=1) { Line(p0,p1,yu,yL); return; }
if(v0<=-1&&v1<=-1) { Line(p0,p1,yL,yu); return; }
if(v0>1) Line(p0,inter(p0,p1,yu),yu,yL);
if(v1>1) Line(inter(p0,p1,yu),p1,yu,yL);
if(v0<-1) Line(p0,inter(p0,p1,yL),yL,yu);
if(v1<-1) Line(inter(p0,p1,yL),p1,yL,yu); }
void process(double (*f)(double,double),observe3D ob) //浮动水平线主过程( (1,-1,-2)观察方向)
{int yu[650],yL[650],k,i; double x,z,x0=-10, z0=-10, dx=20.0/M,dz=20.0/N; Point Pki,Pki1,Pk1i;
Rect rc; point3D::getViewport(rc); cleardevice();
for(i=0;i<=rc.right;i++) yu[i]=yL[i]=-1; //初始浮动线y值为-1
for(k=0;k<=M;k++) for(i=N;i>=0;i--)
{x=x0+k*dx; z=z0+i*dz; Pki=ob.trans(point3D(x,f(x,z),z)).toPoint();
if(i<N){Pki1=ob.trans(point3D(x,f(x,z+dz),z+dz)).toPoint();draw(Pki,Pki1,yu,yL); }
if(k>0){Pk1i=ob.trans(point3D(x-dx,f(x-dx,z),z)).toPoint();draw(Pk1i,Pki,yu,yL); }
} }
//------------------------------------------------------------------------------------------------------------------
void process2(double (*f)(double,double),observe3D ob) //浮动水平线主过程2(全方向)
{int yu[650],yL[650],k,i; Rect rc; point3D::getViewport(rc); cleardevice();
for(i=0;i<=rc.right;i++) yu[i]=yL[i]=-1; //初始浮动线y值为-1
double x0=-10, z0=-10, dx=20.0/M,dz=20.0/N,x2=x0+M*dx,z2=z0+N*dz,sx,sz,u,v,t;
double d[4][4]={{x0,dx,z2,-dz},{x2,-dx,z0,dz},{z0,dz,x0,dx},{z2,-dz,x2,-dx}},*s;
int idx=3,kN=M,iN=N; Point Pki,Pki1,Pk1i;
sx=ob.trans(point3D(1,0,0)).z; sz=ob.trans(point3D(0,0,1)).z; //x、z轴观察方向
if(sx>0&&sz<=0) idx=0; else if(sx<0&&sz>=0) idx=1; else if(sz>0&&sx>=0) idx=2; //4种观察方向
if(idx>=2) { kN=N; iN=M; } s=d[idx]; //处理x方向条带的情况
double &u0=s[0],&du=s[1],&v0=s[2],&dv=s[3],&x=(idx<2?u:v),&z=(idx<2?v:u);
for(k=0;k<=kN;k++) for(i=0;i<=iN;i++) //处理v方向条带
{u=u0+k*du; t=v=v0+i*dv; Pki=ob.trans(point3D(x,f(x,z),z)).toPoint();
if(i>0){ v-=dv; Pki1=ob.trans(point3D(x,f(x,z),z)).toPoint();draw(Pki,Pki1,yu,yL); }
if(k>0){ u-=du; v=t; Pk1i=ob.trans(point3D(x,f(x,z),z)).toPoint();draw(Pk1i,Pki,yu,yL); }
} }
