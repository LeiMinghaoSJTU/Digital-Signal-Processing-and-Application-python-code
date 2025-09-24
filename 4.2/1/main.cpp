//图形程序ege5_1.cpp 多条线段求交改进算法
//功能1：鼠标左键拖拽画多个直线段
//功能2：点击右键，计算交点且设置交点标记，再点击左键重画直线段
//交点标记：红色圆黄色填充，半径5，用fillellipse(x,y,5,5)
#include <graphics.h>
#include <math.h>
#include <set>
using std::set;
const double eps=1e-7;
struct Point
{int x,y;
Point(int xx=0,int yy=0) { x=xx; y=yy; }
Point operator-(Point b) const{ Point c(x-b.x,y-b.y); return c; } //向量减
double operator*(Point b) const{ return(double)x*b.x+(double)y*b.y; } //内积
bool operator!=(Point b)const{ return x!=b.x||y!=b.y; }
double zCross(Point b) const{ return (double)x*b.y-(double)y*b.x; } //叉乘z坐标
bool operator<(Point b) const{ return x*10000+y<b.x*10000+b.y; } //重载<保证set
};
struct RealPoint//实数坐标点
{double x,y; RealPoint( ) { }
RealPoint(Point p) { x=p.x; y=p.y; } };
struct Line
{Point p1,p2;
double getY(double x) { return p1.y+double(p2.y-p1.y)/(p2.x-p1.x)*(x-p1.x); } //y坐标
bool less(Line s2,double x) //线段在x处相邻线段表中的<次序：在上或重合时偏上
{double y1=getY(x),y2=s2.getY(x);return y1<=y2-eps||(fabs(y1-y2)<eps&&(p2-p1).zCross(s2.p2-s2.p1)>0); }
};

void drawLines(Line s[ ],int&n,set<Point> &A,bool leftdown,bool rightdown,bool mv);
int main( )
{Line s[50]; set<Point> A; int n=0; bool move,leftdown,rightdown;
initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); setcolor(RED); setfillcolor(YELLOW);
setlinestyle(SOLID_LINE,0,3); mouse_msg msg={0};
for( ; is_run( ) ; delay_fps(60))
{move=leftdown=rightdown=false;
while(mousemsg ( ) )
{msg=getmouse( );
if(msg.is_move( ) ) move=true;
else if(msg.is_left( )&&msg.is_down( ) ) leftdown=true;
else if(msg.is_right( )&&msg.is_down( ) ) rightdown=true;
} drawLines(s,n,A,leftdown,rightdown,move);
} closegraph( ); return 0; }

void refresh(Line s[ ],int n,set<Point> &A); //重画直线段和交点
int vertInt(Line s[ ],int &n,set<Point> &A); //垂直线段移到后面，线段调整为左到右
void BentleyOttmann(Line s[ ],int n,set<Point> &A); //多条非垂直线段求交点

void drawLines(Line s[ ],int &n,set<Point> &A,bool leftdown,bool rightdown,bool mv)
{if(rightdown) //按右键求交点，画出交点，并设成初始状态，清交点集合A
{ int m=vertInt(s,n,A); BentleyOttmann(s,m,A); refresh(s,n,A); n=0; A.clear( ); }
else if(leftdown||(mv&&keystate(key_mouse_l))) //左键拖拽画直线段
{Point pp; mousepos(&pp.x,&pp.y); if(leftdown) s[n++].p1=pp;
s[n-1].p2=pp; refresh(s,n,A);
}
}
void refresh(Line s[ ],int n,set<Point> &A) //重画直线段和交点
{set<Point>::iterator ptr; cleardevice( );
for(int i=0;i<n;i++) line(s[i].p1.x,s[i].p1.y,s[i].p2.x,s[i].p2.y);
for(ptr=A.begin( );ptr!=A.end( );++ptr) fillellipse((*ptr).x,(*ptr).y,5,5);
}

