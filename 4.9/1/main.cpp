//图形程序ege5_2.cpp Jarvis算法画点集的凸壳(按y轴向上，屏幕画对称图)
//鼠标左击添加点，右击删除点；键盘按ESC键清除点集，按'j' 画点集的凸壳
# include <graphics.h>
# include <math.h>
struct Point
{
 int x,y;
 Point(int xx=0,int yy=0) { x=xx; y=yy; }
 Point operator-(Point b) const{ Point c(x-b.x,y-b.y); return c; } //向量减
 double operator*(Point b) const{ return(double)x*b.x+(double)y*b.y; } //内积
 bool operator!=(Point b)const{ return x!=b.x||y!=b.y; }
 double zCross(Point b) const{ return (double)x*b.y-(double)y*b.x; } //叉乘z坐标
};
bool getMessages(bool&mv,bool&ld,bool&rd,char&ch); //读取鼠标或键盘操作
void drawPoly(Point a[ ],int&n,Point b[ ],int&nc,bool ld,bool rd,bool move,char ch);
int main( )
{
 Point a[50],con[50]; int n=0,nc=0; bool move,leftdown,rightdown; char ch;
 initgraph(640,480,INIT_RENDERMANUAL); setbkcolor(WHITE); setcolor(BLUE);
 for( ; is_run( ) ; delay_fps(60))
 {
  if(!getMessages(move,leftdown,rightdown,ch)) continue;
  drawPoly(a,n,con,nc,leftdown,rightdown,move,ch); 
 }
 closegraph( ); return 0;
}

int searchDot(Point a[ ],int n,Point p) //点集中查找点p，找到返回a 的下标，否则-1
{
 for(int i=0;i<n;i++) { if((a[i]-p)*(a[i]-p)<=9) return i; }
 return -1;
}
void Jarvis(Point a[ ],int n,Point b[ ],int&nc); //点集a 生成凸壳顶点存入b
void refresh(Point a[ ],int n,Point b[ ],int nc); //画点集a和凸壳b
bool getMessages(bool&mv,bool&ld,bool&rd,char&ch)
{
 mouse_msg msg={0}; bool m=false; mv=ld=rd=false; ch='\0';
 while(mousemsg( )||kbhit( ) )
 {
  m=true; if(kbhit( ) ) { ch=getch( ); } //有键盘操作则读取字符
  if(mousemsg( ) )
  {
   msg=getmouse( );
   if(msg.is_move( ) ) mv=true;
   else if(msg.is_left( )&&msg.is_down( ) ) ld=true;
   else if(msg.is_right( )&&msg.is_down( ) ) rd=true; 
  }
 } 
 return m; 
}
void drawPoly(Point a[ ],int&n,Point b[ ],int&nc,bool ld,bool rd,bool move,char ch)
{
 if(ch==key_esc) { n=nc=0; cleardevice( ); } //按ESC键清除点集
 else if(ch=='j') { Jarvis(a,n,b,nc); refresh(a,n,b,nc); } //点集a 画凸壳
 else if(ld||rd)
 {
  Point p; mousepos(&p.x,&p.y); int k=searchDot(a,n,p);
  if(ld&&k<0) { a[n++]=p; } //左键添加点
  else if(rd&&k>=0) { n--; for(int i=k;i<n;i++) a[i]=a[i+1]; } //右键删除点
  nc=0; refresh(a,n,b,nc); 
 } 
}

Point vertex(Point a[ ],int n,Point p0,Point p1) //以p0->p1 为方向找a 中下一个凸壳点
{
 double tmax=-1,t,Lmax=0,L; Point d(0,-1),p2=p0,v; 
 if(p0!=p1) d=p1-p0;
 for(int i=0;i<n;i++)
 {
  if(a[i]!=p0&&a[i]!=p1) //找非p0、p1的点
  {
   v=a[i]-p1; L=v*v; t=v*d/sqrt(L*(d*d)); //计算p1到a[i]的向量与d的夹角余弦
   if(t>tmax||(fabs(t-tmax)<1e-7&&L>Lmax)) //找最大或最远夹角余弦点
    { p2=a[i]; tmax=t; Lmax=L; } 
  }
 } 
 return p2;
}
void Jarvis(Point a[ ],int n,Point b[ ],int&nc)
{
 int i; Point u0,u,v0,v1; nc=0;
 for(v0=a[0],i=1;i<n;i++) //找x、y字典序最小的点作为第一个凸壳点v0
 {if(a[i].x<v0.x||(a[i].x==v0.x&&a[i].y<v0.y)) v0=a[i]; }
 b[nc++]=v0; u0=u=v0; v1=vertex(a,n,u0,u); //找下一个凸壳点
 while(v1!=v0) { b[nc++]=v1; u0=u; u=v1; v1=vertex(a,n,u0,u); } //反复找凸壳点
}
void refresh(Point a[ ],int n,Point b[ ],int nc)
{
 cleardevice( );
 for(int i=0;i<n;i++) //画点集
 {
  int x=a[i].x,y=a[i].y; circle(x,y,4); 
  line(x-4,y-4,x+4,y+4); line(x-4,y+4,x+4,y-4);
 }
 if(nc==0) return; 
 setlinestyle(SOLID_LINE,0,2); setcolor(RED);
 moveto(b[nc-1].x,b[nc-1].y); for(int i=0;i<nc;i++) lineto(b[i].x,b[i].y); //画凸壳
 setlinestyle(SOLID_LINE,0,1); setcolor(BLUE); 
}
