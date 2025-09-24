//图形程序ege7_4painter.cpp 画家算法画网格图
//鼠标左击画网格图1，右击画网格图2
# include <graphics.h>
# include "testfunction.h"
# include "divide.h"
void createVertex(point3D meshData[ ][N+1],double (*f)(double,double),observe3D ob);
void process(point3D mesh[ ][N+1]); //由远而近画函数曲面网格
int main( )
{initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); setfillcolor(EGERGB(255,255,120));
mouse_msg msg; bool leftdown,rightdown; Rect rc={0,0,639,479};
point3D::setViewport(rc); point3D::setWindow(-12,12,12,-12); //设置视区窗口
point3D mesh[M+11][N+1]; observe3D ob; 
ob.lookAt( 1,-1,-2,0,1,0); //设置观察角度
createVertex(mesh,f1,ob); process(mesh); //初始显示f1网格图
for( ; is_run( ) ; delay_fps(60))
{leftdown=rightdown=false;
while(mousemsg()) {msg=getmouse();
if(msg.is_left( )&&msg.is_down( )) leftdown=true;
if(msg.is_right( )&&msg.is_down( )) rightdown=true; }
if(leftdown) { createVertex(mesh,f1,ob); process(mesh); } //左击画f1 
else if(rightdown) { createVertex(mesh,f2,ob); process(mesh); } //右击画f2
} 
closegraph( ); return 0; }

//生成曲面网格
void createVertex(point3D meshData[ ][N+1],double (*f)(double,double),observe3D ob)
{int i,j; double x,z,x0=-10,z0=-10,dx=20.0/M,dz=20.0/N;
for(i=0;i<=M;i++) for(j=0;j<=N;j++)
{ x=x0+i*dx; z=z0+j*dz; meshData[i][j]=ob.trans(point3D(x,f(x,z),z)); }
}
//按最远顶点由远而近排序三角形列表
void sortFar(TRI list[ ],int k,point3D mesh[ ][N+1])
{int i,j,kk; double zz,zt; TRI pp;
for(i=0;i<k;i++)
{zz=list[i].zmax(mesh);
for(kk=i,j=i+1;j<k;j++) { if((zt=list[j].zmax(mesh))>zz) { kk=j; zz=zt; } }
if(kk!=i) { pp=list[kk]; list[kk]=list[i]; list[i]=pp; }
} }
//包围盒无遮挡测试
bool boxTest(TRI &p,TRI &q,point3D mesh[ ][N+1]) //p,q的包围盒分离则true
{double pL,pT,pR,pB,qL,qT,qR,qB; point3D a,b,c;
p.get(mesh,a,b,c); pL=Min(a.x,b.x,c.x); pR=Max(a.x,b.x,c.x);
pB=Min(a.y,b.y,c.y); pT=Max(a.y,b.y,c.y);
q.get(mesh,a,b,c); qL=Min(a.x,b.x,c.x); qR=Max(a.x,b.x,c.x);
qB=Min(a.y,b.y,c.y); qT=Max(a.y,b.y,c.y); bool r=pL >=qR+TRI::eps;
return (r||qL >=pR+TRI::eps||pB>=qT+TRI::eps||qB>=pT+TRI::eps);
}
//P在Q'的v方向一侧测试
bool farOrNear(TRI &p,TRI&q,point3D mesh[ ][N+1],point3D v)
{point3D pp[3],pc; p.get(mesh,pp[0],pp[1],pp[2]); equation eq(q,mesh);
double t=1; 
if(q.normal(mesh)*v<0) t=-1; //Q'法向量与v同方向t为1，反方向t为-1
for(int i=0;i<3;i++) if(eq.f(pp[i])*t<-TRI::eps) return false; return true;
}
//投影不相交测试
bool outTri(TRI &p,TRI &t,point3D mesh[ ][N+1]) //t所有顶点在p某边界外侧则true
{point3D pp[3],qq[3],v; p.get(mesh,pp[0],pp[1],pp[2]); t.get(mesh,qq[0],qq[1],qq[2]);
if(((pp[1]-pp[0])^(pp[2]-pp[1])).z<0) { v=pp[0]; pp[0]=pp[2]; pp[2]=v; } //p边按逆时针
for(int i=0,j;i<3;i++) //对p的每条边界判断t所有顶点是否在外侧
{for(v=pp[(i+1)%3]-pp[i],j=0;j<3;j++) if((v^(qq[j]-pp[i])).z>0) break; //顶点在内侧
if(j==3) return true; //t所有顶点都不在边界内侧，返回true
} return false; 
}
bool project(TRI &p,TRI&q,point3D mesh[ ][N+1]) //p,q投影不相交则true
{return outTri(p,q,mesh)||outTri(q,p,mesh); }
//构建三角形列表：list[0]~list[k-1]
int createList(TRI list[ ],point3D mesh[ ][N+1])
{int k=0,i,j; TRI q;
for(i=0;i<=M-1;i++) 
{for(j=0;j<=N-1;j++) //构建三角形列表：list[0]~list[k-1], 顺时针
{q=TRI::TRIcreate(i,j,i+1,j,i,j+1); 
if(fabs(q.normal(mesh).z)/2>=0.01) list[k++]=q;
q=TRI::TRIcreate(i+1,j+1,i,j+1,i+1,j);
if(fabs(q.normal(mesh).z)/2>=0.01)list[k++]=q;
} return k; 
}}
void draw(TRI &q,point3D mesh[ ][N+1]) //画三角形
{Point c[3];
for(int i=0;i<3;i++)c[i]=mesh[q.p[i][0]][q.p[i][1]].toPoint();
fillpoly(3,(int*)c);}
void process(point3D mesh[ ][N+1]) //由远而近画函数曲面网格
{TRI *list; list=new TRI[2*(M+11)*(N+1)]; int i,j,k=0; bool noHide; double zminP;
point3D far0(0,0,1),near0(0,0,-1);
k=createList(list,mesh); //构建三角形列表：list[0]~list[k-1]
sortFar(list,k,mesh); //三角形列表按最远点排序
for(TRI::col=0,i=0;i<k-1; )
{if((zminP=list[i].zmin(mesh))>=list[i+1].zmax(mesh)) { i++; continue; } //情况(i)
for(noHide=true,j=i+1;j<k&&list[j].zmax(mesh)>zminP;j++)
{if(boxTest(list[i],list[j],mesh)||farOrNear(list[i],list[j],mesh,far0)) //(a)(b)
continue;
if(farOrNear(list[j],list[i],mesh,near0)||project(list[i],list[j],mesh)) //(c)(d)
continue;
noHide=false; break;
}
if(noHide) { i++; continue; } //没遮挡，继续下一个多边形确认
if(list[j].out==0) {TRI c(list[i]); list[i]=list[j]; c.out=1; list[j]=c;} //无标记则交换
else { divide d0(list,mesh,k); k=d0.cutting(i,j); } //有标记则i分割j
}
cleardevice(); for(i=0;i<k;i++) draw(list[i],mesh); //依次画出多边形
delete[ ] list; }
