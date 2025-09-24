//图形程序ege7_1.cpp 网格图的观察变换
//鼠标左击画网格图1，右击画网格图2
# include <graphics.h>
# include "testfunction.h"
void process(double (*f)(double,double),observe3D ob);
int main( )
{initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); mouse_msg msg;
Rect rc={0,0,639,479}; point3D::setViewport(rc);point3D::setWindow(-12,12,12,-12); //视区窗口
observe3D ob; ob.lookAt(1,-1,-2,0,1,0); process(f1,ob); //设置观察角度
bool leftdown,rightdown;
for( ; is_run( ) ; delay_fps(60))
{leftdown=rightdown=false;
while(mousemsg())
{msg=getmouse();
if(msg.is_left()&&msg.is_down()) leftdown=true;
if(msg.is_right()&&msg.is_down()) rightdown=true;
}
if(leftdown) process(f1,ob); //鼠标左击画网格图1
else if(rightdown) process(f2,ob); //鼠标右击画网格图2
} closegraph(); return 0;
}
void process(double (*f)(double,double),observe3D ob)
{int k,i; double x,x2,z,z2,x0=-10,z0=-10,dx=20.0/M,dz=20.0/N;Point P1,P2,P3; cleardevice();
for(k=0;k<=M;k++) for(i=0;i<=N;i++) //逐个画网格
{x=x0+k*dx; z=z0+i*dz; x2=x+dx; z2=z+dz; P1=ob.trans(point3D(x,f(x,z),z)).toPoint();
P2=ob.trans(point3D(x,f(x,z2),z2)).toPoint(); P3=ob.trans(point3D(x2,f(x2,z),z)).toPoint();
if(i<N) line(P1.x,P1.y,P2.x,P2.y); if(k<M) line(P1.x,P1.y,P3.x,P3.y);
}
}
