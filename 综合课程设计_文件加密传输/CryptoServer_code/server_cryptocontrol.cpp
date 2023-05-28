#include "server_cryptocontrol.h"

#include "cryptlib.h"
#include "qdebug.h"
#include "osrng.h"
#include "rsa.h"
#include "filters.h"
#include "gcm.h"
#include "modes.h"
#include "aes.h"
#include "qdir.h"
#include "xed25519.h"

Server_CryptoControl::Server_CryptoControl()
{
}

void Server_CryptoControl::save(const std::string& filename,CryptoPP::BufferedTransformation& bt)
{
    CryptoPP::FileSink file(filename.c_str());
    bt.CopyTo(file);
    file.MessageEnd();
}

void Server_CryptoControl::load(const std::string&filename,CryptoPP::BufferedTransformation& bt){
    CryptoPP::FileSource file(filename.c_str(),true);
    file.TransferTo(bt);
    bt.MessageEnd();
}

void Server_CryptoControl::save_private_key(const std::string&filename,const CryptoPP::PrivateKey & key){
    CryptoPP::ByteQueue queue;
    key.Save(queue);
    save(filename,queue);
}

void Server_CryptoControl::save_public_key(const std::string &filename, const CryptoPP::PublicKey &key){
    CryptoPP::ByteQueue queue;
    key.Save(queue);
    save(filename,queue);
}
void Server_CryptoControl::load_private_key(const std::string &filename,CryptoPP::PrivateKey &key){
    CryptoPP::ByteQueue queue;
    load(filename,queue);
    key.Load(queue);
}

void Server_CryptoControl::load_public_key(const std::string &filename, CryptoPP::PublicKey &key){
    CryptoPP::ByteQueue queue;
    load(filename,queue);
    key.Load(queue);
}

bool Server_CryptoControl::decrypt_file(QString filePosition,int index){
    //qDebug()<<"Decrypt file!";
    filePosition=QDir::toNativeSeparators(filePosition);
    std::string decryptedFile=filePosition.toStdString();

    decryptedFile=std::string(decryptedFile.begin(),decryptedFile.end()-4);
    bool result=false;
    if(index==0){
        CryptoPP::CBC_Mode<CryptoPP::AES>::Decryption decryptor;
        CryptoPP::SecByteBlock key(reinterpret_cast<const unsigned char*>(privateKey.c_str()),privateKey.size()),
                                iv(reinterpret_cast<const unsigned char*>(IV.c_str()),IV.size());
        decryptor.SetKeyWithIV(key,key.size(),iv,iv.size());
        CryptoPP::FileSource fs(filePosition.toStdString().c_str(),true,
                                new CryptoPP::StreamTransformationFilter(decryptor,
                                                                         new CryptoPP::FileSink(decryptedFile.c_str())
                                                                         )
                                );
        result=true;
    } else if(index==1){
        CryptoPP::GCM<CryptoPP::AES,CryptoPP::GCM_2K_Tables>::Decryption decryptor;
        CryptoPP::SecByteBlock key(reinterpret_cast<const unsigned char*>(privateKey.c_str()),privateKey.size()),
                                iv(reinterpret_cast<const unsigned char*>(IV.c_str()),IV.size());
        decryptor.SetKeyWithIV(key,key.size(),iv,iv.size());
        CryptoPP::AuthenticatedDecryptionFilter df(decryptor,
                                                   new CryptoPP::FileSink(decryptedFile.c_str()),
                                                   16,GCM_AES_128_TAG_SIZE);
        CryptoPP::FileSource(filePosition.toStdString().c_str(),true,
                             new CryptoPP::Redirector(df));
        result=df.GetLastResult();
    }
    return result;
}

/// \brief valinate the digital signature of file transformed by Crypto Socket
/// \param key position
/// \param file position
/// \param the index of ui combox, now it 's useless because it only support ED25519 signature scheme
bool Server_CryptoControl::valinate_digital_signature(QString keyPosition,QString filePosition,int index){
    //qDebug()<<keyPosition;
    //qDebug()<<filePosition<<' '<<index;
    CryptoPP::byte result=0;
    keyPosition=QDir::toNativeSeparators(keyPosition);
    filePosition=QDir::toNativeSeparators(filePosition);
    //debug
    //CryptoPP::StringSource(signature, true, new CryptoPP::HexEncoder(new CryptoPP::FileSink("sign.txt")));
    if(index==0){
        // //qDebug()<<"test ed25519";
        CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
        CryptoPP::FileSource fs1(keyPosition.toStdString().c_str(),true);
        CryptoPP::ed25519::Verifier verifier;
        verifier.AccessPublicKey().Load(fs1);
        if(!verifier.AccessPublicKey().Validate(strongRNG,3)){
            //qDebug()<<"Error: invalid ed25519 key!";
        }
        std::ifstream stream(filePosition.toStdString());
        if(!stream.is_open()){
            //qDebug()<<"Error: fail to open the file to be valinated!";
        }

        result=verifier.VerifyStream(stream,(const CryptoPP::byte*)&signature[0],signature.size());
    } else {
        //qDebug()<<"Error:invalid digital signature index!";
    }
    return result;
}


/// \brief encrypt message by selected public key scheme
/// \param key position
/// \param file position
/// \param the index of ui combox, now it 's useless because it only support RSA Encryption Scheme
std::string Server_CryptoControl::connect_by_public_key(QString keyPosition,std::string message,int index){
    CryptoPP::ByteQueue publicKey;
    std::string messageText;
    keyPosition=QDir::toNativeSeparators(keyPosition);
   // //qDebug()<<keyPosition<<' '<<QString::fromStdString(message)<<' '<<message.size();

    if(index==0){
        //to avoid invalid public key from unbelievable source, we should valinate it before it's used.
        CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
        CryptoPP::RSA::PrivateKey RSAkey;
        this->load_private_key(keyPosition.toStdString(),RSAkey);

        if(!RSAkey.Validate(strongRNG,3)){
           //qDebug()<<"Error! invalid RSA key!";
        }
        CryptoPP::RSAES<CryptoPP::OAEP<CryptoPP::SHA256>>::Decryptor decryptor(RSAkey);
        //encryption by filter supported by CryptoPP
        //RSA OAEP scheme based on SHA256 is CCA-secure.
        CryptoPP::StringSource ss(message,true,
                                  new CryptoPP::PK_DecryptorFilter(strongRNG,decryptor,
                                                                   new CryptoPP::StringSink(messageText)
                                                                   )
                                  );
    }
    //qDebug()<<"success in public key";
    return messageText;
}
