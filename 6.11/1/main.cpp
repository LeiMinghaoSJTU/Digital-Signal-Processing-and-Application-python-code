#include <windows.h>
#include <GL/glut.h>
#include <math.h>
#define degToArc(d) (d*3.14159265359/180)
// GL04.cpp 画动态旋转的Bezier曲面 
GLfloat sita=0; 
void drawCoordSys( ) , drawSurface( ) ;
void display() 
{ glClear(GL_COLOR_BUFFER_BIT); glMatrixMode(GL_MODELVIEW); 
glLoadIdentity(); glOrtho(-4,4,-4,4,4,-4); //设置裁剪区域 
glRotatef(sita,1.0,1.0,1.0); //绕过原点的向量 (1.0 , 1.0 , 1.0) 旋转sita 
drawCoordSys(); drawSurface(); //画坐标轴、画Bezier曲面 
glFlush(); glutSwapBuffers(); //双缓冲显示 
} 
void myidle() 
{ sita+=1; if(sita>=360) sita-=360; Sleep(30); glutPostRedisplay(); } 
int main(int argc,char **argv) 
{ glutInit(&argc,argv); glutInitWindowSize(600,600); 
glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE); 
glutCreateWindow("Example 4"); 
glutDisplayFunc(display); 
glutIdleFunc(myidle); 
glutMainLoop(); 
return 0; }
GLfloat a[4][4][3]={ {{-1.5,-1.5,4.0},{-0.5,-1.5,2.0},{0.5,-1.5,-1.0},{1.5,-1.5,2.0}}, 
{{-1.5,-0.5,1.0},{-0.5,-0.5,3.0},{0.5,-0.5,0.0},{1.5,-0.5,-1.0}}, 
{{-1.5,0.5,4.0},{-0.5,0.5,0.0},{0.5,0.5,3.0},{1.5,0.5,4.0}}, 
{{-1.5,1.5,-2.0},{-0.5,1.5,-2.0},{0.5,1.5,0.0},{1.5,1.5,-1.0}}}; 
void drawCoordSys() //画坐标轴 
{ glColor3f(1,0,0); glBegin(GL_LINES); 
glVertex3f(-1,0,0); glVertex3f(3,0,0); glEnd(); 
glColor3f(0,1,0); glBegin(GL_LINES); 
glVertex3f(0,-1,0); glVertex3f(0,3,0); glEnd(); 
glColor3f(0,1,1); glBegin(GL_LINES); 
glVertex3f(0,0,-1); glVertex3f(0,0,3); glEnd(); }
void drawSurface() //由4×4个点画出Bezier曲面 
{ glColor3f(1,1,0); glEnable(GL_MAP2_VERTEX_3); //启用二维求值器
 // 由数组a中的4×4个顶点生成二维求值器，u,v均是4阶(3次)，间隔元素为3,12 
 glMap2f(GL_MAP2_VERTEX_3,0.0,1.0,3,4,0.0,1.0,12,4,&a[0][0][0]); //v间隔1行 
 glMapGrid2f(20,0.0,1.0,20,0.0,1.0); //利用二维求值器计算曲面分点(u,v都20等分) 
 glEvalMesh2(GL_LINE,0,20,0,20); //利用计算出的分点画出曲面网格
 }
 void Bezier4(GLfloat *p0,GLfloat *p1,GLfloat *p2,GLfloat *p3) //4点画曲线 
 { GLfloat p[4][3]; int m=3*sizeof(GLfloat); 
 memcpy(p[0],p0,m); memcpy(p[1],p1,m); memcpy(p[2],p2,m); memcpy(p[3],p3,m); 
 glMap1f(GL_MAP1_VERTEX_3,0.0,1.0,3,4,&p[0][0]); //设置一维求值器 
 glMapGrid1f(20,0.0,1.0);  //利用一维求值器计算Bezier曲线分点 
 glEvalMesh1(GL_LINE,0,20); //绘制求值器计算出的分点 
 }
/* void drawBezier( ) //多点画Bezier曲线，中间插入分点 
 { GLfloat b1[3],b2[3]; int i,j; glColor3f(1,0,1); 
 for(memcpy(b1,a[0],3*sizeof(GLfloat)),i=0;i+2<=n-1;i+=2) 
 { if(i+3==n-1) { Bezier4(b1,a[i+1],a[i+2],a[i+3]); } //只剩4点：b1,ai+1,ai+2,ai+3 
 else if(i+2==n-1) //只剩3点：b1,ai+1,ai+2，在ai+1和ai+2中补一点b2 
 { for(j=0;j<3;j++) b2[j]=(a[i+1][j]+a[i+2][j])/2; Bezier4(b1,a[i+1],b2,a[i+2]); }
  else //起码i+4==n-1，即至少还剩5点：b1,ai+1,ai+2,ai+3,ai+4 ，至少有两个分段 
  { for(j=0;j<3;j++) b2[j]=(a[i+2][j]+a[i+3][j])/2; //ai+2,ai+3中补一点b2 
  Bezier4(b1,a[i+1],a[i+2],b2); memcpy(b1,b2,3*sizeof(GLfloat)); } } 
  glFlush(); } 

void display( ) //画图函数：画顶点、折线、Bezier曲线 
{ int i; glClear(GL_COLOR_BUFFER_BIT); glColor3f(1,1,0); glBegin(GL_LINE_STRIP); //画折线 
for(i=0;i<n;i++) glVertex3fv(a[i]); glEnd(); glColor3f(0,1,0); glPointSize(5.0); //设置画点的大小
 glBegin(GL_POINTS); //画点
  for(i=0;i<n;i++) glVertex3fv(a[i]); glEnd(); drawBezier(); }
  */
