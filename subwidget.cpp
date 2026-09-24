#include "subwidget.h"
#include<iostream>
using namespace std;
#include<stack>
#include<vector>
#include<cstdlib>
#include<limits.h>
bool isNum(char ch);
bool isoper(char ch);
int level(char ch);
string bintodec(string s);
string hextodec(string s);
int sb=1;//进制判断
int bt=1;//错误判断
double scd(string s);
double getValue(vector<string> V);
vector<string> midToPost(string s);
SubWidget::SubWidget(QWidget *parent) : QWidget(parent)
{b=new QPushButton("切换");
  this->setWindowTitle("进制");
            connect(b,&QPushButton::clicked,this,&SubWidget::sendSlot);
            inputline=new QLineEdit;
            inputline->setText(input);
            zero=new QPushButton("0");
            one=new QPushButton("1");
            two=new QPushButton("2");
            three=new QPushButton("3");
            four=new QPushButton("4");
            five=new QPushButton("5");
            six=new QPushButton("6");
            seven=new QPushButton("7");
            eight=new QPushButton("8");
            nine=new QPushButton("9");
            dec=new QPushButton(".");
            CE=new QPushButton("CE");
            AC=new QPushButton("AC");

            add=new QPushButton("+");
            sub=new QPushButton("-");
            mul=new QPushButton("*");
            div=new QPushButton("/");
            equ=new QPushButton("=");
            A=new QPushButton("A");
            B=new QPushButton("B");
            C=new QPushButton("C");
            D=new QPushButton("D");
            E=new QPushButton("E");
            F=new QPushButton("F");
            bin=new QPushButton("bin");
            hex=new QPushButton("hex");

            QGridLayout *h=new QGridLayout(this);

            inputline->setFixedHeight(50);
            h->addWidget(inputline,0,0,1,3);
            h->setRowStretch(0,100);
            h->addWidget(AC,0,4);
            h->addWidget(CE,0,5);
            h->addWidget(one,1,0);
            h->addWidget(two,1,1);
            h->addWidget(three,1,2);
            h->addWidget(add,1,3);
            h->addWidget(A,1,5);
            h->addWidget(sub,1,4);
            h->addWidget(b,4,3);
            h->addWidget(four,2,0);
            h->addWidget(five,2,1);
            h->addWidget(six,2,2);
            h->addWidget(mul,2,3);
            h->addWidget(div,2,4);
            h->addWidget(B,2,5);

            h->addWidget(seven,3,0);
            h->addWidget(eight,3,1);
            h->addWidget(nine,3,2);
            h->addWidget(equ,3,3);
            h->addWidget(C,3,4);
            h->addWidget(D,3,5);
            h->addWidget(zero,4,0);
            h->addWidget(bin,4,1);
            h->addWidget(hex,4,2);
            h->addWidget(E,4,4);
            h->addWidget(F,4,5);
             this->setLayout(h);
            connect(zero,SIGNAL(clicked()),this,SLOT(butzero()));
            connect(one,SIGNAL(clicked()),this,SLOT(butone()));
            connect(two,SIGNAL(clicked()),this,SLOT(buttwo()));
            connect(three,SIGNAL(clicked()),this,SLOT(butthree()));
            connect(four,SIGNAL(clicked()),this,SLOT(butfour()));
            connect(five,SIGNAL(clicked()),this,SLOT(butfive()));
            connect(six,SIGNAL(clicked()),this,SLOT(butsix()));
            connect(seven,SIGNAL(clicked()),this,SLOT(butseven()));
            connect(eight,SIGNAL(clicked()),this,SLOT(buteight()));
            connect(nine,SIGNAL(clicked()),this,SLOT(butnine()));
            connect(A,SIGNAL(clicked()),this,SLOT(butA()));
            connect(B,SIGNAL(clicked()),this,SLOT(butB()));
            connect(C,SIGNAL(clicked()),this,SLOT(butC()));
            connect(D,SIGNAL(clicked()),this,SLOT(butD()));
            connect(E,SIGNAL(clicked()),this,SLOT(butE()));
            connect(F,SIGNAL(clicked()),this,SLOT(butF()));
            connect(add,SIGNAL(clicked()),this,SLOT(butadd()));
            connect(sub,SIGNAL(clicked()),this,SLOT(butsub()));
            connect(mul,SIGNAL(clicked()),this,SLOT(butmul()));
            connect(div,SIGNAL(clicked()),this,SLOT(butdiv()));
            connect(CE,SIGNAL(clicked()),this,SLOT(butCE()));
            connect(AC,SIGNAL(clicked()),this,SLOT(butAC()));
            connect(equ,SIGNAL(clicked()),this,SLOT(butequ()));
            connect(bin,SIGNAL(clicked()),this,SLOT(butbin()));
            connect(hex,SIGNAL(clicked()),this,SLOT(buthex()));
}
void SubWidget::sendSlot(){
    emit mySignal();
}
void SubWidget::butzero(){
    if(input=="0")
        input='0';
    else {
        input=input+'0';
    }inputline->setText(input);
}
void SubWidget::butone(){
    if(input=="0")
        input='1';
    else {
        input=input+'1';
    }inputline->setText(input);
}
void SubWidget::buttwo(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='2';
    else {
        input=input+'2';
    }inputline->setText(input);
}
void SubWidget::butthree(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='3';
    else {
        input=input+'3';
    }inputline->setText(input);
}
void SubWidget::butfour(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='4';
    else {
        input=input+'4';
    }inputline->setText(input);
}
void SubWidget::butfive(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='5';
    else {
        input=input+'5';
    }inputline->setText(input);
}
void SubWidget::butsix(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='6';
    else {
        input=input+'6';
    }inputline->setText(input);
}
void SubWidget::butseven(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='7';
    else {
        input=input+'7';
    }inputline->setText(input);
}
void SubWidget::buteight(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='8';
    else {
        input=input+'8';
    }inputline->setText(input);
}
void SubWidget::butnine(){
    if(sb==3)
        bt=1;
    if(input=="0")
        input='9';
    else {
        input=input+'9';
    }inputline->setText(input);
}
void SubWidget::butadd(){
    if(input=="0")
        input='+';
    else {
        input=input+'+';
    }inputline->setText(input);
}
void SubWidget::butsub(){
    if(input=="0")
        input='-';
    else {
        input=input+'-';
    }inputline->setText(input);
}
void SubWidget::butmul(){
    if(input=="0")
        input='*';
    else {
        input=input+'*';
    }inputline->setText(input);
}
void SubWidget::butdiv(){
    if(input=="0")
        input='/';
    else {
        input=input+'/';}
    inputline->setText(input);}
