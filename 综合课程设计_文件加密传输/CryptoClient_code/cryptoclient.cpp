#include "cryptoclient.h"
#include "ui_cryptoclient.h"
#include "filters.h"
#include "hex.h"
#include <QFileDialog>

CryptoClient::CryptoClient(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::CryptoClient),ipAddress("127.0.0.1"),filePort(11451),cryptoPort(11452),CryptoMannager(new CryptoControl){

    ui->setupUi(this);
    fileSocket=nullptr,cryptoSocket=nullptr;

    isFileOver=isFileRemove=false;
    isReceivedIV=isReceivedKey=isReceivedSignatrue=false;
    init_TCP();
    //传输参数设置
    blockSize=64*1024;
    totalBytes=0;
    bytesWritten=bytestoWrite=0;

    //file
    connect(this->ui->pushButton_File,SIGNAL(clicked()),this,SLOT(select_sending_file()));
    connect(this->ui->pushButton_SendFile,SIGNAL(clicked()),this,SLOT(send_file()));
    connect(this->ui->checkBox_RemoveFile,SIGNAL(clicked(bool)),this,SLOT(update_is_file_remove(bool)));
    //ip
    connect(this->ui->pushButton_IP,SIGNAL(clicked()),this,SLOT(choose_IP_address()));
    connect(this->ui->pushButton_IP,SIGNAL(clicked()),this,SLOT(disconnect_server()));
    connect(this->ui->pushButton_SendFile,SIGNAL(clicked()),this,SLOT(update_message_send_file()));
    //crypto
    connect(this->ui->pushButton_DigitalKeyGenerate,SIGNAL(clicked()),this,SLOT(generate_digital_signature_key()));
    connect(this->ui->pushButton_DigitalKeyPosition,SIGNAL(clicked()),this,SLOT(select_digital_signature_key()));
    connect(this->ui->pushButton_PublicConnectGenerate,SIGNAL(clicked()),this,SLOT(generate_public_connection_key()));
    connect(this->ui->pushButton_PublicConnectPosition,SIGNAL(clicked()),this,SLOT(select_public_connection_key()));
}

CryptoClient::~CryptoClient(){
    delete ui;
    delete CryptoMannager;
    delete cryptoSocket;
    delete fileSocket;
}

void CryptoClient::update_message_in_brower(QString who,QString message) {
    currentDateTime=QDateTime::currentDateTime();
    strDateTime=currentDateTime.toString("yyyy-MM-dd hh:mm:ss");

    ui->textBrowser->append(who+" "+strDateTime+"\n"+message);
}


void CryptoClient::init_TCP(){
    this->fileSocket=new QTcpSocket(this);
     this->cryptoSocket=new QTcpSocket(this);
    connect(ui->pushButton_Connect,SIGNAL(clicked()),this,SLOT(connect_server()));
    connect(ui->pushButton_Disconnect,SIGNAL(clicked()),this,SLOT(disconnect_server()));
    connect(this->cryptoSocket,SIGNAL(disconnected()),this,SLOT(update_message_close_connection()));
    connect(this->cryptoSocket,SIGNAL(connected()),this,SLOT(update_message_establish_connection()));
    connect(this->fileSocket,SIGNAL(bytesWritten(qint64)),this,SLOT(update_sended_file_progress(qint64)));

}

void CryptoClient::choose_IP_address(){
    ipAddress=ui->lineEdit_IP->text();
    QString portFile=ui->lineEdit_FilePort->text();
    QString portCrypto=ui->lineEdit_ControlPort->text();

    cryptoPort=portCrypto.toInt();
    filePort=portFile.toInt();
    update_message_in_brower("You", "Set new IP address: "+this->ipAddress+"/"+QString::number(cryptoPort)+
                             "(The port of sending file is "+QString::number(filePort)+").");
}

void CryptoClient::connect_server(){
    fileSocket->abort();
    fileSocket->connectToHost(ipAddress,filePort);
    cryptoSocket->abort();
    cryptoSocket->connectToHost(ipAddress,cryptoPort);
    //qDebug()<<"connect trying\n";
    connect(cryptoSocket,SIGNAL(readyRead()),this,SLOT(receive_data()));
    update_message_in_brower("You","Try controling connect default ip address: "+this->ipAddress+"/"+QString::number(cryptoPort)+
                             "(The port of sending file is "+QString::number(filePort)+").");
}

