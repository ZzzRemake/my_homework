#ifndef CRYPTOSERVER_H
#define CRYPTOSERVER_H

#include <QWidget>
#include <QTcpServer>
#include <QTcpSocket>
#include <QFile>
#include <QDateTime>
#include "server_cryptocontrol.h"

QT_BEGIN_NAMESPACE
namespace Ui { class CryptoServer; }
QT_END_NAMESPACE

class CryptoServer : public QWidget
{
    Q_OBJECT

public:
    CryptoServer(QWidget *parent = nullptr);
    ~CryptoServer();

    QTcpServer *cryptoServer;
    QTcpSocket *cryptoSocket;
    QTcpServer *fileServer;
    QTcpSocket *fileSocket;

    void init_TCP();

private slots:
    void accept_connection();
    void receive_message();

    void accept_file_connection();


    void update_received_file_progress();

    void choose_ip_port();
    void load_public_connection_key();
    void load_digital_signature_key();
    void close_connection();

    void update_message_disconnection();
private:
    Ui::CryptoServer *ui;

    qint64 totalBytes;
    qint64 bytesReceived;
    qint64 fileNameSize;

    QString fileName;
    QString publicConnectKeyName,digitalSignatureKeyName;
    QString filePosition;

    qint64 blockSize;
    QFile *localFile;

    QString encryKey,encryIV,signature;
    qint64 privateKeyState=0;
    bool isReceivedKey,isReceivedIV,isReceivedSignature;
    bool isFileOver;
    Server_CryptoControl * CryptoManager;

    QByteArray inBlock;
    QByteArray outBlock;
    quint64 keySize=0,ivSize=0,signSize=0;

    QDateTime currentDateTime;
    QString strDateTime;

    quint16 cryptoPort_listen;
    quint16 filePort_listen;

    void update_message_in_brower(QString who,QString message);
    void valinate_then_decrypt_file();
};
#endif // CRYPTOSERVER_H