void SubWidget::butA(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='A';
    else {
        input=input+'A';
    }inputline->setText(input);
}
void SubWidget::butB(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='B';
    else {
        input=input+'B';
    }inputline->setText(input);
}
void SubWidget::butC(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='C';
    else {
        input=input+'C';
    }inputline->setText(input);
}
void SubWidget::butD(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='D';
    else {
        input=input+'D';
    }inputline->setText(input);
}
void SubWidget::butE(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='E';
    else {
        input=input+'E';
    }inputline->setText(input);
}
void SubWidget::butF(){
    if(sb!=2)
        bt=1;
    if(input=="0")
        input='F';
    else {
        input=input+'F';
    }inputline->setText(input);
}
void SubWidget::butCE(){
    input =input.left(input.length()-1);
    inputline->setText(input);
}
void SubWidget::butAC(){


        input='0';
    inputline->setText(input);
}
void SubWidget::buthex(){
    sb=2;
}
void SubWidget::butbin(){
    sb=3;
}
void SubWidget::butequ(){

    string temp =input.toStdString();
    vector<string> expression=midToPost(temp);
    double value=getValue(expression);
    if(value !=INT_MAX&&bt!=1){
      input=input+"="+QString::number(value);
      inputline->setText(input);}
    else{
        input=input+"=syntax error";
        inputline->setText(input);

    }

}