void CryptoClient::disconnect_server()
{
    if(fileSocket->state()==QAbstractSocket::ConnectedState){
        fileSocket->disconnectFromHost();
    }
    if(cryptoSocket->state()==QAbstractSocket::ConnectedState){
        cryptoSocket->disconnectFromHost();
    }
}

void CryptoClient::receive_data(){
    QDataStream inCrypto(this->cryptoSocket);
    if(cryptoSocket->bytesAvailable()>=sizeof(qint64)){
        qint64 test;
        inCrypto>>test;
        QString str;
        switch (test) {
            case 0: str="Valinate and decrypt file successfully!";break;
            case 1: str="Decrypt file correctly but valinate failed!";break;
            case 2: str="Decrypt file failed!";break;
            default: str="error! invalid server code:"+QString::fromStdString(std::to_string(test)); break;
        }
        update_message_in_brower("Server",str);
        //qDebug()<<"receive Crypto data from server";
    }
}

void CryptoClient::update_is_file_remove(bool check){
    isFileRemove=check;
}

void CryptoClient::select_sending_file(){
    this->fileName=QFileDialog::getOpenFileName(this,"Open sending file","/","files (*)");
    ui->lineEdit_File->setText(fileName);

}

void CryptoClient::send_file(){
    //qDebug()<<fileName;
    //encrypt file

    signature=this->CryptoMannager->create_digital_signature(digitalSignatureKeyName,
    fileName,ui->comboBox_DigitalOption->currentIndex());


    this->generate_private_key();
    this->CryptoMannager->create_encrypt_file(fileName,ui->comboBox_PrivateOption->currentIndex());
    //qDebug()<<"encrypt!";
    //transform encrypted file
    this->localFile = new QFile(fileName.right(fileName.size()-fileName.lastIndexOf('/')-1)+".enc");
    if(!localFile->open(QFile::ReadOnly)){
        update_message_in_brower("You","Open file error!");
        return;
    }
    fileSocket->abort();
    fileSocket->connectToHost(ipAddress,filePort);

    this->totalBytes=localFile->size();
    QDataStream sendOut(&outBlock,QIODevice::WriteOnly);
    sendOut.setVersion(QDataStream::Qt_5_12);
    QString currentFileName=fileName.right(fileName.size()-fileName.lastIndexOf('/')-1)+".enc";



    encryKey=this->CryptoMannager->create_public_connection(
                publicConnectionKeyName,this->CryptoMannager->get_privatekey()
                ,ui->comboBox_PublicConnectOption->currentIndex());
    encryIV=this->CryptoMannager->create_public_connection(
                publicConnectionKeyName,this->CryptoMannager->get_iv()
                ,ui->comboBox_PublicConnectOption->currentIndex());
    signature=this->CryptoMannager->create_public_connection(
                publicConnectionKeyName,signature
                ,ui->comboBox_PublicConnectOption->currentIndex());
    //qDebug()<<"key and iv generate!"<<encryKey.size()<<' '<<encryIV.size();
    //qDebug()<<totalBytes;
    sendOut<<qint64(0)<<qint64(0)<<qint64(0)<<currentFileName;
    totalBytes+=outBlock.size();
    sendOut.device()->seek(0);
    sendOut<<qint64(totalBytes)<<qint64(ui->comboBox_PrivateOption->currentIndex())<<qint64(outBlock.size()-sizeof(qint64)*3);
    //qDebug()<<totalBytes<<" "<<ui->comboBox_PrivateOption->currentIndex()<<qint64(outBlock.size()-sizeof(qint64)*3);
    this->ui->progressBar->reset();
    this->ui->progressBar->setValue(0);
    this->ui->progressBar->setMaximum(totalBytes);

    bytestoWrite=totalBytes-fileSocket->write(outBlock);
    outBlock.resize(0);
}

