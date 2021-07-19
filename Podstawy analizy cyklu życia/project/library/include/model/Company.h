#ifndef CINEMA_COMPANY_H
#define CINEMA_COMPANY_H
#include "Client.h"
#include "Address.h"
#include "typedefs.h"
#include "includeHeader.h"

// Company Client, for puropses of companies organising group events
// this should be used for all insitutions, including schools, that buy tickets for larger groups

class Company: public Client {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version){
        ar & boost::serialization::base_object<Client>(*this);
        ar & name;
        ar & nip;
        ar & address;
    }
    std::string name;
    std::string nip;
    AddressPtr address;
public:

    Company();

    Company(int maxNumber, ClientType clientType, const std::string &name, const std::string &nip,
            const AddressPtr &address);

    const std::string &getName() const;

    const std::string &getNip() const;

    const AddressPtr &getAddress() const;

    float getDiscount();

    std::string toString() override ;

    virtual ~Company();
};



#endif //CINEMA_COMPANY_H
