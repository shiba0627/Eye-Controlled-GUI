#pragma once

#include <QtWidgets/QMainWindow>
#include <QPushButton>
#include <QLabel>
#include <QPixmap>
#include <Qvector>
//#include "ui_mainwindow.h"//mainwindow.uiをロード

class MainWindow : public QMainWindow//MainWindowはQMainWindowを継承
{
    Q_OBJECT//シグナル・スロットを有効化

public:
    MainWindow(QWidget *parent = nullptr);//コンストラクタ
    ~MainWindow();//デストラクタ

protected:
    void resizeEvent(QResizeEvent* event) override;


private:
    //Ui::MainWindowClass ui;//Qtdesignerで編集
    //QPushButton* button;
    QLabel* setting;
    QLabel* forward;
    QLabel* stop;
    QLabel* cw;
    QLabel* ccw;
    QLabel* back;
    QVector<QLabel*> labels;         // QLabelをまとめて管理
    QVector<QPixmap> pixmaps;        // 元画像を保持
};

