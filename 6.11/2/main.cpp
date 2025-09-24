# include <windows.h> 
#include <GL/glut.h> 
#include <math.h>
// GL08.cpp 画多边形网格的明暗图
const int M=50, N=50;
GLfloat vex[M+1][N+1][3]={0},nr[M+1][N+1][3]={0};
void createNormals() //生成顶点法向量
{ int i,j,i0,j0,i1,j1,m=M,n=N; GLfloat *p1,*p2,*p3; double x,y,z,t;
for(i=1;i<=m;i++) for(j=1;j<=n;j++) //计算四边形网格表面的法向量
{ p1=vex[i-1][j-1]; p2=vex[i][j-1]; p3=vex[i-1][j]; //右手系右手法则取点
x=(double)p1[1]*p2[2]+(double)p2[1]*p3[2]+(double)p3[1]*p1[2];
x=x-(double)p2[1]*p1[2]-(double)p3[1]*p2[2]-(double)p1[1]*p3[2];
y=(double)p1[2]*p2[0]+(double)p2[2]*p3[0]+(double)p3[2]*p1[0];
y=y-(double)p2[2]*p1[0]-(double)p3[2]*p2[0]-(double)p1[2]*p3[0];
z=(double)p1[0]*p2[1]+(double)p2[0]*p3[1]+(double)p3[0]*p1[1];
z=z-(double)p2[0]*p1[1]-(double)p3[0]*p2[1]-(double)p1[0]*p3[1]; t=sqrt(x*x+y*y+z*z); nr[i][j][0]=x/t; nr[i][j][1]=y/t; nr[i][j][2]=z/t; }
for(i=0;i<=m;i++) for(j=0;j<=n;j++) //由四边形网格表面法向量计算顶点法向量
{ i0=i; j0=j; i1=i+1; j1=j+1;if(i0<1) i0=1; if(j0<1) j0=1;if(i1>m) i1=m; if(j1>n) j1=n;
x=(double)nr[i0][j0][0]+nr[i0][j1][0]+nr[i1][j0][0]+nr[i1][j1][0];
y=(double)nr[i0][j0][1]+nr[i0][j1][1]+nr[i1][j0][1]+nr[i1][j1][1];
z=(double)nr[i0][j0][2]+nr[i0][j1][2]+nr[i1][j0][2]+nr[i1][j1][2];
t=sqrt(x*x+y*y+z*z); nr[i][j][0]=x/t; nr[i][j][1]=y/t; nr[i][j][2]=z/t; } }

double f1(double x,double y) 
{ x/=3; y/=3; double t=3*(1-x)*(1-x)*exp(-x*x-(y+1)*(y+1)); t=t-10*(x/5-x*x*x-y*y*y*y*y)*exp(-x*x-y*y)-exp(-(x+1)*(x+1)-y*y)/3; return t; } 
double f2(double x,double y) { return 3*exp(-(x*x+y*y)*0.01)*sin((x*x+y*y)/12); }
 double (*f)(double,double)=f1; 
 void createVertices(double (*f)(double,double)) //生成网格顶点 
 { double x0=-10.0,z0=-10.0,dx=20.0/N,dz=20.0/M,x,y,z,ss=10.0; 
 int i,j; for(i=0;i<=M;i++) 
 for(j=0;j<=N;j++) { x=x0+j*dx; z=z0+i*dz; y=f(x,z);vex[i][j][0]=x; vex[i][j][1]=y; vex[i][j][2]=z; } } 
 void createGrid() //带法向量绘制网格表面 
 { for(int k=0;k<N;k++) 
 { glBegin(GL_QUAD_STRIP); 
  for(int i=0;i<=M;i++) 
  { glNormal3fv(nr[i][k+1]); glVertex3fv(vex[i][k+1]); glNormal3fv(nr[i][k]); glVertex3fv(vex[i][k]); } 
  glEnd(); 
  } 
  glFlush(); 
  }
void mouse(int button,int state,int x,int y) //鼠标消息处理函数 
{ if(button==GLUT_LEFT_BUTTON&&state==GLUT_DOWN) f=f1; 
else if(button==GLUT_RIGHT_BUTTON&&state==GLUT_DOWN) f=f2; 
else return; glutPostRedisplay(); 
} 
void display(void) 
{ GLfloat pos[4]={-10,20,20,1},color[]={1,1,0,1}; glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT); //清颜色及深度 
glMatrixMode(GL_MODELVIEW); glLoadIdentity(); glOrtho(-12,12,-12,12,-12,12); glRotatef(30,1,1,0); glEnable(GL_DEPTH_TEST); //启用深度测试：用z缓冲算法消隐 
glEnable(GL_NORMALIZE); //使用法向量 
glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glLightfv(GL_LIGHT0,GL_POSITION,pos); //设置光源位置 
glLightfv(GL_LIGHT0,GL_AMBIENT,color); //设置环境光颜色 
glLightfv(GL_LIGHT0,GL_DIFFUSE,color); //设置漫反射光颜色
 glLightfv(GL_LIGHT0,GL_SPECULAR,color); //设置镜面反射光颜色 
 glShadeModel(GL_FLAT); 
 createVertices(f); createNormals(); createGrid(); glFlush(); }

int main(int argc,char **argv) 
{ glutInit(&argc,argv); glutInitWindowPosition(300,200); glutInitWindowSize(600,600); 
glutCreateWindow("Example 8"); glutDisplayFunc(display); glutMouseFunc(mouse); glutInitDisplayMode(GLUT_RGB|GLUT_DEPTH);
 glutMainLoop(); return 0; }
