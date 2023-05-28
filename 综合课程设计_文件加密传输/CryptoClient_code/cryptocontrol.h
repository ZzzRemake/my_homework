#ifndef CRYPTOCONTROL_H
#define CRYPTOCONTROL_H

#include "qdebug.h"
#include "filters.h"
#include "hex.h"
#include "files.h"
#include "rsa.h"
#include "osrng.h"
#include "string"


class CryptoControl
{
private:
    void load(const std::string& filename,CryptoPP::BufferedTransformation& bt);
    void save(const std::string& filename, CryptoPP::BufferedTransformation& bt);

    CryptoPP::SecByteBlock privateKey;
    CryptoPP::SecByteBlock IV;

    const int GCM_AES_128_TAG_SIZE=16;
    const int GCM_AES_128_IV_SIZE=12;
    const int AES_128_BLOCK_SIZE=16;
public:
    CryptoControl();

    QString generate_digital_signature_key(int index);
    QString generate_public_connection_key(int index);
    void generate_private_key(QString absPosition,int index);

    std::string create_digital_signature(QString keyPosition,QString filePosition,int index);
    std::string create_public_connection(QString keyPosition,std::string message,int index);
    void create_encrypt_file(QString filePosition,int index);

    void save_private_key(const std::string&filename,const CryptoPP::PrivateKey & key);
    void save_public_key(const std::string&filename,const CryptoPP::PublicKey & key);
    void load_private_key(const std::string&filename,CryptoPP::PrivateKey & key);
    void load_public_key(const std::string&filename,CryptoPP::PublicKey & key);
    std::string get_privatekey(){
        return std::string(reinterpret_cast<const char*>(&privateKey[0]),privateKey.size());
    };
    std::string get_iv(){
        return std::string(reinterpret_cast<const char*>(&IV[0]),IV.size());
    };
};

#endif // CRYPTOCONTROL_H
