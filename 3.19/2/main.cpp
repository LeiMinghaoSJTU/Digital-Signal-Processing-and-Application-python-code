//图形程序ege3_1.cpp 折线的平移与旋转
//鼠标左键拖拽画折线、平移、旋转//键盘按键选择功能：'d' –画折线、'm' –平移、'r' –旋转
# include <graphics.h>
# include <math.h>
struct Point { int x,y; }; //屏幕像素点类型
bool getMessages(bool *pmove,bool*pleftdown,bool*prightdown,char*pch); //记录一批信息
void drawPoly(Point a[ ],Point b[ ],int* psize,bool leftdown,bool rightdown); //画折线
void moving(Point a[ ],Point b[ ],int n,bool leftdown,bool move,Point* ppre); //平移
void rotate(Point a[ ],Point b[ ],int n,bool leftdown,bool move,Point base[ ]); //旋转

int main( )
{
//a保存原始顶点，b保存显示顶点(平移旋转时用)，base为旋转基点和起始点
Point a[50]={0},b[50]={0},pre={0,0},base[2]={0}; int n=0; 
bool move,leftdown,rightdown; char ch='d';
initgraph(640,480,INIT_RENDERMANUAL); //INIT_RENDERMANUAL为渲染模式，可提高动画效果
setbkcolor(WHITE); setcolor(RED);
for( ; is_run( ) ; delay_fps(60) )
 {
 if(!getMessages(&move,&leftdown,&rightdown,&ch)) continue;
 switch(ch) //键盘字符ch用来选择画折线、平移还是旋转
 {
  case 'd': drawPoly(a,b,&n,leftdown,rightdown); break; //画折线
  case 'm': moving(a,b,n,leftdown,move,&pre); break; //平移
  case 'r': rotate(a,b,n,leftdown,move,base); break; //旋转
 }
 }
closegraph( );
return 0;
}

bool getMessages(bool *pmove,bool*pleftdown,bool*prightdown,char*pch)
{
 mouse_msg msg={0}; bool m=false;
 *pmove=*pleftdown=*prightdown=false;
 while(mousemsg( )||kbhit( ) ) //检测一批鼠标或键盘消息
 {m=true;
  if(kbhit( ) ) { *pch=getch( ); } //读取键盘消息
  if(mousemsg( ) )
   {msg=getmouse( );
   if(msg.is_move( ) ) *pmove=true; //有移动消息
   else if(msg.is_left( )&&msg.is_down( ) ) *pleftdown=true; //有按左键消息
   else if(msg.is_right( )&&msg.is_down( ) ) *prightdown=true; //有按右键消息
   }
 }
 return m;
}

void refresh(Point a[],int n) //重画折线
{
 cleardevice( ); moveto(a[0].x,a[0].y);
 for(int i=1;i<n;i++) lineto(a[i].x,a[i].y);
}

void drawPoly(Point a[ ],Point b[ ],int* psize,bool leftdown,bool rightdown)
{
 if(rightdown) { *psize=0; refresh(a,0); } //按右键重画
 else if(leftdown) //按左键增加折线顶点
 {
  mousepos(&a[*psize].x,&a[*psize].y); (*psize)++; //将鼠标位置记录到数组a[]中 
  for(int i=0;i<*psize;i++) b[i]=a[i]; refresh(b,*psize); //更新显示数据并画折线（这里还 
 }
}

void moving(Point a[ ],Point b[ ],int n,bool leftdown,bool move,Point* ppre)
{
 if(leftdown) //按左键取得平移起始点*ppre并确认显示数据
 {
  refresh(b,n); mousepos(&(ppre->x),&(ppre->y));
  for(int i=0;i<n;i++) a[i]=b[i]; //更新折线原始数据
 }
 else if(keystate(key_mouse_l)&&move) //按下左键移动则平移折线
 {
  int x,y; mousepos(&x,&y); x=x-ppre->x; y=y-ppre->y; //获取平移量
  for(int i=0;i<n;i++) { b[i].x=a[i].x+x; b[i].y=a[i].y+y; } refresh(b,n); //画折线
 }
}

void rotate(Point a[ ],Point b[ ],int n,bool leftdown,bool move,Point base[ ])
{
 static int idx=0; //记录取得旋转基点(0)还是旋转起始点(1)
 if(leftdown) //取旋转基点或旋转起始点并确认显示数据
 {
  if(idx==2) idx=0; mousepos(&base[idx].x,&base[idx].y); idx++; //循环取点
  for(int i=0;i<n;i++) a[i]=b[i]; //更新折线原始数据
 }
 else if(keystate(key_mouse_l)&&move&&idx==2) //取好基点起始点且左键移动
 {
  int x,y; double t1,t2,c,s,xx1,yy1,xx2,yy2;
  mousepos(&x,&y); //取旋转终止点
  xx1=base[1].x-base[0].x; yy1=base[1].y-base[0].y; //取基点到起始点向量
  xx2=x-base[0].x; yy2=y-base[0].y; //取基点到终止点向量
  t1=sqrt(xx1*xx1+yy1*yy1); t2=sqrt(xx2*xx2+yy2*yy2);
  c=(xx1*xx2+yy1*yy2)/(t1*t2); s=sqrt(1-c*c); //求得向量夹角的余弦和正弦
  if(xx1*yy2-xx2*yy1<0) s=-s; //旋转超过180度或反向旋转，叉乘确定sin正负
  for(int i=0;i<n;i++)
  {
   xx1=a[i].x-base[0].x; yy1=a[i].y-base[0].y; //取基点到顶点向量
   b[i].x=xx1*c-yy1*s+base[0].x; b[i].y=xx1*s+yy1*c+base[0].y; //绕基点转
  }
  refresh(b,n);
 }
}
