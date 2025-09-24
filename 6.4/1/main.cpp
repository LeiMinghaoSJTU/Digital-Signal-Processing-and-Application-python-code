#include <windows.h>
#include <GL/glut.h>
#include <math.h>
#define degToArc(d) (d*3.14159265359/180)
void display()
{   glClearColor(1.0,1.0,1.0,1.0); //用白色清屏幕，第4参数是不透明度，1为不透明
	glClear(GL_COLOR_BUFFER_BIT); //清颜色缓冲区（屏幕） 
	glColor3f(1.0,1.0,0.0); //设置颜色：黄色 
	glBegin(GL_POLYGON); //设置图元：填充多边形 
	glVertex2f(-0.5,-0.5); //图元顶点坐标集合 
	glVertex2f(-0.5,0.5); glVertex2f(0.5,0.5); glVertex2f(0.5,-0.5);
	glEnd();
	glColor3f(0.0,0.0,1.0); //设置颜色：蓝色 
	glBegin(GL_TRIANGLES); //设置图元：填充三角形 
	glVertex2f(-0.3,-0.2); glVertex2f(0.3,-0.2); glVertex2f(0.0,0.32); glEnd(); 
	GLfloat x,y; glColor3f(0.0,1.0,0.0); //设置颜色：绿色 
	glBegin(GL_TRIANGLE_FAN); //设置图元：由三角扇形近似一个圆 
	glVertex2f(0.5,-0.5); glVertex2f(0.5+0.4,-0.5); 
	for(int i=10;i<=360;i+=10) 
	{ x=0.4*cos(degToArc(i)); y=0.4*sin(degToArc(i)); glVertex2f(0.5+x,-0.5+y); } 
	glEnd(); glFlush(); // glFlush() 用于将图元画到屏幕上
}
int main(int argc, char** argv)
{
glutInit(&argc,argv); //初始化glut
glutCreateWindow("Example 1"); //创建一个窗口，作为画图界面 
 glutDisplayFunc(display); //设置窗口执行的画图函数 
 glutMainLoop(); //使程序进入事件处理循环 
 return 0;
}
