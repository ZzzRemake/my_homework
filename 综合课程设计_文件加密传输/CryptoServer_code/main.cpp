#include "cryptoserver.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    CryptoServer w;
    w.show();
    return a.exec();
}
