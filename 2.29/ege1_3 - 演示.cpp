//图形程序  ege1_3 - 演示.cpp
# include <graphics.h>
void Mandelbrot();   //画分形图 Mandelbrot集 
int main( )
{
	initgraph(640,480); 
	setbkcolor(WHITE); setcolor(RED);  setfillcolor(GREEN);   //设置背景为白色，画图红色，填充绿色 
	bar(100,100,300,200);  outtextxy(320,0,"bar(100,100,300,200);"); getch(); //画无边框实心矩形 
	outtextxy(120,120,"无边框实心矩形"); outtextxy(320,25,"outtextxy(120,120,\"无边框实心矩形\");"); getch(); //带背景色输出文字 
	fillellipse(400,300,150,80); outtextxy(320,50,"fillellipse(400,300,150,80);"); getch(); //画有边框实心椭圆 
	setbkmode(TRANSPARENT);  outtextxy(320,75,"setbkmode(TRANSPARENT);"); getch(); //设置文字透明背景 
	outtextxy(350,300,"有边框实心椭圆"); outtextxy(320,100,"outtextxy(350,300,\"有边框实心椭圆\");"); //背景透明输出文字 
	getch();  cleardevice();  Mandelbrot();  getch(); 
	closegraph();
	return 0; 
 } 
 void Mandelbrot()
 { 	color_t c[6]={0xFF0000,0xFF,0xFF00,0xFF00FF,0xFFFF00,0xFFFF};//红蓝绿紫黄青 
 	int i,j,n,w=640,h=480,wc=411,hc=240;  double x,y,t,cx,cy,d=3.0/h;  
	for(i=0;i<w;i++) for(j=0;j<h;j++)
	{	cx=(i-wc)*d;  cy=(j-hc)*d;  x=y=0;
		for(n=100;n>0;n--) {t=x*x-y*y+cx; y=2*x*y+cy; x=t; if(x*x+y*y>16) break;}
		putpixel(i,j,n>0?c[n%6]:EGERGB(0,0,0));  //画点 
	 } 
 }
