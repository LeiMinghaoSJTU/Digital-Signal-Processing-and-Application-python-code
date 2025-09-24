#include <graphics.h>
int main() {
initgraph(640,480,INIT_RENDERMANUAL);
setbkcolor(WHITE); 
setcolor(BLUE); 
setlinestyle(SOLID_LINE,0,3); //设置画线类型为宽度为3的实线
int x1,y1,x2,y2; bool move,leftdown; mouse_msg msg={0}; //定义鼠标消息变量
for( ; is_run( ) ; delay_fps(60) )
{move=leftdown=false; //记录移动和按下左键消息的变量初始化为false
  while(mousemsg( ) ) //反复检测并读取鼠标消息
   {msg=getmouse( ); if(msg.is_move( )) move=true; //有移动操作
    if(msg.is_left( )&&msg.is_down( )) leftdown=true; //有按下左键操作
   }
if(!keystate(key_mouse_l)) continue; //左键未按下则忽略 
if(leftdown) { x1=x2=msg.x; y1=y2=msg.y; } //按下左键操作，两点重叠
else if(move) { x2=msg.x; y2=msg.y; } //移动操作，改动第二点
cleardevice( ); line(x1,y1,x2,y2);}
closegraph( ); return 0;
}
