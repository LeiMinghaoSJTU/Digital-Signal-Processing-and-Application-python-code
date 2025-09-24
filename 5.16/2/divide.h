//头文件：divide.h
//本文件前面要添加# include "testfunction.h"
//定义类型：网格三角形类TRI
//三角形平面方程类equation
//三角形分割类divide
inline double Max(double x,double y,double z) { return x>=y&&x>=z?x:(y>z?y:z); }
inline double Min(double x,double y,double z) { return x<=y&&x<=z?x:(y<z?y:z); }
struct TRI //网格三角形的类
{int out; int p[3][2]; //out为三角形移出首部的交换标记，初始0，移出为1
void get(point3D mesh[ ][N+1], point3D &a,point3D &b,point3D &c)//取顶点
{a=mesh[p[0][0]][p[0][1]];b=mesh[p[1][0]][p[1][1]];c=mesh[p[2][0]][p[2][1]]; }
point3D normal(point3D mesh[ ][N+1]) //求三角形的法向量
{point3D p0,p1,p2; get(mesh,p0,p1,p2); return (p1-p0)^(p2-p1); } double zmin(point3D mesh[ ][N+1]) //三角形中各顶点的最小z，即最近点的z
{point3D p0,p1,p2; get(mesh,p0,p1,p2); return Min(p0.z,p1.z,p2.z); }
double zmax(point3D mesh[ ][N+1]) //三角形中各顶点的最大z，即最远点的z
{point3D p0,p1,p2; get(mesh,p0,p1,p2); return Max(p0.z,p1.z,p2.z); }
static TRI TRIcreate(int i0,int j0,int i1,int j1,int i2,int j2) //索引返回三角形
{ TRI c; int b[3][2]={{i0,j0},{i1,j1},{i2,j2}}; memcpy(c.p,b,24); c.out=0;return c; }
static int col; static const double eps; //col为新出现的点的下标，eps为误差
};
int TRI::col=0; const double TRI::eps=1e-7; //运算中考虑误差eps为1e-7
struct equation //三角形平面方程类
{point3D norm; double d; //norm为平面单位法向量，方程为norm*p+d=0
equation(TRI &q,point3D mesh[ ][N+1]) //构造函数
{ norm=q.normal(mesh).unitize(); d=-(norm*mesh[q.p[0][0]][q.p[0][1]]); }
double f(point3D pt){ double t=norm*pt+d; if(fabs(t)<1e-7) t=0; return t; } //求函数值
};
class divide //三角形分割类
{private:
TRI *list; int k; point3D (*mesh)[N+1]; //list三角形数组(k为个数),mesh网格点数组
double t1,t2; //t1,t2为分割参数
public:
divide(TRI *lst,point3D msh[ ][N+1],int k0):list(lst),mesh(msh),k(k0),t1(0),t2(0) {} 
int cutting(int i, int j) //list[i]分割list[j]并插入新的三角形
{equation eq(list[i],mesh); point3D q0,q1,q2; list[j].get(mesh,q0,q1,q2);
bool u=(eq.f(q0)>=0&&eq.f(q1)>=0&&eq.f(q2)>=0); //j在i面正侧
u=u||(eq.f(q0)<=0&&eq.f(q1)<=0&&eq.f(q2)<=0); //j在i面反侧
if(u) projectInter(list[i],list[j]); //j在i面一侧，则用投影分割
else planeInter(list[i],list[j]); //j在i面的两侧，则用平面分割
divideAndInsert(i,j);
return k;
}
private:double parameter(double a,double b,double v=0.5) //取a/b或一个合适的比例
{if(fabs(b)<TRI::eps||a/b<TRI::eps) return 0.5; a/=b; return (a>1-TRI::eps?v:a); }
void shift(TRI &q,int i) //调整q的顶点为：p[i],p[(i+1)%3],p[(i+2)%3]
{if(i>0&&i<3){int s[10];memcpy(s,q.p,24);memcpy(s+6,s,16); memcpy(q.p,s+i*2,24);}}
void divideAndInsert(int i, int j) //根据分割参数实施list[i]分割list[j]并插入
{TRI p[3],q=list[j]; point3D p0,p1,p2,q1,q2; int i1,j1,i2,j2;q.get(mesh,p0,p1,p2);
int kk=2; i2=q.p[2][0]; j2=q.p[2][1]; q1=p0+(p1-p0)*t1; q2=p0+(p2-p0)*t2;
i1=M+1+TRI::col/(N+1); j1=TRI::col++%(N+1); mesh[i1][j1]=q1; //记录t1交点
if(fabs(t2-1)>TRI::eps) //若t2≠1则记录t2交点
{i2=M+1+TRI::col/(N+1); j2=TRI::col++%(N+1); mesh[i2][j2]=q2; kk=3; }
p[0]=TRI::TRIcreate(q.p[0][0],q.p[0][1],i1,j1,i2,j2); //至少分割成p[0],p[1]三角形
p[1]=TRI::TRIcreate(q.p[1][0],q.p[1][1],q.p[2][0],q.p[2][1],i1,j1);
if(kk==3) { p[2]=TRI::TRIcreate(q.p[2][0],q.p[2][1],i2,j2,i1,j1); } //t2≠1还有p[2]
int ii,jj; double zz;
for(jj=j;jj<k-1;jj++) list[jj]=list[jj+1]; k--; //删除原三角形list[j]
for(j=0;j<kk;j++) //有序插入新的三角形
{if(fabs(p[j].normal(mesh).z)/2<0.01) continue; //忽略投影面积0的三角形
zz=p[j].zmax(mesh); for(ii=i;ii<k&&zz<list[ii].zmax(mesh); ii++) ; //找插入位置
for(jj=k-1;jj>=ii;jj--) list[jj+1]=list[jj]; list[ii]=p[j]; k++; //插入新的三角形
}}
void planeInter(TRI &p,TRI&q) //平面p分割三角形q，取得分割参数
{
point3D pp[5],p0,*pt; q.get(mesh,pp[0],pp[1],pp[2]); pp[3]=pp[0]; pp[4]=pp[1];
equation eq(p,mesh);
for(pt=pp;pt<pp+2;pt++) //查找是否pp[0]、pp[1]开始，都不是则pp[2]开始
{ if(eq.f(pt[0])*eq.f(pt[1])<0&&eq.f(pt[1])*eq.f(pt[2])>=0)break; }
p0=pt[0]; t1=parameter(-eq.f(p0),eq.norm*(pt[1]-p0));
t2=parameter(-eq.f(p0),eq.norm*(pt[2]-p0),1.0); shift(q,pt-pp);
}
void projectInter(TRI &p,TRI&q) //p投影边分割q的投影，取得分割参数
{point3D pp[5],*pt,L0; q.get(mesh,pp[0],pp[1],pp[2]); pp[3]=pp[0]; pp[4]=pp[1];
point3D L[4],v,v0,v1,v2; p.get(mesh,L[0],L[1],L[2]); L[3]=L[0]; t1=0.5; t2=1;
for(int k=0;k<3;k++) //对三角形p的每一条边v，测试边投影是否投影分割三角形q
{v=L[k+1]-L[k]; L0=L[k];
for(pt=pp;pt<pp+3;pt++)
{v0=pt[0]-L0; v1=pt[1]-L0; v2=pt[2]-L0;
if( (v0^v).z*(v1^v).z<0&&(v1^v).z*(v2^v).z>=0) break;
} //测试分割
if(pt==pp+3) continue;
t1=parameter(-(v0^v).z,((pt[1]-pt[0])^v).z); //若分割求t1,t2
t2=parameter(-(v0^v).z,((pt[2]-pt[0])^v).z,1.0); shift(q,pt-pp); return;
}
}
};
