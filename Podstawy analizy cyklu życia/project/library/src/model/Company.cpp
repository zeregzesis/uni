#include "Company.h"

// constructor - initialize all fields while calling base class constructor
Company::Company(int maxNumber, ClientType clientType, const std::string &name, const std::string &nip,
                 const AddressPtr &address) : Client(maxNumber, clientType), name(name), nip(nip), address(address) {}

// constructor - nothing to initialize
Company::Company() = default;

// begin - simple getters and setters
const std::string &Company::getName() const {
    return name;
}

const std::string &Company::getNip() const {
    return nip;
}

const AddressPtr &Company::getAddress() const {
    return address;
}
// end - simple getters and setters

// modifier to base class discount
float Company::getDiscount() {

    return 0.9*Client::getDiscount();
}

// output object as string
std::string Company::toString() {
    return Client::toString()+"Company::name"+name+";nip:"+nip+";address:"+address->toString()+";;";
}

// destructor - nothing inside to destroy alongside this
Company::~Company() = default;
