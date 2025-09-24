//图形程序ege7_2dynamic.cpp 动态画球的消隐线框图
//鼠标按左键拖拽转动，按右键恢复初始状态
# include <graphics.h>
# include "observe.h"
void rotateByPoint(Point start,Point end,double R);
void process(double R,observe3D ob);
observe3D ob; Point start={0,0},end={0,0}; double R=10;
int main( )
{
 initgraph(640,480,INIT_RENDERMANUAL); setbkcolor(WHITE);
 Rect rc={0,0,639,479}; point3D::setViewport(rc); point3D::setWindow(-12,12,12,-12);
 ob.lookAt(0,0,-1,0,1,0); process(R,ob); bool move,leftdown,rightdown; mouse_msg msg;
 for( ; is_run( ) ; delay_fps(60))
 {move=leftdown=rightdown=false;
  while(mousemsg())
  {msg=getmouse(); if(msg.is_move()) move=true;
   else if(msg.is_left()&&msg.is_down()) leftdown=true;
   else if(msg.is_right()&&msg.is_down()) rightdown=true;
  }
 if(leftdown) { start.x=msg.x; start.y=msg.y; end=start; }
 else if(rightdown) { ob=observe3D(); ob.lookAt(0,0,-1,0,1,0); process(R,ob); }
 else if(move&&keystate(key_mouse_l))
  { start=end; mousepos(&end.x,&end.y); rotateByPoint(start,end,R); process(R,ob); }
 }
 closegraph(); return 0; 
}
point3D topoint3D(Point v,double R) // 视区上的点反推球面上的点(右手系的点)
{
 point3D v3D=point3D::byPoint(v); double x=v3D.x,y=v3D.y,z=R*R-x*x-y*y;
 if(z>0) v3D.z= sqrt(z); return v3D; 
} //v3D是右手系的向量，故v3D.z取正
void rotateByPoint(Point start,Point end,double R) //start到end过球心的旋转变换
{
 point3D v1=topoint3D(start,R),v2=topoint3D(end,R),v3;double sita; v3=v1^v2;
 double t=v1*v2; t/=sqrt((v1*v1)*(v2*v2)); sita=acos(t); ob.rotate(sita,v3); 
}
point3D f(double R,double sita,double phi) // 球坐标换算成直角坐标
{return point3D(R*sin(sita)*sin(phi),R*cos(sita),R*sin(sita)*cos(phi)); }
void draw(observe3D ob,point3D p1,point3D p2,point3D p3,point3D p4) //画面片正面
{
 p1=ob.trans(p1); p2=ob.trans(p2); p3=ob.trans(p3); p4=ob.trans(p4);//p1p2p3p4顺时针
 if( ((p2-p1)^(p3-p2)).z<0 )//面片外法线方向朝观察者(左手系向量叉乘与观察方向相反)
 {Point cp[5]={p1.toPoint(),p2.toPoint(),p3.toPoint(),p4.toPoint(),p1.toPoint()};drawpoly(5,(int*)cp);}
}
void process(double R,observe3D ob) //凸多边形消隐算法画球面网格图
{
 const double pi=3.141592653589793; double dsita=pi/20,dphi=2*pi/36,sita,phi;
 point3D p0(0,R,0),p1,p2,p3,p4,xc(R*1.5,0,0),yc(0,R*1.5,0),zc(0,0,R*1.5);
 Point cp[3]={ob.trans(xc).toPoint(),ob.trans(yc).toPoint(),ob.trans(zc).toPoint()},c;
 c=ob.trans(point3D(0,0,0)).toPoint(); cleardevice();
 setcolor(RED); 
 for(int i=0;i<3;i++) line(c.x,c.y,cp[i].x,cp[i].y); setcolor(GREEN); //画坐标轴
 for(phi=0;phi<2*pi-0.001;phi+=dphi) //按经线从北向南画面片
 {
  p1=p2=p0; p3=f(R,dsita,phi+dphi); p4=f(R,dsita,phi); //左手系顺时针方向取面片顶点
  draw(ob,p2,p3,p4,p1); //前三点确定外法线方向，此处p1=p2
  for(sita=2*dsita;sita<=pi+0.001;sita+=dsita)
  {p1=p4; p2=p3; p3=f(R,sita,phi+dphi); p4=f(R,sita,phi);
   draw(ob,p1,p2,p3,p4); }
  } 
}