void CryptoClient::update_sended_file_progress(qint64 numBytes){
    bytesWritten+=(qint64)numBytes;
    //qDebug()<<totalBytes<<' '<<bytesWritten<<' '<<bytestoWrite;
    if(bytestoWrite>0ll){
        outBlock=localFile->read(qMin(bytestoWrite,blockSize));
        bytestoWrite-=((int)fileSocket->write(outBlock));
        outBlock.resize(0);
    } else {
      localFile->close();
    }

    this->ui->progressBar->setMaximum(totalBytes);
    this->ui->progressBar->setValue(bytesWritten);

    if((bytesWritten==totalBytes||bytesWritten==2*totalBytes)&&bytesWritten){
       // //qDebug()<<signature.size();
        if(isFileRemove){
            QFile temFile(fileName.right(fileName.size()-fileName.lastIndexOf('/')-1)+".enc");
            temFile.remove();
        }

        QDataStream sendOut(&outBlock,QIODevice::WriteOnly);
    //  sendOut.setVersion(QDataStream::Qt_5_12);
        quint64 tem1=encryKey.size(),tem2=encryIV.size(),tem3=signature.size();
        sendOut.writeRawData(reinterpret_cast<char*>(&tem1),sizeof(tem1));
        //qDebug()<<outBlock.size();
        sendOut.writeRawData(reinterpret_cast<char*>(&tem2),sizeof(tem2));
        //qDebug()<<outBlock.size();
        sendOut.writeRawData(reinterpret_cast<char*>(&tem3),sizeof(tem3));
        //qDebug()<<outBlock.size();
        sendOut.writeRawData(encryKey.c_str(),encryKey.size());
        //qDebug()<<outBlock.size();
        sendOut.writeRawData(encryIV.c_str(),encryIV.size());
        //qDebug()<<outBlock.size();
        sendOut.writeRawData(signature.c_str(),signature.size());
        //qDebug()<<outBlock.size();
        this->cryptoSocket->write(outBlock);
        //qDebug()<<outBlock.size();
        outBlock.resize(0);
        bytesWritten=0;
        totalBytes=0;
        bytestoWrite=0;
        localFile->close();
        delete localFile;
    }
}

void CryptoClient::update_message_send_file(){
    QString str="Begin send file!";
    update_message_in_brower("You",str);
}

void CryptoClient::update_message_establish_connection(){
    QString str="Establish connection successfully!";
    update_message_in_brower("You",str);
}

void CryptoClient::update_message_close_connection(){
    QString str="Close control and file connection.";
    update_message_in_brower("You",str);
}

//generate key
void CryptoClient::generate_private_key(){
    int privateKeyIndex=ui->comboBox_PrivateOption->currentIndex();
    CryptoMannager->generate_private_key(
                QCoreApplication::applicationDirPath(), privateKeyIndex);
    update_message_in_brower("You","Generate "+ui->comboBox_PrivateOption->currentText()+" private key!");
}

void CryptoClient::generate_public_connection_key(){
    int publicConnectionIndex=ui->comboBox_PublicConnectOption->currentIndex();
    publicConnectionKeyName= CryptoMannager->generate_public_connection_key(publicConnectionIndex);
    ui->lineEdit_PublicConnectPosition->setText(publicConnectionKeyName);
    update_message_in_brower("You","Generate "+ui->comboBox_PublicConnectOption->currentText()+" public connection key!");
}

void CryptoClient::generate_digital_signature_key(){
    int digitalSignatureIndex=ui->comboBox_DigitalOption->currentIndex();
    digitalSignatureKeyName=CryptoMannager->generate_digital_signature_key(digitalSignatureIndex);
    ui->lineEdit_DigitalKeyPosition->setText(digitalSignatureKeyName);
    update_message_in_brower("You","Generate "+ui->comboBox_DigitalOption->currentText()+" digital signature key!");
}

void CryptoClient::select_public_connection_key(){
    this->publicConnectionKeyName=QFileDialog::getOpenFileName(this,"Open a public key(public) file","/","files (*)");
    ui->lineEdit_PublicConnectPosition->setText(publicConnectionKeyName);
    update_message_in_brower("You","select public connection key in "+this->publicConnectionKeyName);
}

void CryptoClient::select_digital_signature_key(){
    this->digitalSignatureKeyName=QFileDialog::getOpenFileName(this,"Open a digital signature(private) key file","/","files (*)");
    ui->lineEdit_DigitalKeyPosition->setText(digitalSignatureKeyName);
    update_message_in_brower("You","select digital signature key in "+this->digitalSignatureKeyName);
}

