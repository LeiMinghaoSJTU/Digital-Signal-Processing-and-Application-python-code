#include <graphics.h>
int main() {
initgraph(640,480,INIT_RENDERMANUAL); 
const char *p; setbkcolor(WHITE); setcolor(BLUE); setfont(50,0,"宋体"); char ch='\0';
for( ; ch!=key_esc ; delay_fps(60) ) //按ESC键退出消息循环
 {if( kbhit( ) ) ch=getch( ); //检测并读取键盘
  if(ch=='A') p="苹果"; else if(ch=='B') p="香蕉"; else p="其它";outtextxy(160,125,p);}
  closegraph( ); return 0;}

