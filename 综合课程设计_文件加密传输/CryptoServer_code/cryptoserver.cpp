#include "cryptoserver.h"
#include "ui_cryptoserver.h"
#include <QStandardPaths>
#include <QFileDialog>
#include <filters.h>


CryptoServer::CryptoServer(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::CryptoServer),cryptoPort_listen(11452),filePort_listen(11451)
{
    ui->setupUi(this);
    CryptoManager= nullptr;
    init_TCP();
    isFileOver=false;
    isReceivedKey=isReceivedIV=isReceivedSignature=false;
    filePosition=QStandardPaths::standardLocations(QStandardPaths::DownloadLocation).first()+"/";
    //qDebug()<<filePosition<<"\n";

    bytesReceived=0;
    totalBytes=0;
    fileNameSize=0;
    connect(ui->pushButton_Port,SIGNAL(clicked()),this,SLOT(choose_ip_port()));
    connect(ui->pushButton_closeConnection,SIGNAL(clicked()),this,SLOT(close_connection()));

    //Crypto
    connect(ui->pushButton_publicConnectKey,SIGNAL(clicked()),this,SLOT(load_public_connection_key()));
    connect(ui->pushButton_digitalSignatureKey,SIGNAL(clicked()),this,SLOT(load_digital_signature_key()));

    //debug
    //this->publicConnectKeyName="D:/Desktop_total/study/QT/build-CryptoClient-Desktop_Qt_5_12_12_MSVC2017_64bit-Release/RSA_connect_private.key";
    //this->digitalSignatureKeyName="D:/Desktop_total/study/QT/build-CryptoClient-Desktop_Qt_5_12_12_MSVC2017_64bit-Release/ed25519_Signal_public.key";
}

void CryptoServer::init_TCP(){
    //control socket

    this->cryptoServer =new QTcpServer(this);
    this->cryptoSocket = new QTcpSocket(this);
    this->cryptoServer->listen(QHostAddress::Any,cryptoPort_listen);
    connect(this->cryptoServer,SIGNAL(newConnection()),this,SLOT(accept_connection()));

    //file socket
    this->fileServer=new QTcpServer(this);
    this->fileSocket=new QTcpSocket(this);
    this->fileServer->listen(QHostAddress::Any,filePort_listen);
    connect(this->fileServer,SIGNAL(newConnection()),this,SLOT(accept_file_connection()));
    connect(this->cryptoSocket,SIGNAL(disconnected()),this,SLOT(update_message_disconnection()));
}

CryptoServer::~CryptoServer()
{
    delete ui;
}

void CryptoServer::update_message_in_brower(QString who,QString message) {
    currentDateTime=QDateTime::currentDateTime();
    strDateTime=currentDateTime.toString("yyyy-MM-dd hh:mm:ss");

    ui->textBrowser->append(who+" "+strDateTime+"\n"+message);
}

void CryptoServer::accept_connection(){
    this->cryptoSocket=this->cryptoServer->nextPendingConnection();
    connect(cryptoSocket,SIGNAL(readyRead()),this,SLOT(receive_message()));
    update_message_in_brower("Client","recieve new connection from "+cryptoSocket->peerAddress().toString()+":"+
                             QString::fromStdString(std::to_string(cryptoSocket->peerPort()))+"(hostname: "+
                             cryptoSocket->peerName()+")");
}

void CryptoServer::close_connection(){
    this->cryptoSocket->close();
    this->fileSocket->close();
}

void CryptoServer::accept_file_connection(){
    bytesReceived=0;
    blockSize=64*1024;
    //qDebug()<<"accept file\n";
    this->fileSocket=this->fileServer->nextPendingConnection();
    connect(fileSocket,SIGNAL(readyRead()),this,SLOT(update_received_file_progress()));
}

void CryptoServer::receive_message(){
    //qDebug()<<isFileOver<<" "<<isReceivedKey<<" begin receive crypto information";
    QDataStream inCrypto(this->cryptoSocket);
   // inCrypto.setVersion(QDataStream::Qt_5_12);
    char * strtem=nullptr;
    if(isFileOver){
        delete CryptoManager;
        CryptoManager=new Server_CryptoControl();
        //qDebug()<<cryptoSocket->bytesAvailable();
        if(cryptoSocket->bytesAvailable()>=sizeof(quint64)*3&&keySize==0){
            inCrypto.readRawData(reinterpret_cast<char*>(&keySize),sizeof(keySize));
            inCrypto.readRawData(reinterpret_cast<char*>(&ivSize),sizeof(ivSize));
            inCrypto.readRawData(reinterpret_cast<char*>(&signSize),sizeof(signSize));
        }
        //qDebug()<<cryptoSocket->bytesAvailable()<<' '<<keySize<<' '<<ivSize<<' '<<signSize;
        if(!isReceivedKey&&keySize&&cryptoSocket->bytesAvailable()>=keySize){
            //qDebug()<<"?";
            update_message_in_brower("You","receive private key");
            strtem=new char[keySize];
            inCrypto.readRawData(strtem,keySize);
            std::string str=std::string(strtem,keySize);
            CryptoManager->privateKey=CryptoManager->connect_by_public_key(
                        publicConnectKeyName,str,ui->comboBox_publicConnectKey->currentIndex());;
            isReceivedKey=true;
            delete [] strtem;
        }
        //qDebug()<<cryptoSocket->bytesAvailable()<<' '<<keySize<<' '<<ivSize<<' '<<signSize;
        if(!isReceivedIV&&ivSize&&cryptoSocket->bytesAvailable()>=ivSize){
                        update_message_in_brower("You","receive private iv");
            strtem=new char[ivSize];
            inCrypto.readRawData(strtem,ivSize);
            std::string str=std::string(strtem,ivSize);
            CryptoManager->IV=CryptoManager->connect_by_public_key(publicConnectKeyName,str,ui->comboBox_publicConnectKey->currentIndex());
            isReceivedIV=true;
            delete [] strtem;
        }
        //qDebug()<<cryptoSocket->bytesAvailable()<<' '<<keySize<<' '<<ivSize<<' '<<signSize;
        if(!isReceivedSignature&&signSize&&cryptoSocket->bytesAvailable()>=signSize){
                        update_message_in_brower("You","receive digital signature");
            strtem= new char [signSize];
            inCrypto.readRawData(strtem,signSize);
            std::string str=std::string(strtem,signSize);
            CryptoManager->signature=CryptoManager->connect_by_public_key(publicConnectKeyName,str,ui->comboBox_publicConnectKey->currentIndex());
            isReceivedSignature=true;
            delete [] strtem;
        }
        if(isReceivedKey&&isReceivedIV&&isReceivedSignature){
            isReceivedKey=isReceivedIV=isReceivedSignature=false;
            isFileOver=false;
            keySize=ivSize=signSize=0;
            //qDebug()<<"?";
            update_message_in_brower("You","begin valinate and decrypt file!");
            valinate_then_decrypt_file();
            QFile temFile(fileName);
            temFile.remove();
        }

    }
}

