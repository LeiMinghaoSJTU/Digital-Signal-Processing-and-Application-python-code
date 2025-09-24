//图形程序ege7_5zBuffer.cpp 网格图的观察变换
//鼠标左击画网格图1，右击画网格图2
# include <graphics.h>
# include "testfunction.h"
# include "zpoint.h"
//生成曲面网格
void createVertex(point3D meshData[ ][N+1],double (*f)(double,double),observe3D ob);
int main( )
{initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); mouse_msg msg; Rect rc={0,0,639,479};
point3D::setViewport(rc); point3D::setWindow(-12,12,12,-12); //设置视区和窗口
observe3D ob; ob.lookAt(1,-1,-2,0,1,0); //设置观察角度
point3D *mesh[M+1][N+1]; point3D meshData[M+1][N+1];
for(int i=0;i<=M;i++) for(int j=0;j<=N;j++) mesh[i][j]=&meshData[i][j];
zPoint a0[6],*pm[6]; for(int i=0;i<6;i++) pm[i]=&a0[i];
zBuffer oz(mesh,pm);
createVertex(meshData,f1,ob);
oz.process( );
bool leftdown,rightdown;
for( ; is_run( ) ; delay_fps(60))
{leftdown=rightdown=false;
while(mousemsg())
{msg=getmouse();
if(msg.is_left()&&msg.is_down()) leftdown=true;
if(msg.is_right()&&msg.is_down()) rightdown=true;
} if(leftdown) { createVertex(meshData,f1,ob); oz.process( ); } //左击画f1 else if(rightdown) { createVertex(meshData,f2,ob); oz.process( ); } //右击画f2
}
closegraph();
return 0;
}
void createVertex(point3D meshData[ ][N+1],double (*f)(double,double),observe3D ob)
{int i,j; double x,z,x0=-10,z0=-10,dx=20.0/M,dz=20.0/N;
for(i=0;i<=M;i++) for(j=0;j<=N;j++)
{x=x0+i*dx; z=z0+j*dz; meshData[i][j]=point3D(ob.trans(point3D(x,f(x,z),z))); }
}
