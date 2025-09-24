//图形程序ege5_4A.cpp 简单多边形的三角剖分
//鼠标左击画多边形，右击重画；键盘按'd' 进行三角剖分；用屏幕坐标系，y轴向下
# include <graphics.h>
# include <math.h>
struct Point
{int x,y;
Point(int xx=0,int yy=0) { x=xx; y=yy; }
Point operator-(Point b) const { Point c(x-b.x,y-b.y); return c; } //向量减
double operator*(Point b) const { return(double)x*b.x+(double)y*b.y; } //内积
bool operator!=(Point b)const { return x!=b.x||y!=b.y; }
double zCross(Point b) const { return (double)x*b.y-(double)y*b.x; } 
};

bool getMessages(bool &mv,bool &ld,bool &rd,char &ch);
void drawPoly(Point a[ ],int &n,bool leftdown,bool rightdown,bool move,char ch);

int main( )
{Point a[50]; int n=0; bool move,leftdown,rightdown; char ch;
initgraph(640,480,INIT_RENDERMANUAL); setbkcolor(WHITE);
setcolor(BLUE); setfillcolor(GREEN); setbkmode(TRANSPARENT);
for( ; is_run( ) ; delay_fps(60))
{if(!getMessages(move,leftdown,rightdown,ch)) continue;
drawPoly(a,n,leftdown,rightdown,move,ch);
} 
closegraph( ); return 0; 
}

void divide(Point a[ ],int n); //进行三角剖分
void refresh(Point a[ ],int n,int b[ ][3]=0,int nt=0); //画多边形和三角剖分
bool getMessages(bool &mv,bool &ld,bool &rd,char &ch)
{mouse_msg msg={0}; bool m=false; mv=ld=rd=false; ch='\0';
while(mousemsg( )||kbhit( ) )
{m=true;
if(kbhit( ) ) { ch=getch( ); }
if(mousemsg( ) )
{msg=getmouse( );
if(msg.is_move( ) ) mv=true;
else if(msg.is_left( )&&msg.is_down( ) ) ld=true;
else if(msg.is_right( )&&msg.is_down( ) ) rd=true;
}
} return m;
}
void drawPoly(Point a[ ],int &n,bool leftdown,bool rightdown,bool move,char ch)
{if(ch!='\0') { if(ch=='d') divide(a,n); n=0; }
else
{if(leftdown) { mousepos(&a[n].x,&a[n].y); n++; }
else if(rightdown) n=0; else return; //鼠标移动时不重画
refresh(a,n); }
}

//三角形包含判定：包含(含边)返回true，否则返回false，注意y轴向下
bool inside(Point p0,Point p1,Point p2,Point p)
{Point v1=p1-p0,v2=p2-p1,v3=p0-p2; double s=1; if(v1.zCross(v2)>0) s= -1;
return v1.zCross(p-p1)*s<=0&&v2.zCross(p-p2)*s<=0&&v3.zCross(p-p0)*s<=0;
}
//两条线段相交性判定：相交返回true，否则返回false
bool intersect(Point p1,Point p2,Point q1,Point q2)
{Point p=p2-p1,q=q2-q1; //q1、q2在p1p2两侧且p1、p2在q1q2两侧
return (p.zCross(q1-p2)*p.zCross(q2-p2)<=0&&q.zCross(p1-q2)*q.zCross(p2-q2)<=0);
}
//三点构成的有向线段的偏向角：( 弧度) 即从p0p1到向量p1p2的转角(顺时针正角度)
double angle(Point p0,Point p1,Point p2) //求p0p1到p1p2的夹角(弧度制)
{Point v1=p1-p0,v2=p2-p1; double t=v1*v2,t2=(v1*v1)*(v2*v2);
if(t2<1e-14) return 0;
t=acos(t/sqrt(t2)); if(v1.zCross(v2)<0) t=-t; return t;
}
bool issimple(Point a[ ],int n) //判别是否是简单多边形：是则true，否则false
{for(int i=2;i<n;i++) for(int j=0;j<=i-2;j++) //判断是否有两条不相邻的边界相交
{if(((i+1)%n!=j)&&intersect(a[i],a[(i+1)%n],a[j],a[j+1])) return false; } //不相邻
return true;
}

void anticlockwise(Point a[ ],int n) //多边形顶点调整为逆时针方向
{double sita=angle(a[n-1],a[0],a[1]);
for(int i=0;i<n-1;i++) sita+=angle(a[i],a[i+1],a[(i+2)%n]); //求多边形外角总和
if(sita>0) { for(int i=0,j=n-1;i<j;i++,j--) { Point p=a[i]; a[i]=a[j]; a[j]=p; } } //顺时针
}
void showMessage(const char *s) //显示文字，按任意键结束
{
setcolor(YELLOW); bar(100,100,500,200); outtextxy(200,140,s); getch( );
}
void refresh(Point a[ ],int n,int b[ ][3],int nt)
{cleardevice( ); setlinestyle(SOLID_LINE,0,2); setcolor(BLACK);
moveto(a[0].x,a[0].y); for(int i=1;i<n;i++) lineto(a[i].x,a[i].y); //输出折线
if(nt!=0) lineto(a[0].x,a[0].y); //封闭成多边形
setlinestyle(SOLID_LINE,0,1); setcolor(RED);
for(int i=0;i<nt;i++) //输出三角剖分
{moveto(a[b[i][2]].x,a[b[i][2]].y);
for(int j=0;j<3;j++) lineto(a[b[i][j]].x,a[b[i][j]].y);
}
setcolor(BLUE);
}
void divide(Point a[ ],int n) //进行三角剖分
{int tri[50][3],b[50]; int nt=0,nb,i,q0,q1,q2,N; Point p0,p1,p2;
if(n<=2||!issimple(a,n))
{showMessage("非简单多边形--按任意键结束"); refresh(a,n); return; }
anticlockwise(a,n); //调整为逆时针
for(nb=n,i=0;i<nb;i++) b[i]=i; q0=0;
for(nt=N=0;nb>3;N++) //N为找到剖分三角形前查找次数，nb剩余边数
{if(N>nb) //找了一轮，没有找到凸出三角形
{ showMessage("非简单多边形--按任意键结束"); refresh(a,n); return; }
q1=(q0+1)%nb; q2=(q1+1)%nb; p0=a[b[q0]]; p1=a[b[q1]]; p2=a[b[q2]]; //连续点
if((p1-p0).zCross(p2-p1)>=0) { q0=q1; continue; } //q0q1q2不左转则继续查找
for(i=(q2+1)%nb;i!=q0;i=(i+1)%nb) //检测其余各点是否在三角形q0q1q2内
{ if(inside(p0,p1,p2,a[b[i]])) break; }
if(i!=q0) { q0=q1; continue; } //有其余点在三角形q0q1q2内则继续查找
tri[nt][0]=b[q0]; tri[nt][1]=b[q1]; tri[nt][2]=b[q2]; nt++; //记录凸出三角形
for(nb--,i=q1;i<nb;i++) b[i]=b[i+1]; q0=q0%nb; N=0; //删除找到的三角形,N清零
}
tri[nt][0]=b[0]; tri[nt][1]=b[1]; tri[nt][2]=b[2]; nt++;
refresh(a,n,tri,nt);
}
