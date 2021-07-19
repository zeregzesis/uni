#ifndef CINEMA_ADDRESS_H
#define CINEMA_ADDRESS_H
#include "typedefs.h"
#include "includeHeader.h"

// address of a given Client

class Address {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version)
    {
        ar & city;
        ar & street;
        ar & number;
    }

    std::string city;
    std::string street;
    std::string number;
public:
    Address();

    Address(const std::string &city, const std::string &street, const std::string &number);

    const std::string &getCity() const;


    const std::string &getStreet() const;


    const std::string &getNumber() const;

    std::string toString();

    virtual ~Address();
};




#endif //CINEMA_ADDRESS_H
