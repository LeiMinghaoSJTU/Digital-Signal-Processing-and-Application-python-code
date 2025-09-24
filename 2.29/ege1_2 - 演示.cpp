//图形程序  ege1_2 - 演示.cpp
# include <graphics.h>
int main( )
{
	initgraph(640,480); 
	outtextxy(0,0,"计算机图形学");outtextxy(320,0,"outtextxy(0,0,\"计算机图形学\");");getch(); //(0,0)为左上角显示文字
	line(100,100,300,300); outtextxy(320,25,"line(100,100,300,300);");getch(); //(100,100)-(300,300)画直线段 
	circle(200,200,100); outtextxy(320,50,"circle(200,200,100);");getch();  //(200,200)为圆心，100为半径画圆
	rectangle(100,100,300,300);  outtextxy(320,75,"rectangle(100,100,300,300);");getch(); //(100,100)-(300,300)画矩形 
	cleardevice();  outtextxy(0,25,"cleardevice();");getch(); //清屏 
	int p[4*2]={300,50,100,396,500,396,300,50};  //多边形顶点坐标数组：头尾顶点重合 
	drawpoly(4,p); outtextxy(0,50,"drawpoly(4,p);");getch();  //画封闭图形
	xyprintf(100,400,"三角形：(%d,%d)-(%d,%d)-(%d,%d)",p[0],p[1],p[2],p[3],p[4],p[5]); //输出数据 
	outtextxy(0,75,"xyprintf(100,400,\"三角形：(%d,%d)-(%d,%d)-(%d,%d)\",p[0],p[1],p[2],p[3],p[4],p[5]);"); getch();
	closegraph(); 
	return 0; 
 } 
