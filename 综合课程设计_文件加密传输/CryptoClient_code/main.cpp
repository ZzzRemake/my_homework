#include "cryptoclient.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    CryptoClient w;
    w.show();
    return a.exec();
}
