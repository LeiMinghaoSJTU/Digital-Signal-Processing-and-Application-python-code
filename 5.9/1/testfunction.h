//头文件名：testfunction.h
# include "observe.h"
double f1(double x,double y)
//{x/=3; y/=3; double t=3*(1-x)*(1-x)*exp(-x*x-(y+1)*(y+1));
//t=t-10*(x/5-x*x*x-y*y*y*y*y)*exp(-x*x-y*y)-exp(-(x+1)*(x+1)-y*y)/3; return t; }
{return x-4*y+2;}
double f2(double x,double y)
{return 3*exp(-(x*x+y*y)*0.01)*sin((x*x+y*y)/12); }
const int M=30,N=30; //网格分割数
double (*ff)(double,double)=f1; //曲面函数指针
