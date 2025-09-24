# include <graphics.h>
struct Point { int x,y; };
bool getMessages(bool *pm,bool *pld,bool *prd,char *pch); //函数：读各种操作,有操作则true
void drawPoly(Point a[],int *psize,bool leftdown,bool rightdown,bool move,char ch);
int main( )
{
 Point a[50]={0}; int n=0; char ch='b';
 bool move,leftdown,rightdown;
 initgraph(640,480,INIT_RENDERMANUAL);
 setbkcolor(WHITE); setcolor(RED);
 for( ; is_run( ) ; delay_fps(60))
  {if(!getMessages(&move,&leftdown,&rightdown,&ch)) continue;
  drawPoly(a,&n,leftdown,rightdown,move,ch); //ch='s'实线，'c'虚线，'d'点线
  }
 closegraph(); return 0;
}
bool getMessages(bool *pm,bool *pld,bool *prd,char *pch)
 {
  mouse_msg msg={0}; bool m=false;
  *pm=*pld=*prd=false;
  while(mousemsg()||kbhit()) //是否有鼠标操作或按键操作，没有则结束循环
   {m=true; //标记有操作
    if(kbhit()) { *pch=getch(); } //若有键盘操作，则读取键盘
    if(mousemsg()) //若有鼠标操作，则进行下列处理
     {msg=getmouse(); //读取鼠标操作信息
      if(msg.is_move()) *pm=true; //记录鼠标移动
      else if(msg.is_left()&&msg.is_down()) *pld=true; //记录按下左键
      else if(msg.is_right()&&msg.is_down()) *prd=true; //记录按下右键
     }
   }
 return m; //返回是否测试到鼠标或键盘操作
}
void drawPoly(Point a[],int *psize,bool leftdown,bool rightdown,bool move,char ch)
{
 static bool start=true; //重画折线模式标志
 if(rightdown) { start=true; } //进入重画折线模式
 else
  {if(leftdown&&start) { *psize=0; start=false; } //重画模式按左键则清零
   if(start&&move) return; //重画模式移动则忽略
   if(!start) //非重画模式，则反复画折线
   {mousepos(&a[*psize].x,&a[*psize].y); //读取当前点
    if(leftdown) { (*psize)++; a[*psize]=a[*psize-1]; } //按左键则确认顶点
   }
  }
  if(ch=='s') setlinestyle(SOLID_LINE,0,1);
  else if(ch=='c') setlinestyle(CENTER_LINE,0,1);
  else if(ch=='d') setlinestyle(DOTTED_LINE,0,1);
  cleardevice(); moveto(a[0].x,a[0].y);
  for(int i=1;i<*psize;i++) lineto(a[i].x,a[i].y); //用选定的线型画折线
}
