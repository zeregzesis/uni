#include "Address.h"

// constructor - nothing to initialize
Address::Address() = default;

// constructor - initialize all fields
Address::Address(const std::string &city, const std::string &street, const std::string &number) : city(city),street(street),number(number) {}

// begin - simple getters and setters
const std::string &Address::getCity() const {
    return city;
}

const std::string &Address::getStreet() const {
    return street;
}

const std::string &Address::getNumber() const {
    return number;

}
// end - simple getters and setters

// output object as string
std::string Address::toString() {
    return "Address::city:"+city+";street:"+street+";number:"+number+";;";
}

// destructor - nothing inside to destroy alongside this
Address::~Address() = default;
