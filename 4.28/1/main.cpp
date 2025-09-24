//图形程序ege6_1.cpp 画分形图案
//键盘按'k' 画Koch 曲线，按's' 画Sierpinski 三角，按'j' 画Julia 集，
//画Julia 集状态下，鼠标右击输入Julia 集参数(一个复数)
# include <graphics.h>
# include <stdio.h>
struct Point { int x,y; };
void koch(Point p0,Point p1); //画从p0 到p1 的Koch 曲线
void sierpinski(Point p0,Point p1,Point p2); //画p0,p1,p2三点构成的Sierpinski 三角
void julia(double re,double im); //画参数为复数re+im*i 的Julia 集
int main( )
{
 Point p0={80,430},p1={420,50},p2={560,430};
 bool rightdown; char kbstate='k',kbmsg; //kbstate记录按键状态，kbmsg记录消息
 double re=0.35,im=0.4; //记录Julia 集的参数的实部re 和虚部im
 initgraph(640,480,INIT_RENDERMANUAL);
 setbkcolor(WHITE); setcolor(BLUE); mouse_msg msg;
 outtextxy(10,10,"Koch曲线"); koch(p0,p2); //初始画Koch 曲线
 for( ; is_run( ) ; delay_fps(60))
 {
  kbmsg='\0'; if(kbhit( ) ) { kbstate=kbmsg=getch( ); } //读取键盘按键消息
  rightdown=false;
  while(mousemsg( ) ) //读鼠标{ msg=getmouse( ); if(msg.is_right( )&&msg.is_down( ) ) rightdown=true; }
  if(kbmsg=='k') // 按'k' 键
   { cleardevice( ); outtextxy(10,10,"Koch曲线"); koch(p0,p2); }
  else if(kbmsg=='s') //按's' 键
   { cleardevice( ); outtextxy(10,10,"Sierpinski三角"); sierpinski(p0,p1,p2); }
  else if(kbmsg=='j'||(kbstate=='j'&&rightdown)) //按'j' 键或'j' 键状态鼠标右击
   {if(rightdown)
    {const char *ps="输入一个复数：\n如-3+2.4i、0.1-1.3i、3.1+0i、0-2.7i等";
     char str[30]; inputbox_getline(0,ps,str,30); //输入字符串形式的复数
     sscanf(str,"%lf%lf",&re,&im); //从字符串读取复数实部和虚部
    }
   cleardevice( ); julia(re,im);xyprintf(10,10,"Julia集：参数%.2f%s%.2f i",re,(im<0?"":"+"),im);
   }
 }
 closegraph( );
 return 0;
}
void koch(Point p0,Point p1)
{
 Point p2,p3,p4,pt={p1.x-p0.x,p1.y-p0.y}; double v3=1.73205080756888/6; //sqrt(3)/6
 if( pt.x*pt.x+pt.y*pt.y<=2 ) { line(p0.x,p0.y,p1.x,p1.y); return; } //直接画直线
 p2.x=(2*p0.x+p1.x)/3; p2.y=(2*p0.y+p1.y)/3;
 p4.x=(p0.x+2*p1.x)/3; p4.y=(p0.y+2*p1.y)/3;
 p3.x=(p0.x+p1.x)/2+pt.y*v3; p3.y=(p0.y+p1.y)/2-pt.x*v3; //y轴向下
 koch(p0,p2); koch(p2,p3); koch(p3,p4); koch(p4,p1); //递归画Koch曲线
}
void sierpinski(Point p0,Point p1,Point p2)
{
 int i,k,x,y; Point p[3]={p0,p1,p2};
 for(x=p0.x,y=p0.y,i=1;i<=100000;i++) //循环100000次随机均匀画三角上的点
 {k=rand( )%3; x=(x+p[k].x)/2; y=(y+p[k].y)/2; putpixel(x,y,BLUE); }
}
void julia(double re,double im)
{
 int x,y,k,w=640,h=480; double sx=w/2.0,sy=h/2.0,xx,yy,tt;
 for(x=0;x<w;x++) for(y=0;y<h;y++)
 {xx=4*(x-sx)/w; yy=4*(sy-y)/h; //屏幕点对应到复数xx+yy*i ，y轴向下
  for(k=20;k>0;k--)
  {tt=xx*xx-yy*yy+re; yy=2*xx*yy+im; xx=tt; if(xx*xx+yy*yy>25) break; }
  if(k==0) putpixel(x,y,BLUE); //xx+yy*i点构成了有限序列
 }
}
