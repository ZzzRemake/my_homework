#ifndef CRYPTOCLIENT_H
#define CRYPTOCLIENT_H

#include <QWidget>
#include <QTcpSocket>
#include <QFile>
#include <QDateTime>
#include "cryptocontrol.h"

QT_BEGIN_NAMESPACE
namespace Ui { class CryptoClient; }
QT_END_NAMESPACE

class CryptoClient : public QWidget
{
    Q_OBJECT

public:
    CryptoClient(QWidget *parent = nullptr);
    ~CryptoClient();

    void init_TCP();
    void new_connect();

private slots:
    void connect_server();
    void disconnect_server();

    void receive_data();

    void select_sending_file();
    void choose_IP_address();

    void send_file();
    void update_sended_file_progress(qint64);
    void update_message_send_file();
    void update_message_establish_connection();
    void update_message_close_connection();
    void update_is_file_remove(bool check);

    void generate_public_connection_key();
    void generate_digital_signature_key();
    void select_public_connection_key();
    void select_digital_signature_key();
private:
    Ui::CryptoClient *ui;

    QTcpSocket *fileSocket;
    QTcpSocket *cryptoSocket;

    QFile *localFile;

    qint64 totalBytes;
    qint64 bytesWritten;
    qint64 bytestoWrite;
    //qint64 fileNameSize;
    qint64 blockSize;

    QString fileName;
    bool isFileOver;
    bool isFileRemove;

    QString publicConnectionKeyName,digitalSignatureKeyName;
    std::string encryKey,encryIV;
    QString encryFileName;
    std::string signature;
    bool isReceivedKey,isReceivedIV,isReceivedSignatrue;


    QByteArray outBlock;

    QDateTime currentDateTime;
    QString strDateTime;

    QString ipAddress;
 //   quint16 controlPort;
    quint16 filePort;
    quint16 cryptoPort;

    void update_message_in_brower(QString who,QString message);
    void generate_private_key();
    CryptoControl *CryptoMannager;
};
#endif // CRYPTOCLIENT_H
