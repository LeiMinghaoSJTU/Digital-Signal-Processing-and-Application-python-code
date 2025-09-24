//头文件名：gouraudphong.h
//本文件前面要添加
# include "testfunction.h"
//定义类型：环境光和点光源类light
// 材料表面反光性质类material
// 带法向量的顶点坐标的类point3Ddir
// 带亮度和z的屏幕点坐标类GouraudPoint
// 带法向量和z的屏幕点坐标类PhongPoint
// 带亮度及亮度优先级和z的屏幕点坐标类FlatPoint
# include "zpoint.h"
struct light //环境光和点光源类
{
double Lx,Ly,Lz; //光源方向
double Iar,Iag,Iab,Ipr,Ipg,Ipb; //环境光强度和点光源光强度
double r,k; //点光源距离和距离调整参数
} src;
struct material //材料表面反光性质类
{double Kar,Kag,Kab; //环境反射系数
double Kdr,Kdg,Kdb; //漫反射系数
double Ks; //镜面反射系数
} mat;
struct point3Ddir: public point3D //带法向量的顶点坐标的类
{point3D norm; point3Ddir() { }
point3Ddir(point3D p):point3D(p) { }
color_t toIntensity( ) //由单位法向量计算亮度:I=IaRa+IP/(r+k)[Kd(L·N)+Ks(R·V)10]
{double LN,RV,smooth=10,t1=src.r+src.k, t2; int r,g,b; //t1=r+k
point3D L(src.Lx,src.Ly,src.Lz); LN=L*norm; if(LN<=0) LN=0;
RV= -2*LN*norm.z+src.Lz; // RV=R·V=R·(0,0,-1)= -Rz，L+R=2(L·N)N
if(RV<0) RV=0;// -Rz= -2(L·N)Nz+Lz
smooth=pow(RV,smooth); t2=mat.Ks*smooth; //t2=Ks(R·V)10
r=round(src.Iar*mat.Kar+src.Ipr/t1*(mat.Kdr*LN+t2));
g=round(src.Iag*mat.Kag+src.Ipg/t1*(mat.Kdg*LN+t2));
b=round(src.Iab*mat.Kab+src.Ipb/t1*(mat.Kdb*LN+t2));
if(r>255) r=255; if(g>255) g=255; if(b>255) b=255;
return EGERGB(r,g,b);
}
};
struct GouraudPoint: public zPoint//带亮度和z的屏幕点坐标类
{color_t intensity; //亮度
GouraudPoint() { }
GouraudPoint(Point p,double zz,color_t ii=0):zPoint(p,zz){ intensity=ii; }
void combine(point3D *p) //*p点转换为GouraudPoint点
{ zPoint::combine(p); intensity=(reinterpret_cast<point3Ddir*>(p))->toIntensity(); }
void interpolation(zPoint*p1,double t,zPoint*res) //*this到*p1的t插值，存入*res
{GouraudPoint*pres=dynamic_cast<GouraudPoint*>(res);
zPoint::interpolation(p1,t,res); pres->intensity=colorInterpolation(p1,t);
}
color_tcolorInterpolation(zPoint*p1,double t) //*this亮度到*p1亮度的t插值
{color_t c1=intensity,c2=(dynamic_cast<GouraudPoint*>(p1))->intensity;
int r,g,b; if(t<0) t=0; else if(t>1) t=1;
r=round(EGEGET_R(c1)*(1-t)+EGEGET_R(c2)*t); //三原色红色插值
g=round(EGEGET_G(c1)*(1-t)+EGEGET_G(c2)*t); //三原色绿色插值
b=round(EGEGET_B(c1)*(1-t)+EGEGET_B(c2)*t); //三原色蓝色插值
return EGERGB(r,g,b);
}
};
struct PhongPoint: public zPoint//带法向量和z的屏幕点坐标类
{point3D norm; //法向量
PhongPoint() { }PhongPoint(Point p,double zz):zPoint(p,zz){ }
void combine(point3D *p)//*p点转换为PhongPoint点
{zPoint::combine(p); this->norm=(reinterpret_cast<point3Ddir*>(p))->norm; }
void interpolation(zPoint *p1,double t,zPoint *res) //*this到*p1的t插值，存入*res
{PhongPoint* pp1=dynamic_cast<PhongPoint*>(p1);
PhongPoint* pres=dynamic_cast<PhongPoint*>(res);
zPoint::interpolation(p1,t,res); point3D n1=norm,n2=pp1->norm,nn;
nn=n1*(1-t)+n2*t; pres->norm=nn.unitize();
}
color_t colorInterpolation(zPoint*p1,double t) //*this到*p1的t插值点亮度
{PhongPoint pt; point3Ddir pd;
interpolation(p1,t,&pt); pd.norm=pt.norm;
return pd.toIntensity();
}
};
struct FlatPoint: public zPoint//带亮度及亮度优先级和z的屏幕点坐标类
{color_t intensity; //亮度
int R; //点的亮度优先级
FlatPoint() { }
FlatPoint(Point p,double zz,color_t ii=0,int rr=0):zPoint(p,zz){ intensity=ii; R=rr; }
void combine(point3D *p) //*p点转换为FlatPoint点
{zPoint::combine(p); R=0;intensity=(reinterpret_cast<point3Ddir*>(p))->toIntensity();}
void interpolation(zPoint*p1,double t,zPoint*res) //*this到*p1的t插值，存入*res
{FlatPoint*pres=dynamic_cast<FlatPoint*>(res);
zPoint::interpolation(p1,t,res); 
pres->intensity=colorInterpolation(p1,t);
pres->R=R+(dynamic_cast<FlatPoint*>(p1))->R+1; //优先级为端点优先级和+1
}
color_t colorInterpolation(zPoint*p1,double t) //*this到*p1的t插值点亮度
{FlatPoint*pp1=dynamic_cast<FlatPoint*>(p1); if(R>=pp1->R) return intensity; //取大优先级亮度，优先级相同取左端亮度
else return pp1->intensity;}
};
