#ifndef SERVER_CRYPTOCONTROL_H
#define SERVER_CRYPTOCONTROL_H

#include "qstring.h"
//#include "filters.h"
#include "files.h"
#include "string"

class Server_CryptoControl
{
public:
    //CryptoPP::AutoSeededX917RNG<CryptoPP::AES> strongRNG;
    //CryptoPP::AutoSeededRandomPool normalRNG;
    Server_CryptoControl();
    void load_private_key_and_IV(std::string key,std::string iv,int index);
    bool decrypt_file(QString filePosition,int index);
    bool valinate_digital_signature(QString keyPosition,QString filePosition,int index);
    std::string connect_by_public_key(QString keyPosition,std::string message,int index);

    void save_private_key(const std::string&filename,const CryptoPP::PrivateKey & key);
    void save_public_key(const std::string&filename,const CryptoPP::PublicKey & key);
    void load_private_key(const std::string&filename,CryptoPP::PrivateKey & key);
    void load_public_key(const std::string&filename,CryptoPP::PublicKey & key);
    std::string privateKey;
    std::string IV;
    std::string signature;
private:
    void load(const std::string& filename,CryptoPP::BufferedTransformation& bt);
    void save(const std::string& filename, CryptoPP::BufferedTransformation& bt);
    const int GCM_AES_128_TAG_SIZE=16;
    const int GCM_AES_128_IV_SIZE=12;
    const int AES_128_BLOCK_SIZE=16;
};

#endif // SERVER_CRYPTOCONTROL_H
