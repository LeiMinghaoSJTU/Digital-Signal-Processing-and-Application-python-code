# include <graphics.h>
using namespace std;
struct Node
{ 
int ymax,x; double dx; Node *next; //成员数据
Node(int ymm=0,int xx=0,double dxx=0);
Node(const Node &nd);
Node *insert(Node *head); //结点升序插入链表head中，返回新链表头指针
Node *del(Node *head); //结点从链表head中脱链，返回新链表头指针
static void exchange(Node *pt1,Node *pt2); //交换pt1和pt2指向结点的数据
static void delAll(Node *head); //删除链表head，并释放结点空间
};
Node **createET(int n,int p[ ],int &Ymi,int &Yma); //生成ET返回，传Ymi和Yma
void Fillpoly2(int n,int p[ ]); //有序边表填充算法画多边形

int main( )
{initgraph(640,480);
int poly[6*2]={100,100, 100,300, 250,450, 400,300, 400,100, 250,250};
setcolor(YELLOW); setfillcolor(BLUE); setlinestyle(SOLID_LINE,0,3);
Fillpoly2(6,poly); getch(); closegraph(); return 0;
}

Node **createET(int n,int p[ ],int&Ymi,int&Yma)
{int i,j,x0,y0,x1,y1,x,y,ymax; double dxx; Node *pt,**ET;
for(Ymi=Yma=p[1],i=1;i<2*n;i+=2) //找多边形顶点y坐标的最小Ymi和最大Yma
{if(p[i]>Yma) Yma=p[i]; else if(p[i]<Ymi) Ymi=p[i]; }
ET=new Node*[Yma-Ymi+1]; ET=ET-Ymi;
for(i=Ymi;i<=Yma;i++) ET[i]=0; //ET清零
for(i=0;i<n;i++) //处理每一条边
{x0=p[2*i]; y0=p[2*i+1];
j=(i+1)%n; x1=p[2*j]; y1=p[2*j+1];
if(y0==y1) continue; //跳过水平边
if(y0<y1) { x=x0; y=y0; ymax=y1; } //确定边的低端(x,y)高端ymax,斜率倒数dx
else { x=x1; y=y1; ymax=y0; }
dxx=double(x1-x0)/(y1-y0); pt=new Node(ymax-1,x,dxx);ET[y]=pt->insert(ET[y]); //(ymax,x,dx)有序插入链表ET[y]中
}
return ET;
}

void Fillpoly2(int n,int p[ ])
{int Ymi,Yma,x,y,i; color_t fillcolor=getfillcolor();
Node **ET=createET(n,p,Ymi,Yma),*AET=0,*pt,*pt2; //生成ET，AET=0
for(y=Ymi;y<=Yma;y++)
{for(pt=ET[y];pt!=0;pt=pt->next) //链表ET[y]中的每一个结点插入链表AET中
{pt2=new Node(*pt); AET=pt2->insert(AET); }
for(pt2=AET;pt2!=0&&pt2->next!=0;pt2=pt2->next) //依次填充AET中的结点对
{x=pt2->x; pt2=pt2->next; while(x<=pt2->x) { putpixel(x,y,fillcolor); x++; } }
for(pt2=AET;pt2!=0; ) //对链表AET 中的每一个结点执行
{if(pt2->ymax==y) //删除y=ymax的结点
{ pt=pt2; pt2=pt2->next; AET=pt->del(AET); delete pt; }
else { pt2->x+=pt2->dx; pt2=pt2->next; } //否则改动x=x+dx
}
for(pt2=AET;pt2!=0&&pt2->next!=0; ) //扫描AET，若降序则重排
{pt=pt2; pt2=pt2->next; double v1,v2;
v1=pt->x*1000.0+pt->dx,v2=pt2->x*1000.0+pt2->dx;
if(v1>v2) Node::exchange(pt,pt2) ; //相邻点(x,dx)降序则交换
}
}
moveto(p[2*n-2],p[2*n-1]); for(i=0;i<n;i++) lineto(p[2*i],p[2*i+1]); //画多边形的边
Node::delAll(AET); for(y=Ymi;y<=Yma;y++) Node::delAll(ET[y]); //释放结点空间delete[ ](ET+Ymi); }
Node::Node(int ymm,int xx,double dxx) //类成员函数的定义
{ ymax=ymm;x=xx;dx=dxx;next=0; }
Node::Node(constNode &nd)
{ymax=nd.ymax; x=nd.x; dx=nd.dx; next=0; }
Node *Node::insert(Node *head)
{Node tmp,*p1=&tmp,*p2=head; tmp.next=head;
while(p2&&!(x<p2->x||x==p2->x&&dx<p2->dx)){ p1=p2; p2=p2->next; }
p1->next=this; this->next=p2; return tmp.next;
}
Node *Node::del(Node *head)
{Node tmp,*p1=&tmp,*p2=head; tmp.next=head;
while(p2&&p2!=this) { p1=p2;p2=p2->next; }
if(p2==this){ p1->next=p2->next; }
return tmp.next;
}

void Node::exchange(Node *pt1,Node *pt2)
{intk=pt1->ymax; pt1->ymax=pt2->ymax; pt2->ymax=k;
k=pt1->x; pt1->x=pt2->x; pt2->x=k;
double t=pt1->dx; pt1->dx=pt2->dx; pt2->dx=t;
}

void Node::delAll(Node *head)
{for(Node *pt=head;pt!=0;pt=head) { head=head->next; delete pt; } }
} 
