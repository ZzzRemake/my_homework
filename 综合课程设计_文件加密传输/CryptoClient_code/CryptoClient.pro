QT       += core gui
QT       += network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

INCLUDEPATH += "D:/Desktop_total/study/QT/LastOne/Cryptopp/include"
LIBS += -L"D:/Desktop_total/study/QT/LastOne/Cryptopp/lib" -lcryptlib

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    cryptocontrol.cpp \
    main.cpp \
    cryptoclient.cpp

HEADERS += \
    cryptoclient.h \
    cryptocontrol.h

FORMS += \
    cryptoclient.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RC_FILE = client_logo.rc