int vertInt(Line s[ ],int &n,set<Point> &A) //垂直线段移到后面，线段调整为左到右
{int k,i,j; int xx,y1,y2; double yy; Line ss; Point pp;
for(j=i=0;i<n;i++) if((s[i].p2-s[i].p1)*(s[i].p2-s[i].p1)>4) s[j++]=s[i]; //删除离散点
for(k=n=j,i=0;i<k;i++) //将s中的垂直线段全部移到数组后面,s[k]~s[n-1]为垂线
{if(s[i].p1.x==s[i].p2.x) { k--; ss=s[i]; s[i]=s[k]; s[k]=ss; i--; }
else if(s[i].p1.x>s[i].p2.x) { pp=s[i].p1; s[i].p1=s[i].p2; s[i].p2=pp; } //顺线段左右
}
for(j=k;j<n;j++) //s[0]~s[k-1]为斜线，s[k]~s[n-1]为垂直线，扫描垂直线
{for(xx=s[j].p1.x,y1=s[j].p1.y,y2=s[j].p2.y,i=0;i<k;i++) //垂线与各斜线求交点
{if((s[i].p1.x-xx)*(s[i].p2.x-xx)>0) continue; //一定不相交
yy=s[i].getY(xx); if((yy-y1)*(yy-y2)<eps) A.insert(Point(xx,round(yy)));
}
} return k;
}
//-------------------------两条直线段求交点-------------------------------
bool interLine(Line s1,Line s2,RealPoint &rp) //求线段s1,s2的交点rp，相交则true
{Point ab=s1.p2-s1.p1,cd=s2.p2-s2.p1,ac=s2.p1-s1.p1;
double Delta=-ab.zCross(cd),lambda=-ac.zCross(cd),mu=-ac.zCross(ab);
if(fabs(Delta)>=1e-7) { lambda/=Delta; mu/=Delta; }
if(fabs(Delta)<1e-7||lambda<0||lambda>1||mu<0||mu>1) return false;
rp.x=s1.p1.x+lambda*ab.x; rp.y=s1.p1.y+lambda*ab.y; return true;
}

//----------相邻线段表的类-------
class neigLine
{private: Line *ps; int ns; int L[20]; int nL; //L为相邻线段表索引，nL为大小
 public:
  neigLine(Line s[ ],int n) { ps=s; ns=n; nL=0; } //构造函数
  void clear( ) { nL=0; } //清线段表
  int size( ) { return nL; } //取相邻线段个数
  void findMinMax(int &Min,int &Max)//线段表头尾
  {Min=Max=-1;if(nL>0){Min=L[0];Max=L[nL-1];} 
  }
  void findUpDown(RealPoint rp,int &Up,int &Down) //rp上下邻,Up,Down为-1表示无
  {int i; Up=Down=-1; if(nL==0) return;
   for(i=0;i<nL&&ps[L[i]].getY(rp.x)<rp.y-eps;i++); if(i>0) Up=L[i-1];
   while(i<nL&&fabs(ps[L[i]].getY(rp.x)-rp.y)<eps) i++; if(i<nL) Down=L[i];
  }
  bool inter(RealPoint rp) //判断rp点为交点
  { int i,k=0; for(i=0;i<nL;i++) if(fabs(ps[L[i]].getY(rp.x)-rp.y)<eps) k++; return k>1;
  }
  void del(RealPoint rp) //有序删除过rp点的线段
  {int i,j,n=nL; if(nL==0) return;
   for(nL=i=0;i<n;i++){ if(fabs(ps[L[i]].getY(rp.x)-rp.y)>=eps) L[nL++]=L[i]; } 
  }
  void insert(double x,int idLn) //有序插入单独线段s[idLn]
  { int i; for(i=nL++-1;i>=0&&ps[idLn].less(ps[L[i]],x);i--)L[i+1]=L[i];L[i+1]=idLn;
  }
  void insert(double x,neigLine &LL) { for(int i=0;i<LL.nL;i++) insert(x,LL.L[i]); } 
};

