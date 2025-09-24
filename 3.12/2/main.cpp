# include <graphics.h>
void EllipseMidpoint(int x1,int y1,int x2,int y2); 
int main( )
{
 initgraph(640,480,INIT_RENDERMANUAL); 
 setbkcolor(WHITE); int x1,y1,x2,y2; 
 bool move,leftdown; mouse_msg msg={0}; 
 for( ; is_run( ) ; delay_fps(60) )
  {
  move=leftdown=false;
  while(mousemsg( ) ) 
   {
   msg=getmouse( ); 
   if(msg.is_move( )) move=true; 
   if(msg.is_left( )&&msg.is_down( )) leftdown=true; 
   }
   if(!keystate(key_mouse_l)) continue;
   if(leftdown) { x1=x2=msg.x; y1=y2=msg.y; } 
   else if(move) { x2=msg.x; y2=msg.y; }
   cleardevice( ); 
   EllipseMidpoint(x1,y1,x2,y2);
   }
   closegraph( ); 
   return 0;
}

void EllipseMidpoint(int x1,int y1,int x2,int y2)
{
 int a=(x2-x1)/2,b=(y2-y1)/2, xc=(x1+x2)/2,yc=(y1+y2)/2; //a水平半轴，b垂直半轴
 int x,y,a2=a*a,b2=b*b; int d1,d2;
 if(a<0) a= -a; 
 if(b<0) b= -b;
 x=0; y=b; d1=b2-a2*b+a2/4;
 while( 2*b2*(x+1)<2*a2*y-a2 ) //A区向右画弧
  {
  putpixel(xc+x,yc+y,RED); putpixel(xc-x,yc+y,RED); putpixel(xc+x,yc-y,RED); putpixel(xc-x,yc-y,RED); 
  if(d1>=0) { d1+=a2*(2-2*y); y--; } 
  d1+=b2*(3+2*x); x++;
  }
  d2=b2*(x*x+x)+a2*(y-1)*(y-1)-a2*b2+b2/4; //B区的起始位置
  while(y>=0) //B区向下画弧
  {
  putpixel(xc+x,yc+y,RED); putpixel(xc-x,yc+y,RED); putpixel(xc+x,yc-y,RED); putpixel(xc-x,yc-y,RED); 
  if(d2<0) { d2+=b2*(2+2*x); x++; } 
  d2+=a2*(3-2*y); y--;
  }
}
