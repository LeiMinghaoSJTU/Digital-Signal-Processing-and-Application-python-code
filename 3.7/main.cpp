#include <graphics.h>
void LineBresenham(int x1,int y1,int x2,int y2); 
int main( )
 {initgraph(640,480,INIT_RENDERMANUAL);
  setbkcolor(WHITE);
  int x1,y1,x2,y2;
  bool move,leftdown;
  mouse_msg msg={0}; 
  for( ; is_run( ) ; delay_fps(60) )
   {
    move=leftdown=false;
	while(mousemsg( ))
	{
	 msg=getmouse( ); 
	 if(msg.is_move( )) move=true; 
	 if(msg.is_left( )&&msg.is_down( )) leftdown=true; 
	 }
	if( ! keystate(key_mouse_l) ) continue;
	if(leftdown ) { x1=x2=msg.x; y1=y2=msg.y; } 
	else if(move) { x2=msg.x; y2=msg.y; }
	cleardevice( ); 
	LineBresenham(x1,y1,x2,y2);
	}
   closegraph( ); 
   return 0;
   }
   
void LineBresenham(int x1,int y1,int x2,int y2)
{
 int dx=1,dy=1,deltax=x2-x1,deltay=y2-y1,p,x=x1,y=y1,i;
 if(deltax<0) { dx=-1; deltax=-deltax; }
 if(deltay<0) { dy=-1; deltay=-deltay; } 
 if(deltax>=deltay) 
  {
   for(p=2*deltay-deltax,i=0;i<=deltax; i++)
    {putpixel(x,y,RED); 
	 x+=dx;
	 if(p>=0) { y+=dy; p-=2*deltax; }
	 p+=2*deltay; 
	 }
  }
  else // x坐标与y坐标交换，deltax与deltay，dx与dy交换
  {
   for(p=2*deltax-deltay,i=0;i<=deltay; i++)
    {
	 putpixel(x,y,RED); 
	 y+=dy; 
	 if(p>=0) { x+=dx; p-=2*deltay; } 
	 p+=2*deltax; 
	 }
   }
}
