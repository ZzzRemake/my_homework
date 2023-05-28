#include "cryptocontrol.h"
#include "qdebug.h"
#include "filters.h"
#include "hex.h"
#include "files.h"
#include "rsa.h"
#include "osrng.h"
#include "string"
#include "aes.h"
#include "modes.h"
#include "gcm.h"
#include "filters.h"
#include "xed25519.h"
#include "qdir.h"

CryptoControl::CryptoControl()
{

}

void CryptoControl::save(const std::string& filename,CryptoPP::BufferedTransformation& bt)
{
    CryptoPP::FileSink file(filename.c_str());
    bt.CopyTo(file);
    file.MessageEnd();
}

void CryptoControl::load(const std::string&filename,CryptoPP::BufferedTransformation& bt){
    CryptoPP::FileSource file(filename.c_str(),true);
    file.TransferTo(bt);
    bt.MessageEnd();
}

void CryptoControl::save_private_key(const std::string&filename,const CryptoPP::PrivateKey & key){
    CryptoPP::ByteQueue queue;
    key.Save(queue);
    save(filename,queue);
}

void CryptoControl::save_public_key(const std::string &filename, const CryptoPP::PublicKey &key){
    CryptoPP::ByteQueue queue;
    key.Save(queue);
    save(filename,queue);
}
void CryptoControl::load_private_key(const std::string &filename,CryptoPP::PrivateKey &key){
    CryptoPP::ByteQueue queue;
    load(filename,queue);
    key.Load(queue);
}

void CryptoControl::load_public_key(const std::string &filename, CryptoPP::PublicKey &key){
    CryptoPP::ByteQueue queue;
    load(filename,queue);
    key.Load(queue);
}

QString CryptoControl::generate_digital_signature_key(int index){
    QString position;
    CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;

    if(index==0){//ED25519
        CryptoPP::ed25519::Signer EDsigner;
        EDsigner.AccessPrivateKey().GenerateRandom(strongRNG);
        CryptoPP::ed25519::Verifier EDVerifier(EDsigner);

        CryptoPP::FileSink edprivatefs("ed25519_Signal_private.key");
        CryptoPP::FileSink edpublicfs("ed25519_Signal_public.key");

        position=QDir::currentPath()+"/ed25519_Signal_private.key";
        EDsigner.GetPrivateKey().Save(edprivatefs);
        EDVerifier.GetPublicKey().Save(edpublicfs);
    } else {//Error
        //qDebug()<<"Error: generate digital signature key index is invalid.";
    }
    return position;
}
QString CryptoControl::generate_public_connection_key(int index){
    QString position;
    CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
    CryptoPP::InvertibleRSAFunction RSAparams;
    RSAparams.GenerateRandomWithKeySize(strongRNG,3072);
    CryptoPP::RSA::PrivateKey RSAprivateKey(RSAparams);
    CryptoPP::RSA::PublicKey RSApublicKey(RSAparams);
    switch (index){
        case 0: // RSA
          //  RSAprivateKey.GenerateRandomWithKeySize(strongRNG,3072);
         //   RSApublicKey.AssignFrom(RSAprivateKey);
            if(!RSAprivateKey.Validate(strongRNG,3)||!RSApublicKey.Validate(strongRNG,3)){
               //qDebug()<<"RSA key generation failed!";
            }
            position=QDir::currentPath()+"/RSA_connect_public.key";
            save_private_key("RSA_connect_private.key",RSAprivateKey);
            save_public_key("RSA_connect_public.key",RSApublicKey);
            break;
        case 1: break;
    }
    return position;
}
void CryptoControl::generate_private_key(QString absPosition,int index){
    CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
    privateKey.resize(CryptoPP::AES::DEFAULT_KEYLENGTH);
    if(index==0){
        IV.resize(AES_128_BLOCK_SIZE);
    } else {
        IV.resize(GCM_AES_128_IV_SIZE);
    }
    strongRNG.GenerateBlock(privateKey,privateKey.size());
    strongRNG.GenerateBlock(IV,IV.size());
}

std::string CryptoControl::create_digital_signature(QString keyPosition,QString filePosition,int index){
    std::string signature;

    keyPosition=QDir::toNativeSeparators(keyPosition);
    filePosition=QDir::toNativeSeparators(filePosition);
    //qDebug()<<keyPosition;
    //qDebug()<<filePosition;
    if(index==0){
        CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
        CryptoPP::FileSource fs1(keyPosition.toStdString().c_str(),true);
        CryptoPP::ed25519::Signer signer;
        signer.AccessPrivateKey().Load(fs1);
        if(!signer.GetPrivateKey().Validate(strongRNG,3)){
            //qDebug()<<"Error: ed25519 private key invalid!";
        }

        std::ifstream stream(filePosition.toStdString());
        if(!stream.is_open()){
            //qDebug()<<"Error: fail to open the key file to stream!";
        }

        size_t siglen = signer.MaxSignatureLength();
        signature.resize(siglen);

        siglen=signer.SignStream(CryptoPP::NullRNG(),stream,(CryptoPP::byte*)&signature[0]);

        signature.resize(siglen);
        stream.close();
    } else {
        //qDebug()<<"Error: invalid digital signatrue index";
    }
    return signature;
}
std::string CryptoControl::create_public_connection(QString keyPosition,std::string message,int index){
    std::string cipherText;
    //qDebug()<<keyPosition;
    //qDebug()<<index;
    keyPosition=QDir::toNativeSeparators(keyPosition);
    if(index==0){
        CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
        CryptoPP::RSA::PublicKey RSAkey;
        load_public_key(keyPosition.toStdString(),RSAkey);
        //qDebug()<<"RSA public key decode!";
        if(!RSAkey.Validate(strongRNG,3)){
            //qDebug()<<"Error! invalid RSA key!";
        }
        CryptoPP::RSAES<CryptoPP::OAEP<CryptoPP::SHA256>>::Encryptor encryptor(RSAkey);
        CryptoPP::StringSource ss(message,true,
                                  new CryptoPP::PK_EncryptorFilter(strongRNG,encryptor,
                                                                   new CryptoPP::StringSink(cipherText)
                                                                   )
                                  );
    } else {
        //qDebug()<<"Error!";
    }
    return cipherText;
}
void CryptoControl::create_encrypt_file(QString filePosition,int index){
    //qDebug()<<filePosition<<"?";
    QString encryptedFile=filePosition.right(filePosition.size()-filePosition.lastIndexOf('/')-1)+".enc";;
    if(index==0){
       CryptoPP::CBC_Mode<CryptoPP::AES>::Encryption encryptor;
       encryptor.SetKeyWithIV(privateKey,privateKey.size(),IV);
       //qDebug()<<encryptedFile<<"!";
       CryptoPP::FileSource(filePosition.toStdString().c_str(),true,
                            new CryptoPP::StreamTransformationFilter(encryptor,
                                                                     new CryptoPP::FileSink(encryptedFile.toStdString().c_str())
                                                                     )
                            );
    } else if(index==1){
        CryptoPP::GCM<CryptoPP::AES,CryptoPP::GCM_2K_Tables>::Encryption encryptor;
        encryptor.SetKeyWithIV(privateKey,privateKey.size(),IV);
        CryptoPP::FileSource(filePosition.toStdString().c_str(),true,
                             new CryptoPP::AuthenticatedEncryptionFilter(encryptor,
                                                                     new CryptoPP::FileSink(encryptedFile.toStdString().c_str()),
                                                                         false,GCM_AES_128_TAG_SIZE
                                                                      )
                             );
    } else {
        //qDebug()<<"Error: wrong index in private key encrypted!";
    }
}
