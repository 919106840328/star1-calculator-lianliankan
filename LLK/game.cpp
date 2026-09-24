#include "game.h"
#include <QBitmap>
#include <QPixmap>
#include <QTimer>
#include <QPalette>
#include <algorithm>
#include <iostream>
#include <stdio.h>
#include <time.h>

game::game(QWidget *parent)
    : QWidget(parent)
{
    window = 0;
    isStart = 2;
    setStartWindow();
}

game::~game()
{
    if(isStart == 1)
    {
        del_game();
        delete window;
    }
    else if(isStart == 0)
    {
        del_start();
        delete window;
    }
}

void game::creatmap()
{
    int b[MaxSizeX*MaxSizeY];
    int i, j, k;

    for(i = 0; i < MaxSizeX*MaxSizeY; i += 4)
        b[i] = b[i+1] = b[i+2] = b[i+3] = i/4+1;
    srand((unsigned)time(NULL));
    std::random_shuffle(b, b+MaxSizeX*MaxSizeY);
    memset(map, 0, sizeof(map));
    for(i = 1, k = 0; i <= MaxSizeX; i++)
        for(j = 1; i <= MaxSizeY; k++, j++)
            map[i][j] = b[k];

}







































