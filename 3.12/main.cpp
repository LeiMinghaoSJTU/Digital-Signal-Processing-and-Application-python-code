# include <graphics.h>
# include <math.h>
void CircleBresenham(int xc,int yc,int x2,int y2); 
int main( )
 {
 initgraph(640,480,INIT_RENDERMANUAL); 
 setbkcolor(WHITE); 
 int xc,yc,x2,y2; 
 bool move,leftdown; 
 mouse_msg msg={0}; 
 for( ; is_run( ) ; )
  {
  move=leftdown=false;
  while(mousemsg( ) ) 
   {
   msg=getmouse( ); 
   if(msg.is_move( )) move=true; 
   if(msg.is_left( )&&msg.is_down( )) leftdown=true; 
   }
   if(!keystate(key_mouse_l)) continue; 
   if(leftdown ) { xc=x2=msg.x; yc=y2=msg.y; } 
   else if(move) { x2=msg.x; y2=msg.y; } 
   cleardevice( ); 
   CircleBresenham(xc,yc,x2,y2);
   }
   closegraph( ); 
   return 0;
   }
void CircleBresenham(int xc,int yc,int x2,int y2)
{
 int a=x2-xc,b=y2-yc,r,x,y,p; 
 r=int(sqrt(double(a*a+b*b))+0.5); x=0; y=r; p=3-2*r;
 while(x<=y)
  {
  putpixel(xc+x,yc+y,RED); 
  putpixel(xc-x,yc+y,RED);
  putpixel(xc+x,yc-y,RED); 
  putpixel(xc-x,yc-y,RED);
  putpixel(xc+y,yc+x,RED); 
  putpixel(xc-y,yc+x,RED);
  putpixel(xc+y,yc-x,RED); 
  putpixel(xc-y,yc-x,RED);
  if(p>=0) { p+=4-4*y; y--; }p+=6+4*x; x++;}
}
