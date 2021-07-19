#ifndef CINEMA_CLIENT_H
#define CINEMA_CLIENT_H
#include "typedefs.h"
#include "includeHeader.h"
#include "utils/EnumString.h"

// base class, to initialize once and use whenever selling to one-time customer
// regular customers must be handeled by child classes as different rules apply

// all client types, based on cinema policy on membership and discounts
enum ClientType{
    Regular,
    Junior,
    Senior,
    Casual,
    Premium
};
Begin_Enum_String( ClientType )
{
    Enum_String( Regular );
    Enum_String( Junior );
    Enum_String( Senior );
    Enum_String( Casual );
    Enum_String( Premium );
}
End_Enum_String;

class Client {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version){
        ar.template register_type<Registered>();
        ar.template register_type<Company>();
        ar & maxNumber;
        ar & clientType;
    }
    int maxNumber;
    ClientType clientType;
    std::map<ClientType,std::string> clientTypeMap = {{Regular,"Regular"},{Junior,"Junior"},{Senior,"Senior"},{Casual,"Casual"},{Premium,"Premium"}};
public:
    Client(int maxNumber, ClientType clientType);

    Client();

    int getMaxNumber() const;

    void setMaxNumber(int newMaxNumber);

    ClientType getClientType() const;

    void setClientType(ClientType newClientType);

    float getDiscount();

    virtual std::string toString();

    virtual ~Client();
};


#endif //CINEMA_CLIENT_H