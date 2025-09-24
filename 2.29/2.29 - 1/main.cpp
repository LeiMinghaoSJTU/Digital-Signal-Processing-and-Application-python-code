#include <graphics.h>
int main() {
	initgraph(640,480); //宽度和长度，如果要满屏则输入-1 
//	outtextxy(100,100,"line"); //在某个位置显示文字
//	line(0,0,200,250); 
	circle(200,200,100);
	getch(); 
	closegraph();
	return 0;
}
