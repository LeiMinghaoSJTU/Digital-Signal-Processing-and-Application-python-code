//图形程序ege5_3.cpp 凸多边形重叠计算(按y轴向上，屏幕画对称图)
//鼠标左击画凸多边形，右击结束，然后切换画另一个凸多边形，
//若判断不是凸多边形，则将重画刚才的凸多边形
//键盘按'i' 进行凸多边型求交，然后重新画两个凸多边形，不考虑边同向重叠
# include <graphics.h>
# include <math.h>
struct Point
{int x,y;
Point(int xx=0,int yy=0) { x=xx; y=yy; }
Point operator-(Point b) const{ Point c(x-b.x,y-b.y); return c; } //向量减
double operator*(Point b) const{ return(double)x*b.x+(double)y*b.y; } //内积
bool operator!=(Point b)const{ return x!=b.x||y!=b.y; }
double zCross(Point b) const{ return (double)x*b.y-(double)y*b.x; } //叉乘z坐标
};
bool getMessages(bool&mv,bool&ld,bool&rd,char&ch); //检测鼠标操作或键盘操作
void interConvex(Point a[ ][30],int na[ ],Point b[ ],int&nb); //凸多边形求交
void refresh(Point a[ ][30],int na[ ],Point b[ ]=0,int nb=0); //显示凸多边形
//构造凸多边形
void createPoly(Point a[ ][30],int na[ ],int&k,bool leftdown,bool rightdown,bool move);
int main( )
{Point a[2][30],b[30]; int na[2]={0},nb=0,k=0; //a[k]为第k个凸多边形顶点
bool move,leftdown,rightdown; char ch;
initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(BLUE); setfillcolor(GREEN);
for( ; is_run( ) ; delay_fps(60))
{if(!getMessages(move,leftdown,rightdown,ch)) continue;
if(ch=='i') { interConvex(a,na,b,nb); refresh(a,na,b,nb); na[0]=na[1]=nb=0;}
else if(ch=='\0') { createPoly(a,na,k,leftdown,rightdown,move); }
} closegraph( ); return 0;
}

bool getMessages(bool &mv,bool &ld,bool &rd,char &ch)
{mouse_msg msg={0}; bool m=false; mv=ld=rd=false; ch='\0';
while(mousemsg( )||kbhit( ) )
{m=true; if(kbhit( ) ) { ch=getch( ); }
if(mousemsg( ) )
{msg=getmouse( );
if(msg.is_move( ) ) mv=true;
else if(msg.is_left( )&&msg.is_down( ) ) ld=true;
else if(msg.is_right( )&&msg.is_down( ) ) rd=true; }
} return m;
}

bool isConvex(Point aa[ ],int n) //判断是否凸多边形，并调整为逆时针序
{Point v1,v2; double val; int i,j;
if(n<3) return false;
v1=aa[n-1]-aa[n-2]; v2=aa[0]-aa[n-1]; val=v1.zCross(v2); if(val==0) return false;
if(val<0) { for(i=0,j=n-1;i<j;i++,j--){ v1=aa[i]; aa[i]=aa[j]; aa[j]=v1; } }
v1=aa[n-1]-aa[n-2]; v2=aa[0]-aa[n-1]; val=v1.zCross(v2); if(val<=0) return false;
for(v2=aa[0]-aa[n-1],i=1;i<n;i++){ v1=v2; v2=aa[i]-aa[i-1]; if(v1.zCross(v2)<=0) return false; }
return true;
}
void createPoly(Point a[ ][30],int na[ ],int &k,bool leftdown,bool rightdown,bool move)
{if(k==2) { if(leftdown) na[0]=na[1]=k=0; else return; }
if(rightdown) //按右键结束画凸多边形，若非凸多边形，则重画
{if(isConvex(a[k],na[k])) { a[k][na[k]]=a[k][0];na[k]++; k++;} else na[k]=0; }
else if(leftdown||move)
{Point *p=a[k]; int &n=na[k];
if(leftdown)
{if(n==0){ mousepos(&p[0].x,&p[0].y); n=1; }
mousepos(&p[n].x,&p[n].y); n++;
}
else if(n>0) { mousepos(&p[n-1].x,&p[n-1].y); }
} refresh(a,na); }

