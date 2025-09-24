# include <windows.h> 
#include <GL/glut.h> 
#include <math.h>
GLfloat r=0.3,x=0.3,y=0.0,sita=0.0; //平移值：x和y，旋转角度：sita（角度制） 
GLint selection=3; //菜单选择：1 平移 2 旋转 3 停止 
void myidle( ) ; //空闲函数代码，本程序中用以产生动画 
void display(void) ; //画图的各种操作代码 
void mymenu(int input) 
{ selection=input; glutPostRedisplay(); //通过消息调用display函数进行窗口重画 
} 
int main(int argc,char **argv)
{ 
  glutInit(&argc,argv); glutInitWindowPosition(300,100); //设置创建的窗口左上角在屏幕中的位置
  glutInitWindowSize(600,600); //设置创建的窗口的大小 
  glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE); //使用双缓冲器画动画 
  glutCreateWindow("Example 2"); glutDisplayFunc(display); 
  glutIdleFunc(myidle); //设置空闲函数用于产生动画 
  glutCreateMenu(mymenu); //创建菜单：菜单处理函数 mymenu 
  glutAddMenuEntry("Translate",1); //添加菜单项：菜单项标题，菜单函数参数 
  glutAddMenuEntry("Rotate",2); 
  glutAddMenuEntry("Stop",3); 
  glutAttachMenu(GLUT_RIGHT_BUTTON); //点击鼠标右键弹出菜单 
  glutMainLoop(); return 0; 
}
//通过坐标变换设计动画
void myidle() //空闲函数，用于实现动画
{ static int k=0; //绕中心半径为0.3的圆逆时针平移图像，平移点的角度(角度制)
if(selection==1) { x=r*cos(3.1416*k/180); y=r*sin(3.1416*k/180); k=(k+1)%360; }
else if(selection==2) { sita+=2.0; if(sita>360.0) sita-=360; }
Sleep(10); //延迟10毫秒
glMatrixMode(GL_MODELVIEW); //设置模型视图变换
glLoadIdentity(); //变换矩阵清为单位矩阵（无变换）
if(selection==1) glTranslatef(x,y,0.0); //平移变换：平移值：x,y,0
else if(selection==2) glRotatef(sita,0.0,0.0,1.0); //旋转变换：绕z轴旋转sita角
glutPostRedisplay();
}
void display(void) //画图函数
{ glClear(GL_COLOR_BUFFER_BIT); glColor3f(1.0,1.0,0.0);
glBegin(GL_POLYGON);
glVertex2f(-0.5,-0.5); glVertex2f(-0.5,0.5); glVertex2f(0.5,0.5);glVertex2f(0.5,-0.5);
glEnd(); glColor3f(0.0,0.0,1.0);
glBegin(GL_TRIANGLES); glVertex2f(-0.3,-0.2);glVertex2f(0.3,-0.2);glVertex2f(0.0,0.32);
glEnd(); glFlush(); glutSwapBuffers(); //切换画好图案的屏幕缓冲器
}
