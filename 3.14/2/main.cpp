# include <graphics.h>
void Boundaryfill(int x,int y,color_t fill, color_t bd); //种子填充函数
int main( )
{
 initgraph(640,480); setbkcolor(WHITE); setcolor(RED); 
 circle(200,200,50); getch( );
 Boundaryfill(200,200,GREEN,RED); getch( ); 
 closegraph( ); return 0;
 } 
void Boundaryfill(int x,int y,color_t fill, color_t bd)
{
 color_t color=getpixel(x,y)&0xFFFFFF; //取(x,y)点的像素颜色清废弃字节
 fill=fill&0xFFFFFF; bd=bd&0xFFFFFF; //清颜色值的废弃字节
 if(color!=fill&&color!=bd)
 {
  putpixel(x,y,fill); Boundaryfill(x,y-1,fill,bd); 
  Boundaryfill(x,y+1,fill,bd); Boundaryfill(x-1,y,fill,bd); 
  Boundaryfill(x+1,y,fill,bd); 
  }
}