enum PointType { left,right,middle };
struct eventElem { RealPoint rp; int size,seg[10]; PointType flag[10]; }; //复合事件点
class event //复合事件点进度表，从左到右、从上到下倒置存放事件点
  {private: eventElem pe[100]; int n;
   public:
   event(Line s[ ],int nn) { n=0; for(int i=0;i<nn;i++) insert(s[i],i); } //端点构造事件点表
   eventElem get( ) { return pe[--n]; } //取第一个复合事件点
   bool empty( ) const { return n==0; } //判断是否空表
   void insert(RealPoint rp,int LNo,PointType tp) //添加事件点rp的事件(rp,LL1,tp)
   {eventElem tmp={rp,0}; int i,j,m;
    for(i=0;i<n&&rp.x*10000+rp.y<pe[i].rp.x*10000+pe[i].rp.y;i++); //降序定位点rp
    if(i==n||fabs(rp.x*10000+rp.y-(pe[i].rp.x*10000+pe[i].rp.y))>=1e-3) //插入空白点
    {for(j=n++;j>i;j--) pe[j]=pe[j-1]; pe[i]=tmp; }
    for(m=pe[i].size,j=0;j<m;j++) if(pe[i].seg[j]==LNo) return; //已存在
    pe[i].seg[m]=LNo; pe[i].flag[m]=tp; pe[i].size=m+1; }
    void insert(RealPoint rp,Line s[ ],int LNo1,int LNo2) //添加线段交点
    {Point p(round(rp.x),round(rp.y)); PointType tp;
     tp=(p!=s[LNo1].p1)?(p!=s[LNo1].p2?middle:right):left; insert(rp,LNo1,tp);
     tp=(p!=s[LNo2].p1)?(p!=s[LNo2].p2?middle:right):left; insert(rp,LNo2,tp);
	}
    void insert(Line ss,int id) { insert(ss.p1,id,left); insert(ss.p2,id,right); } //添加端点
};
//--------------------------索引线段求交点并插入交点表和复合事件点进度表------------------
void interAndInsert(Line s[ ],int i,int j,RealPoint rp,set<Point>&A,event &E)
{RealPoint rpp; if(i==-1||j==-1||!interLine(s[i],s[j],rpp)) return;
 if(rpp.x>=rp.x+eps) {A.insert(Point(round(rpp.x),round(rpp.y))); E.insert(rpp,s,i,j); }
}
//----------Bentley Ottmann modified Algorithm for intersections -------
void BentleyOttmann(Line s[ ],int n,set<Point> &A) //多条非垂直线段求交
{  int i,iSup,iSdown,iL2up,iL2down; neigLine L(s,n),L2(s,n); //L2临时保存同点线段
   event E(s,n); eventElem ev; Point pp;
   while(!E.empty( ))
   {ev=E.get( ); L2.clear( ); //取复合事件点ev，清临时相邻线段表L2
   if(ev.size>1) { A.insert(Point(round(ev.rp.x),round(ev.rp.y))); } //多线段加交点
   for(i=0;i<ev.size;i++) //处理复合事件点，对事件点中的非结束线段添加L2线段
   {if(ev.flag[i]!=right) L2.insert(ev.rp.x,ev.seg[i]); }
   L.del(ev.rp); L.insert(ev.rp.x,L2); //L删去事件点中相关线段，L再添加L2
   if(L.inter(ev.rp )) A.insert(Point(round(ev.rp.x),round(ev.rp.y))); //ev交点则添加
   L.findUpDown(ev.rp,iSup,iSdown); //找事件点上下邻Sup、Sdown的索引(下标)
   if(L2.size( )==0) //L2空，则求Sup与Sdown在事件点右边的交点，加入A
   {interAndInsert(s,iSup,iSdown,ev.rp,A,E); }
   else //求L2最上线段与Sup、求L2最下线段与Sdown在事件点右边交点
   {L2.findMinMax(iL2up,iL2down); //找L2中的最上、最下线段L2up、L2down
    interAndInsert(s,iSup,iL2up,ev.rp,A,E);interAndInsert(s,iL2down,iSdown,ev.rp,A,E);
   }
   } 
}