bool interLine(Point p0,Point p1,Point q0,Point q1,Point &pp) //求线段交点，相交true
{Point ab=p1-p0,cd=q1-q0,ac=q0-p0;
double Delta=-ab.zCross(cd),lambda=-ac.zCross(cd),mu=-ac.zCross(ab);
if(fabs(Delta)>=1e-7) { lambda/=Delta; mu/=Delta; }
if(fabs(Delta)<1e-7||lambda<0||lambda>1||mu<0||mu>1) return false;
pp.x=round(p0.x+lambda*ab.x); pp.y=round(p0.y+lambda*ab.y);
return pp!=p0&&pp!=q0;
}
void Advance(Point a[ ][30],int na[ ],int &i,int &j) //交替前进步骤
{Point vp,vq,vv; double S; int L=na[0]-1,m=na[1]-1,i0,j0;
i0=(i+L-1)%L; j0=(j+m-1)%m; //i0为i的前一点，j0为j的前一点
vp=a[0][i]-a[0][i0]; vq=a[1][j]-a[1][j0]; S=vp.zCross(vq);
if(S>0){ if(vp.zCross(a[1][j]-a[0][i])>0) i++; else j++; }
else if(S<0) { if(vq.zCross(a[0][i]-a[1][j])>0) j++; else i++; }
else
{if(vq.zCross(a[0][i]-a[1][j])<0) i++;
else if(vp.zCross(a[1][j]-a[0][i])<0) j++;
else { vv=a[1][j]-a[0][i]; if(vv*vp>0) i++; else j++; }
} i%=L; j%=m;
}

int Output(Point a[ ][30],int na[ ],int i,int j,Point w,Point b[ ],int &nb) //记录交点间顶点
{static int interN=0,t=0; static Point R0(-1,-1);
int L=na[0]-1,m=na[1]-1,i0=(i+L-1)%L,j0=(j+m-1)%m,k; //i0,j0为I,j的前一点
Point vq=a[1][j]-a[1][j0],vp=a[0][i]-a[0][i0]; interN++;
if(interN==1) {R0=w; if(vq.zCross(w)>0) t=i; else t=j;}//头个交点
else
{if(vq.zCross(vp)>0) //记录Qt,...,Qj-1,[w],t<=i ，Pi与w重合就不保存
{for(k=t;k!=j;k=(k+1)%m) b[nb++]=a[1][k];
t=i; if(w!=a[0][i]) b[nb++]=w;
}
else if(vq.zCross(vp)<0) //记录Pt,...,Pi-1,[w], t<=j
{for(k=t;k!=i;k=(k+1)%L) b[nb++]=a[0][k];
t=j; if(w!=a[1][j]) b[nb++]=w;
}
if(!(w!=R0)) { interN=0; t=0; R0.x=R0.y=-1; } //又回到第一次交点R0
} return interN;
}
int coincide(Point p0,Point p1,Point q0,Point q1) //正向1，反向-1，不重叠0
{Point vp=p1-p0,vq=q1-q0;
if(vp.zCross(vq)!=0||vp.zCross(q1-p0)!=0) return 0; //vp、vq不平行或平行不重叠
if(vp*vq<0) return -1; else return 1;
}

double div(Point v1,Point v2) { return (v1.x*10000.0+v1.y)/(v2.x*10000+v2.y); }
void interConvex(Point a[ ][30],int na[ ],Point b[ ],int &nb)
{ Point pp,p0,p1,q0,q1,vq; int i,j,k,L,m; i=0; j=0; k=1; L=na[0]-1; m=na[1]-1; nb=0;
while(k<=2*(L+m))
{p0=a[0][(i+L-1)%L]; p1=a[0][i]; q0=a[1][(j+m-1)%m]; q1=a[1][j];
if(coincide(p0,p1,q0,q1)<0) //重叠反向
{double tq1=div(q1-p0,p1-p0),tq0=div(q0-p0,p1-p0),t0=0,t1=1; //参数分析
if(tq1>t0) { t0=tq1; p0=q1; } if(tq0<t1) { t1=tq0; p1=q0; }
if(t0<=t1) { b[0]=p0; b[1]=p1; nb=2; } return;
}
else if(interLine(p0,p1,q0,q1,pp)) { if(!Output(a,na,i,j,pp,b,nb)) return; } //相交
Advance(a,na,i,j); k++; }
for(j=1;j<=m;j++) { vq=a[1][j]-a[1][j-1]; if(vq.zCross(a[0][0]-a[1][j])<0) break; }
if(j>m) { for(j=0;j<L;j++) b[j]=a[0][j]; nb=L; return; } //P内含于Q
for(j=1;j<=L;j++) { vq=a[0][j]-a[0][j-1]; if(vq.zCross(a[1][0]-a[0][j])<0) return; }
for(j=0;j<m;j++) b[j]=a[1][j]; nb=m; //Q内含于P
}
void refresh(Point a[ ][30],int na[ ],Point b[ ],int nb)
{int i,k; Point *pa; cleardevice( );
for(k=0;k<2;k++)
{pa=a[k]; moveto(pa[0].x,pa[0].y); for(i=1;i<na[k];i++) lineto(pa[i].x,pa[i].y); }
if(nb>0) fillpoly(nb,(int*)b); }