void CryptoServer::choose_ip_port(){
    close_connection();

    QString portFile=ui->lineEdit_filePort->text();
    QString portControl=ui->lineEdit_controlPort->text();
    cryptoPort_listen=portControl.toInt();
    filePort_listen=portFile.toInt();

    //control socket
    this->cryptoServer->close();
    this->cryptoServer->listen(QHostAddress::Any,cryptoPort_listen);
    //file socket
    this->fileServer->close();
    this->fileServer->listen(QHostAddress::Any,filePort_listen);
    update_message_in_brower("You", "Set new control listening Port: "+QString::number(cryptoPort_listen)+
                             ",file listening port: "+QString::number(filePort_listen)+".");

}



void CryptoServer::load_public_connection_key(){
    this->publicConnectKeyName=QFileDialog::getOpenFileName(this,"Open public key(private) file","/","files (*)");
    ui->lineEdit_publicConnectKey->setText(publicConnectKeyName);
}

void CryptoServer::load_digital_signature_key(){
    this->digitalSignatureKeyName=QFileDialog::getOpenFileName(this,"Open public key(public) file","/","files (*)");
    ui->lineEdit_digitalSignatureKey->setText(digitalSignatureKeyName);
}

void CryptoServer::update_received_file_progress(){
    QDataStream inFile(this->fileSocket);
    inFile.setVersion(QDataStream::Qt_5_12);

    if(bytesReceived<=sizeof(qint64)*3){
        //qDebug()<<"received!";
        if((fileSocket->bytesAvailable()>=(sizeof(qint64))*3)&&(fileNameSize==0)){
            inFile>>totalBytes>>privateKeyState>>fileNameSize;
            //qDebug()<<"3 number!";
            bytesReceived+=sizeof(qint64)*3;
            ui->progressBar->reset();
            ui->progressBar->setValue(0);
            ui->progressBar->setMaximum(totalBytes);
        }
        if((fileSocket->bytesAvailable()>=fileNameSize)&&(fileNameSize!=0)){

            inFile>>fileName;
            bytesReceived+=fileNameSize;
            //qDebug()<<"filename!"<<fileName;
            fileName=filePosition+fileName;
            localFile=new QFile(fileName);
            if(!localFile->open(QFile::WriteOnly)){
                //qDebug()<<"Server open file error!";
                update_message_in_brower("Server", "Open file in specefied postion error!");
                return;
            }
        } else {
            return;
        }
    }

    if(bytesReceived<totalBytes){
        bytesReceived+=fileSocket->bytesAvailable();
        inBlock=fileSocket->readAll();
        localFile->write(inBlock);
        inBlock.resize(0);
    }

    this->ui->progressBar->setMaximum(totalBytes);
    this->ui->progressBar->setValue(bytesReceived);

    if(bytesReceived>=totalBytes){
        isFileOver=true;
        //qDebug()<<isFileOver<<" file over!";
        update_message_in_brower("You","Receive file successfully!");
        bytesReceived=0;
        totalBytes=0;
        fileNameSize=0;
        localFile->close();
        receive_message();
    }
}


void CryptoServer::update_message_disconnection(){
    update_message_in_brower("You","disconnect the socket!");
}

void CryptoServer::valinate_then_decrypt_file(){
    QString str;
    qint64 control;
    std::string tem=fileName.toStdString();
    QString decryptedName=QString::fromStdString(std::string(tem.begin(),tem.end()-4));
    if(CryptoManager->decrypt_file(fileName,privateKeyState)){
        if(CryptoManager->valinate_digital_signature(digitalSignatureKeyName,decryptedName,ui->comboBox_digitalSignatureKey->currentIndex())){
            str="Valinate and decrypt file successfully!";
            control=0;
        } else {
            str="Decrypt file correctly but valinate failed!";
            control=1;
        }
    } else {
        control=2;
        str="Decrypt file failed!";
    }
    //qDebug()<<control;
    QDataStream sendOut(&outBlock,QIODevice::WriteOnly);
    sendOut.writeRawData(reinterpret_cast<char*>(&control),sizeof(control));
    this->cryptoSocket->write(outBlock);
    outBlock.resize(0);
    update_message_in_brower("You",str);
}
