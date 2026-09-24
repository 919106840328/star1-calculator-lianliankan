#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <QMainWindow>
#include<QPushButton>
#include<QLineEdit>
#include<QHBoxLayout>
#include<QString>
#include<QStack>
#include<QVBoxLayout>
#include<QGridLayout>
#include<iterator>
#include<subwidget.h>
class calculator : public QMainWindow
{
    Q_OBJECT

public:
    calculator(QWidget *parent = 0);
    ~calculator();

private:
    QLineEdit *inputline;
    QString input="0";
    bool flat=false;
    QPushButton *zero;
    QPushButton *one;
    QPushButton *two;
    QPushButton *three;
    QPushButton *four;
    QPushButton *five;
    QPushButton *six;
    QPushButton *seven;
    QPushButton *eight;
    QPushButton *nine;//0-9
    QPushButton *binhex;
    QPushButton *add;
    QPushButton *sub;
    QPushButton *div;
    QPushButton *mul;
    QPushButton *dec;
    QPushButton *equ;
    //+-...
    SubWidget w;
    QPushButton *CE;
    QPushButton *AC;
    QPushButton *le;
    QPushButton *ri;

private slots:
    void butzero();
    void butone();
    void buttwo();
    void butthree();
    void butfour();
    void butfive();
    void butsix();
    void butseven();
    void buteight();
    void butnine();

    void butadd();
    void butsub();
    void butmul();
    void butdiv();
    void butdec();

    void butequ();
    void butlef();
    void butri();
    void butCE();
    void butAC();
    void changewin();
    void dealSub();
};

#endif // CALCULATOR_H
