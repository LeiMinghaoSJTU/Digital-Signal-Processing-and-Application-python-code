//图形程序ege3_2.cpp Cohen-Sutherland算法裁剪直线段//鼠标拖拽画直线段，按窗口进行裁剪
# include <graphics.h>
void ClipLine(int x1,int y1,int x2,int y2); //裁剪函数
int left=100,top=50,right=400,bottom=300; //矩形窗口尺寸
int main( )
{
 initgraph(640,480,INIT_RENDERMANUAL);
 setbkcolor(WHITE); setcolor(RED); setfillcolor(GREEN);
 bar(left,top,right,bottom);
 int x1,y1,x2,y2; bool move,leftdown; mouse_msg msg={0};
 for( ; is_run( ) ; delay_fps(60) )
 {
  move=leftdown=false;
  while(mousemsg( ) )
  {
   msg=getmouse( ); if(msg.is_move( ) ) move=true;
   if(msg.is_left( )&&msg.is_down( ) ) leftdown=true; 
  }
  if(!keystate(key_mouse_l)) continue;
  if(leftdown) { x1=x2=msg.x; y1=y2=msg.y; }
  else if(move) { x2=msg.x; y2=msg.y; }
  cleardevice( ); bar(left,top,right,bottom); ClipLine(x1,y1,x2,y2);
 } 
 closegraph( ); return 0;
}

int Code(int x,int y) //计算端点编码
{
 int ret=y<top?8:(y>bottom?4:0);
 if(x>right) ret+=2;
 else if(x<left) ret+=1;
 return ret;
}

void ClipLine(int x1,int y1,int x2,int y2) //裁剪函数
{
 int xx,yy;
 for(int i=1;i<=5;i++) //裁剪过程最多4次，加上最后一次判别，最多五次循环
 {
  if( Code(x1,y1)==0 &&Code(x2,y2)==0 ){ line(x1,y1,x2,y2); break; }
  if( (Code(x1,y1)&Code(x2,y2) )!=0) break;
  int &px=(Code(x1,y1)!=0)?x1:x2; 
  int &py=(Code(x1,y1)!=0)?y1:y2;
  if( (Code(px,py)&8)!=0 ) { yy=top; xx=x1+(yy-y1)*(x2-x1)/(y2-y1); }
  else if( (Code(px,py)&4)!=0 ){ yy=bottom; xx=x1+(yy-y1)*(x2-x1)/(y2-y1); }
  else if( (Code(px,py)&2)!=0 ){ xx=right; yy=y1+(xx-x1)*(y2-y1)/(x2-x1); }
  else { xx=left; yy=y1+(xx-x1)*(y2-y1)/(x2-x1); }
  px=xx; py=yy;
 }
}
