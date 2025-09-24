# include <windows.h> 
#include <GL/glut.h> 
#include <math.h>
// GL03.cpp 鼠标左击画Bezier曲线 
GLfloat a[20][3]; int n=0; void display( ); //画图函数：画顶点、折线、Bezier曲线 
void mouse(int button,int state,int x,int y) //鼠标消息处理函数 
{ if(button==GLUT_RIGHT_BUTTON&&state==GLUT_DOWN) //按下右键 
{ n=0; glutPostRedisplay(); return; } 
if(button!=GLUT_LEFT_BUTTON||state!=GLUT_DOWN) return; //没按下左键 
if(n==20) return; GLint viewport[4]; GLfloat xx,yy; glGetIntegerv(GL_VIEWPORT,viewport); //获得窗口视区的位置和大小 
xx=2.0*x/viewport[2]-1.0; yy= -(2.0*y/viewport[3]-1.0); a[n][0]=xx; a[n][1]=yy; a[n][2]=0.0; n++; glutPostRedisplay(); } 
int main(int argc,char **argv) 
{ glutInit(&argc,argv); glutInitWindowSize(800,400); glutCreateWindow("Example 3");
 glutDisplayFunc(display); glutMouseFunc(mouse); //设置鼠标处理函数 
 glEnable(GL_MAP1_VERTEX_3); //启用一维求值器 
 glutMainLoop(); return 0; }
 
 void Bezier4(GLfloat *p0,GLfloat *p1,GLfloat *p2,GLfloat *p3) //4点画曲线 
 { GLfloat p[4][3]; int m=3*sizeof(GLfloat); memcpy(p[0],p0,m); 
 memcpy(p[1],p1,m); memcpy(p[2],p2,m); memcpy(p[3],p3,m);
  glMap1f(GL_MAP1_VERTEX_3,0.0,1.0,3,4,&p[0][0]); //设置一维求值器 
  glMapGrid1f(20,0.0,1.0); //利用一维求值器计算Bezier曲线分点 
  glEvalMesh1(GL_LINE,0,20); //绘制求值器计算出的分点 
  }
void drawBezier( ) //多点画Bezier曲线，中间插入分点
 { GLfloat b1[3],b2[3]; int i,j; glColor3f(1,0,1);
  for(memcpy(b1,a[0],3*sizeof(GLfloat)),i=0;i+2<=n-1;i+=2) 
  { if(i+3==n-1) { Bezier4(b1,a[i+1],a[i+2],a[i+3]); } //只剩4点：b1,ai+1,ai+2,ai+3 
  else if(i+2==n-1) //只剩3点：b1,ai+1,ai+2，在ai+1和ai+2中补一点b2 
  { for(j=0;j<3;j++) b2[j]=(a[i+1][j]+a[i+2][j])/2; Bezier4(b1,a[i+1],b2,a[i+2]); } 
  else //起码i+4==n-1，即至少还剩5点：b1,ai+1,ai+2,ai+3,ai+4 ，至少有两个分段 
  { for(j=0;j<3;j++) b2[j]=(a[i+2][j]+a[i+3][j])/2; //ai+2,ai+3中补一点b2 
  Bezier4(b1,a[i+1],a[i+2],b2); memcpy(b1,b2,3*sizeof(GLfloat)); } } glFlush(); } 
  
  void display( ) //画图函数：画顶点、折线、Bezier曲线 
  { int i; glClear(GL_COLOR_BUFFER_BIT); glColor3f(1,1,0); 
  glBegin(GL_LINE_STRIP); //画折线
   for(i=0;i<n;i++) glVertex3fv(a[i]); glEnd(); glColor3f(0,1,0); glPointSize(5.0); //设置画点的大小 
   glBegin(GL_POINTS); //画点 
   for(i=0;i<n;i++) glVertex3fv(a[i]); glEnd(); drawBezier(); }
