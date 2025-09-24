//图形程序ege8_1GouraudPhong.cpp 真实感网格图的观察变换
//鼠标左击画网格图1，右击画网格图2 //键盘:'m'画网格、'f' 常数明暗图、'g' Gouraud明暗图、'p' Phong明暗图、其它不变
# include <graphics.h>
# include "testfunction.h"
# include "gouraudphong.h"
bool getMessages(bool *pld,bool *prd,char *pch);//生成曲面网格
void createVertex(point3Ddir meshData[ ][N+1],double(*f)(double,double),observe3D ob);
int main( )
{initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); char ch='m'; Rect rc={0,0,639,479};
point3D::setViewport(rc); point3D::setWindow(-12,12,12,-12); //视区窗口
observe3D ob; ob.lookAt(1,-1,-2,0,1,0); //设置观察角度
point3D L(-0.4,0.9,1); L=ob.trans(L).unitize();
light src0={L.x,L.y,L.z,150,150,150,1500,1500,100,10,0};
material mat0={0.8,0.8,0.8,0.8,0.8,0.8,0.7}; src=src0; mat=mat0;
point3Ddir meshData[M+1][N+1]; point3D *mesh[M+1][N+1];
for(int i=0;i<=M;i++) for(int j=0;j<=N;j++) mesh[i][j]=&meshData[i][j];
zPoint a0[6],*pm0[6],*pm1[6],*pm2[6],*pm3[6],**pmm=pm0;
FlatPoint a1[6]; GouraudPoint a2[6]; PhongPoint a3[6];
for(int i=0;i<6;i++) { pm0[i]=&a0[i]; pm1[i]=&a1[i]; pm2[i]=&a2[i]; pm3[i]=&a3[i]; }
zBuffer oz(mesh,pm0);createVertex(meshData,f1,ob); oz.process( );
bool leftdown,rightdown;
for( ; is_run( ) ; delay_fps(60))
{if(!getMessages(&leftdown,&rightdown,&ch)) continue; //获取消息
if(leftdown) ff=f1; else if(rightdown) ff=f2;
if(ch=='m') pmm=pm0; else if(ch=='f') pmm=pm1;else if(ch=='g') pmm=pm2; else if(ch=='p') pmm=pm3;
oz=zBuffer(mesh,pmm); createVertex(meshData,ff,ob); oz.process( );
} closegraph(); return 0;
}
bool getMessages(bool*pld,bool*prd,char*pch)
{mouse_msg msg={0}; bool m=false; *pld=*prd=false;
while(mousemsg()||kbhit())
{if(kbhit()) { *pch=getch(); m=true; }
if(mousemsg())
{msg=getmouse();
if(msg.is_left()&&msg.is_down()) *pld=m=true;
else if(msg.is_right()&&msg.is_down()) *prd=m=true;
}
} return m; }

void createVertex(point3Ddir meshData[ ][N+1],double(*f)(double,double),observe3D ob)
{int i,j,i0,j0,i1,j1; double x,z,x0=-10,z0=-10,dx=20.0/M,dz=20.0/N; point3D v;
for(i=0;i<=M;i++) for(j=0;j<=N;j++)
{x=x0+i*dx; z=z0+j*dz; meshData[i][j]=point3Ddir(ob.trans(point3D(x,f(x,z),z))); }
for(i=1;i<=M;i++) for(j=1;j<=N;j++) //计算面片(i,j,i-1,j-1)的单位平面法向量
{v=(meshData[i-1][j]-meshData[i][j])^(meshData[i][j-1]-meshData[i][j]);
meshData[i][j].norm=v.unitize();
}
for(i=0;i<=M;i++) for(j=0;j<=N;j++) //生成顶点法向量
{i0=i; j0=j; i1=i+1; j1=j+1;
if(i0<1) i0=1; if(j0<1) j0=1; if(i1>M) i1=M; if(j1>N) j1=N;
v=meshData[i0][j0].norm+meshData[i0][j1].norm+meshData[i1][j0].norm+meshData[i1][j1].norm;
meshData[i][j].norm=v.unitize();
}
}
