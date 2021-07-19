#ifndef CINEMA_REGISTERED_H
#define CINEMA_REGISTERED_H
#include "Client.h"
#include "typedefs.h"
#include "includeHeader.h"

// Client that has registered (regular client)
// to be used for all individual clients, manager has built-in limit on number of tickets this client can buy
// for more tickets with one purchase you nned to be Company, not only Registered

class Registered: public Client {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version){
        ar & boost::serialization::base_object<Client>(*this);
        ar & firstName;
        ar & lastName;
        ar & id;
    }
    std::string firstName;
    std::string lastName;
    std::string id;
public:

    Registered();

    Registered(int maxNumber, ClientType clientType, const std::string &firstName, const std::string &lastName,
               const std::string &id);

    const std::string &getFirstName() const;

    void setFirstName(const std::string &newFirstName);

    const std::string &getLastName() const;

    void setLastName(const std::string &newLastName);

    const std::string &getId() const;

    void setId(const std::string &newId);

    float getDiscount();

    std::string toString() override ;

    virtual ~Registered();
};

#endif //CINEMA_REGISTERED_H
