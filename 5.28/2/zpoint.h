//头文件名：zpoint.h
//本文件前面要添加# include "testfunction.h"
//定义类型：带深度z的屏幕坐标类zPoint
//网格三角形类tri
//z缓冲处理类zBuffer
# include <iostream>
# include "testfunction.h"
struct zPoint: public Point //带深度z的屏幕坐标类
{double z; zPoint( ) { x=y=z=0; }
zPoint(Point p,double zz):Point(p),z(zz) { }
virtual void combine(point3D *p) { *this=zPoint(p->toPoint(),p->z); } //*p->屏坐标
virtual void interpolation(zPoint *p1,double t,zPoint *res) //*res为*this,*p1的t插值
{res->x=x+round(t*(p1->x-x)); res->y=y+round(t*(p1->y-y));res->z=z+t*(p1->z-z);}
virtual color_t colorInterpolation(zPoint*p1,double t) //*this到*p1的t处亮度
{ if(t>0&&t<1) return YELLOW; else return BLUE; } //插值颜色：端点蓝中间黄
};
struct tri //网格三角形的类
{int p[3][2];
static tri triCreate(int i0,int j0,int i1,int j1,int i2,int j2) //索引返回三角形
{tri c; int b[3][2]={{i0,j0},{i1,j1},{i2,j2}}; memcpy(c.p,b,24); return c; }
};
struct zBuffer//z缓冲算法的操作类
{private:
point3D* (*mesh)[N+1]; zPoint**pm; //mesh为网格点指针，pm为6个临时点指针
int u,w; //u为视区像素个数，w为视区中一行像素个数
public:
zBuffer(point3D *mesh0[ ][N+1],zPoint*pm0[ ]):mesh(mesh0),pm(pm0)
{ Rect rc; point3D::getViewport(rc); w=rc.Width( )+1; u=w*(rc.Height( )+1); }
void process( ) //利用z缓冲器画函数曲面网格
{
 double *pz; tri *list; list=new tri[2*(M+1)*(N+1)]; int i,j,k=0;
 try{ pz=new double[u]; } //开辟z缓冲器空间pz，可用new float[u]节省空间
 catch(std::bad_alloc*e) { outtextxy(0,0,e->what( )); delete[ ]list; return; } 
 for(i=0;i<u;i++) pz[i]=1e100; //pz为z缓冲器，初始为无穷大
 for(i=0;i<=M-1;i++) 
  {for(j=0;j<=N-1;j++) //生成三角形列表
  {list[k++]=tri::triCreate(i,j,i+1,j,i,j+1); //每个网格四边形分成两个三角形
  list[k++]=tri::triCreate(i+1,j+1,i,j+1,i+1,j);
  }}
cleardevice( );
for(i=0;i<k;i++) draw(list[i],pz); //z缓冲画每个三角形
delete[ ]list; delete[ ]pz;
}
private:
void draw(tri &p,double*pz) //画三角形p
{zPoint*p0=pm[0],*p1=pm[1],*p2=pm[2],*pp,*pL1,*pR1;
for(int i=0;i<3;i++) pm[i]->combine(mesh[p.p[i][0]][p.p[i][1]]); //提取p的带z点
if((p1->x-p0->x)*(p2->y-p1->y)-(p1->y-p0->y)*(p2->x-p1->x)==0) return; //p退化
if(p1->y<=p0->y&&p1->y<=p2->y) { pp=p0; p0=p1; p1=pp; } //排序p0,p1,p2
else if(p2->y<p0->y) { pp=p0; p0=p2; p2=pp; }
if(p2->y<p1->y) { pp=p1; p1=p2; p2=pp; }
if(p0->y==p1->y) //下三角形
{if(p0->x>p1->x) { pp=p0; p0=p1; p1=pp; }//保证p0在p1左边
scan(p0,p1,p2,p2,pz);} //z缓冲扫描梯形
else if(p1->y==p2->y) //上三角形
{if(p1->x>p2->x) { pp=p1; p1=p2; p2=pp; }//保证p1在p2左边
scan(p0,p0,p1,p2,pz);} //z缓冲扫描梯形
else //左或右三角形
{ double t=double(p1->y-p0->y)/(p2->y-p0->y); pp=pm[3];p0->interpolation(p2,t,pp);
if(p1->x<pp->x) { pL1=p1; pR1=pp; } //左三角形
else { pL1=pp; pR1=p1; } //右三角形
scan(p0,p0,pL1,pR1,pz);//扫描两个梯形
scan(pL1,pR1,p2,p2,pz);
}
}
void scan(zPoint*pL0,zPoint *pR0,zPoint *pL1,zPoint *pR1,double *pzL)
{zPoint*pL,*pR; double t,d,z;
pL=pm[4]; pR=pm[5]; pzL+=w*pL0->y; //pzL指向起始扫描行的z缓冲器
if(pL0->y==pL1->y) return; //退化梯形
for(int y=pL0->y;y<=pL1->y;y++,pzL+=w) //从上往下扫描梯形, pzL指向当前行
{t=double(y-pL0->y)/(pL1->y-pL0->y); //t为对应扫描行的插值参数
pL0->interpolation(pL1,t,pL); pR0->interpolation(pR1,t,pR);//插值边pL、pR
if(pL->x==pR->x) d=1; else d=pR->x-pL->x; //线段的长度
for(int x=pL->x;x<=pR->x;x++) //z缓冲填充扫描线段
{t=(x-pL->x)/d; z=pL->z+(pR->z-pL->z)*t;
if(z<pzL[x]) //未遮挡则画点并更新z缓冲器
{putpixel(x,pL->y,pL->colorInterpolation(pR,t)); pzL[x]=z; }
}}
}

};

