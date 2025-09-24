//图形程序ege3_3.cpp Sutherland-Hodgman算法裁剪多边形
//鼠标左击画折线，右击画封闭多边形，再右击裁剪多边形
# include <graphics.h>
struct Point { int x,y; };
void drawPoly(Point a[ ],int &n,bool leftdown,bool rightdown); //画折线和封闭多边形
void ClipPoly(Point a[ ],int &n); //裁剪函数，n为多边形顶点数
int left=100,top=50,right=400,bottom=300; //矩形窗口尺寸
int main( )
{
 initgraph(640,480,INIT_RENDERMANUAL);
 setbkcolor(WHITE); setcolor(RED); setfillcolor(GREEN);
 Point a[50]; int n=0; bool leftdown,rightdown; mouse_msg msg={0};
 bar(left,top,right,bottom); setlinestyle(SOLID_LINE,0,2);
 for( ; is_run( ) ; delay_fps(60) )
 {
  leftdown=rightdown=false;
  while(mousemsg( ) )
  {
   msg=getmouse( ); if(msg.is_left( )&&msg.is_down( ) ) leftdown=true; //按左键
   if(msg.is_right( )&&msg.is_down( ) ) rightdown=true; //按右键
  }
 cleardevice( ); bar(left,top,right,bottom); //画窗口
  drawPoly(a,n,leftdown,rightdown); //画折线或多边形或裁剪多边形
 }
 closegraph( ); return 0; 
}	
	
void drawPoly(Point a[ ],int &n,bool leftdown,bool rightdown)
{
 static int rButton=0; //连续右击的次数，左击则清零
 if(leftdown) //鼠标左击处理
 {
  if(rButton>0) { rButton=0; n=0; } //右击之后的左击，画折线前清多边形
  mousepos(&a[n].x,&a[n].y); n++; //记录顶点坐标
 }
 else if(rightdown) //鼠标右击处理
 {
  rButton++; //记录右击次数
  if(rButton==1) a[n++]=a[0]; //构成封闭折线
  if(rButton==2) ClipPoly(a,n); //第一次以后的右击则裁剪
 }
 moveto(a[0].x,a[0].y);
 for(int i=1;i<n;i++)lineto(a[i].x,a[i].y);//画多边形的边
}

void ClipPoly(Point a[ ],int &n)
{
 Point dir[4]={{-1,0},{0,-1},{1,0},{0,1}}; //边界left,top,right,bottom外法线
 Point ePt[4]={{left,0},{0,top},{right,0},{0,bottom}}; //边界上的一个点
 int n2,k,i; double t,ss,pp; Point v1,v2,pt,a2[50];
 for(k=0;k<4;k++) //分别对窗口边界left,top,right,bottom裁剪
 {
  v2.x=a[0].x-ePt[k].x; v2.y=a[0].y-ePt[k].y; //构造指向a[0]的向量
  pp=v2.x*dir[k].x+v2.y*dir[k].y; //内外判别式:>0外,<0内，与边界外法线内积
  for(n2=0,i=1;i<n;i++)
  {
   v1=v2; v2.x=a[i].x-ePt[k].x; v2.y=a[i].y-ePt[k].y; //构造指向a[i]的向量
   ss=pp; pp=v2.x*dir[k].x+v2.y*dir[k].y; //a[i]内外判别式
   if(ss*pp<0) //a[i-1]、a[i]在边界两侧
   {
    t=-ss/(pp-ss); //计算边界交点pt：a[i]-(1-t)(v2-v1)
    pt.x=a[i].x-(1-t)*(v2.x-v1.x);
    pt.y=a[i].y-(1-t)*(v2.y-v1.y);
    a2[n2++]=pt; //添加交点
   }
   if(pp<=0) { a2[n2++]=a[i]; } //添加内点
  }
  for(i=0;i<n2;i++) a[i]=a2[i]; //更新顶点表
  a[n2]=a[0]; n=n2+1; //构成封闭折线，更新n
 }
}	
