#include "mainwindow.h"
#include <QPushButton>
#include <QIcon>
#include <QResizeEvent>
#include <QLabel>
#include <QPixmap>

MainWindow::MainWindow(QWidget *parent)//コンストラクタ
    : QMainWindow(parent)
{
    //this->resize(500, 500);
    //ui.setupUi(this);
    //全画面表示(ウィンドウ残し)
    //this->showMaximized();
    // 全画面表示
    //this->showFullScreen();
    QStringList images = {
        ":/MainWindow/img/forward.png",
        ":/MainWindow/img/back.png",
        ":/MainWindow/img/cw.png",
        ":/MainWindow/img/ccw.png",
        ":/MainWindow/img/stop.png"
    };
    for (const auto& path : images) {
        QLabel* lbl = new QLabel(this);
        QPixmap pix(path);
        pixmaps.append(pix); // 元画像を保持
        lbl->setPixmap(pix.scaled(100, 100, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        lbl->setGeometry(50, 50, 100, 100); // 仮初期位置
        labels.append(lbl);
    }
    setting = new QLabel(this);
    QPixmap pix(":/MainWindow/img/setting.png");
    QPixmap scaledPix = pix.scaled(250, 200, Qt::KeepAspectRatio, Qt::SmoothTransformation);
    setting->setPixmap(scaledPix);
    setting->setGeometry(50, 50, scaledPix.width(), scaledPix.height());
    // ボタンの位置とサイズを決める
    //button->setGeometry(1/2*w, 1/2*h, w*0.3, h*0.3); // x, y, width, height
}

// ウィンドウリサイズ時にボタン位置・サイズを更新
void MainWindow::resizeEvent(QResizeEvent* event)
{
    int w = this->width();
    int h = this->height();

    int n = labels.size();
    for (int i = 0; i < n; ++i) {
        int label_w = w * 0.2; // 幅は20%とかに調整
        int label_h = h * 0.2;
        int x = (w / (n + 1)) * (i + 1) - label_w / 2; // 横並び
        int y = h / 2 - label_h / 2; // 縦中央

        labels[i]->setGeometry(x, y, label_w, label_h);

        // pixmapをリサイズして設定
        //QPixmap scaledPix = pixmaps[i].scaled(label_w, label_h, Qt::KeepAspectRatio, Qt::SmoothTransformation);
        QPixmap scaledPix = pixmaps[i].scaled(label_w, label_h, Qt::IgnoreAspectRatio,Qt::SmoothTransformation);

        labels[i]->setPixmap(scaledPix);
    }

    QMainWindow::resizeEvent(event);
}



MainWindow::~MainWindow()
{}

