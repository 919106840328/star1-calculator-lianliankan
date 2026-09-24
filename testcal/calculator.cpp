#include "calculator.h"
#include<iostream>
using namespace std;
#include<stack>//堆
#include<vector>//容器
#include<cstdlib>//转换
#include<limits.h>//限制
bool isNum(char ch);//判断数字
bool isoper(char ch);//判断操作
int level(char ch);//判断优先级
double scd(string s);//字符串转字符组
double getValue(vector<string> V);//计算
vector<string> midToPost(string s);//转表达式

calculator::calculator(QWidget *parent)
    : QMainWindow(parent)
{QWidget *widget=new QWidget;
    this->setCentralWidget(widget);
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
    binhex=new QPushButton("bin/hex");

    add=new QPushButton("+");
    sub=new QPushButton("-");
    mul=new QPushButton("*");
    div=new QPushButton("/");
    equ=new QPushButton("=");

    le=new QPushButton("(");
    ri=new QPushButton(")");
    CE=new QPushButton("CE");
    AC=new QPushButton("AC");
    QGridLayout *H=new QGridLayout(this);

    inputline->setFixedHeight(50);
    CE->setFixedHeight(50);
    AC->setFixedHeight(50);

    H->addWidget(inputline,0,0,1,3);
    H->setRowStretch(0,100);
    H->addWidget(CE,0,3);
    H->addWidget(AC,0,4);
    H->addWidget(one,1,0);
    H->addWidget(two,1,1);
    H->addWidget(three,1,2);
    H->addWidget(add,1,3);
    H->addWidget(sub,1,4);

    H->addWidget(four,2,0);
    H->addWidget(five,2,1);
    H->addWidget(six,2,2);
    H->addWidget(mul,2,3);
    H->addWidget(div,2,4);

    H->addWidget(seven,3,0);
    H->addWidget(eight,3,1);
    H->addWidget(nine,3,2);
    H->addWidget(equ,3,3);

    H->addWidget(zero,4,0);
    H->addWidget(dec,4,1);
    H->addWidget(le,4,2);
    H->addWidget(ri,4,3);
    H->addWidget(binhex,4,4);

    widget->setLayout(H);

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
    connect(CE,SIGNAL(clicked()),this,SLOT(butCE()));
    connect(AC,SIGNAL(clicked()),this,SLOT(butAC()));
    connect(add,SIGNAL(clicked()),this,SLOT(butadd()));
    connect(sub,SIGNAL(clicked()),this,SLOT(butsub()));
    connect(mul,SIGNAL(clicked()),this,SLOT(butmul()));
    connect(div,SIGNAL(clicked()),this,SLOT(butdiv()));
    connect(dec,SIGNAL(clicked(bool)),this,SLOT(butdec()));
    connect(le,SIGNAL(clicked(bool)),this,SLOT(butlef()));
    connect(ri,SIGNAL(clicked(bool)),this,SLOT(butri()));
    connect(equ,SIGNAL(clicked()),this,SLOT(butequ()));
    connect(binhex,SIGNAL(clicked()),this,SLOT(changewin()));
    connect(&w,&SubWidget::mySignal,this,&calculator::dealSub);
    this->setWindowTitle("基本计算器");
}
void calculator::butzero(){
    if(input=="0")
        input='0';
    else {
        input=input+'0';
    }inputline->setText(input);
}
void calculator::butone(){
    if(input=="0")
        input='1';
    else {
        input=input+'1';
    }inputline->setText(input);
}
void calculator::buttwo(){
    if(input=="0")
        input='2';
    else {
        input=input+'2';
    }inputline->setText(input);
}
void calculator::butthree(){
    if(input=="0")
        input='3';
    else {
        input=input+'3';
    }inputline->setText(input);
}
void calculator::butfour(){
    if(input=="0")
        input='4';
    else {
        input=input+'4';
    }inputline->setText(input);
}
void calculator::butfive(){
    if(input=="0")
        input='5';
    else {
        input=input+'5';
    }inputline->setText(input);
}
void calculator::butsix(){
    if(input=="0")
        input='6';
    else {
        input=input+'6';
    }inputline->setText(input);
}
void calculator::butseven(){
    if(input=="0")
        input='7';
    else {
        input=input+'7';
    }inputline->setText(input);
}
void calculator::buteight(){
    if(input=="0")
        input='8';
    else {
        input=input+'8';
    }inputline->setText(input);
}
void calculator::butnine(){
    if(input=="0")
        input='9';
    else {
        input=input+'9';
    }inputline->setText(input);
}
void calculator::butadd(){
    if(input=="0")
        input='+';
    else {
        input=input+'+';
    }inputline->setText(input);
}
void calculator::butsub(){
    if(input=="0")
        input='-';
    else {
        input=input+'-';
    }inputline->setText(input);
}
void calculator::butmul(){
    if(input=="0")
        input='*';
    else {
        input=input+'*';
    }inputline->setText(input);
}
void calculator::butdiv(){
    if(input=="0")
        input='/';
    else {
        input=input+'/';
    }inputline->setText(input);
}
void calculator::butdec(){
    if(input=="0")
    {input=input+'.';}
    else {
        input=input+'.';
    }inputline->setText(input);
}
void calculator::butlef(){
    if(input=="0")
        input='(';
    else {
        input=input+'(';
    }inputline->setText(input);
}
void calculator::butri(){
    if(input=="0")
        input=')';
    else {
        input=input+')';
    }inputline->setText(input);
}
void calculator::butCE(){
    input =input.left(input.length()-1);
    inputline->setText(input);
}
void calculator::butAC(){

        input='0';
    inputline->setText(input);
}
void calculator::butequ(){
    string temp =input.toStdString();
    vector<string> expression=midToPost(temp);
    double value=getValue(expression);
    if(value !=INT_MAX){
      input=input+"="+QString::number(value);
      inputline->setText(input);}
    else{
        input=input+"=syntax error";
        inputline->setText(input);

    }
}
void calculator::changewin(){
    w.show();
    this->hide();
}
void calculator::dealSub(){
    w.hide();
    this->show();
}
bool isNum(char ch){
    if((ch>='0'&&ch<='9')||(ch>='A'&&ch<='F'))
        return true;
    else return false;
}
bool isoper(char ch){
    if(ch=='*'||ch=='-'||ch=='+'||ch=='/'||ch=='('||ch==')')
        return true;
    else return false;
}
int level(char ch){
    switch(ch){
    case '(':
        return 5;
    case '*':
        return 4;
    case '/':
        return 4;
    case '+':
        return 3;
    case '-':
        return 3;
    case ')':
        return 2;
    }
}
    double scd(string s){
    if(s.length()==0)
    return INT_MAX;
    bool flag=false;
    for(int i=0;i<s.length();i++){
    if(i==0&&s[i]=='-')continue;
    else if(s[i]=='.'&&!flag){
    if(i>0&&isNum(s[i-1])){
    flag=true;
    continue;
    }
    else return INT_MAX;
    }
    else if(isNum(s[i]))
    continue;
    else return INT_MAX;
    }
    double result=atof(s.c_str());//字符串转数字
    return result;
    }
    vector<string> midToPost(string s) {
        stack<char> S;//存放临时符号的栈
        vector<string> V;//返回后缀表达式
        int i = 0;
        while(i < s.length()) {
            if(isNum(s[i])) {
                string str = "";
                while(isNum(s[i]) || s[i] == '.') {
                    str += s[i];
                    i++;
                }
                V.push_back(str);
            }//数字入容器

            else if(isoper(s[i])){
                if(s[i] == '-' && (i == 0 || !isNum(s[i-1]))) {
                    string str = "-"; i++;
                    while(isNum(s[i]) || s[i] == '.') {
                        str += s[i]; i++;
                    }
                    V.push_back(str);//负数的情况
                }else{
                    if(S.empty()){
                        S.push(s[i]); i++;
                    }else {
                        int initial = level(s[i]);
                        if(initial == 2) {
                            while(level(S.top()) != 5 && !s.empty()) {
                                string str = "";
                                str += S.top();
                                V.push_back(str);
                                S.pop();
                            }//判断优先级入栈
                            if(S.top() == '(') S.pop(); i++;
                        } else {
                            while(!S.empty() && initial <= level(S.top()) && level(S.top()) != 5) {
                                string str = "";
                                str += S.top();
                                V.push_back(str);
                                S.pop();
                            }
                            S.push(s[i]); i++;
                        }
                    }
                }
            }
            else{
                cout << "表达式出错" << endl;
                V.clear();
                return V;
            }
        }
        while(!S.empty()) {
            string str = ""; str += S.top();
            S.pop();
            V.push_back(str);
        }//将栈中剩余运算符入容器
        //for(int i = 0; i < V.size(); i++) cout << V[i] << "[]";
        return V;
    }

    double getValue(vector<string> V) {
        stack<double> S;//存放临时结果
        for(int i = 0; i < V.size(); i++) {
            if(V[i].length() == 1 && isoper(V[i][0])) {
                double a = 0, b = 0;
                if(!S.empty()) {
                    a = S.top(); S.pop();
                }else return INT_MAX;
//判断表达式
                if(!S.empty()) {
                    b = S.top(); S.pop();
                }else return INT_MAX;

                switch(V[i][0]) {
                    case '+':
                        S.push(b+a);
                        break;
                    case '-':
                        S.push(b-a);
                        break;
                    case '*':
                        S.push(b*a);
                        break;
                    case '/':
                        S.push(b/a);
                        break;
                    default:
                        return INT_MAX;
                }
            }else {
                if(scd(V[i]) == INT_MAX) return INT_MAX;
                else S.push(scd(V[i]));
            }
        }
        if(S.empty()) return INT_MAX;
//计算
        double value = S.top();
        S.pop();
        return value;
    }

calculator::~calculator()
{

}
