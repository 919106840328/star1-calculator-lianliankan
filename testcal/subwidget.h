#ifndef SUBWIDGET_H
#define SUBWIDGET_H

#include <QWidget>
#include<QPushButton>
#include<QLineEdit>
#include<QHBoxLayout>
#include<QString>
#include<QStack>
#include<QVBoxLayout>
#include<QGridLayout>
#include<iterator>
class SubWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SubWidget(QWidget *parent = nullptr);
    void sendSlot();
signals:
    void mySignal();
public slots: void butzero();
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
    void butA();
    void butB();
    void butC();
    void butD();
    void butE();
    void butF();
    void butAC();
    void butCE();
    void butequ();
    void butbin();
    void buthex();
private:
    QPushButton *b;
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
    QPushButton *add;
    QPushButton *sub;
    QPushButton *div;
    QPushButton *mul;
    QPushButton *dec;
    QPushButton *equ;
    QPushButton *A;
    QPushButton *B;
    QPushButton *C;
    QPushButton *D;
    QPushButton *E;
    QPushButton *F;
    QPushButton *bin;
    QPushButton *hex;
    QPushButton *CE;
    QPushButton *AC;
};

#endif // SUBWIDGET_H
