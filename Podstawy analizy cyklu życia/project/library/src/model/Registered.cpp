#include "Registered.h"

// constructor - initialize all fields while calling base class constructor
Registered::Registered(int maxNumber, ClientType clientType, const std::string &firstName, const std::string &lastName,
                       const std::string &id) : Client(maxNumber, clientType), firstName(firstName), lastName(lastName), id(id) {}

// constructor - nothing to initialize
Registered::Registered() = default;


// begin - simple getters and setters
const std::string &Registered::getFirstName() const {
    return firstName;
}

void Registered::setFirstName(const std::string &newFirstName) {
    Registered::firstName = newFirstName;
}

const std::string &Registered::getLastName() const {
    return lastName;
}

void Registered::setLastName(const std::string &newLastName) {
    Registered::lastName = newLastName;
}

const std::string &Registered::getId() const {
    return id;
}

void Registered::setId(const std::string &newId) {
    Registered::id = newId;
}
// end - simple getters and setters

// modifier to base class discount
float Registered::getDiscount() {
    return 0.95*Client::getDiscount();
}

// output object as string
std::string Registered::toString() {
    return Client::toString()+"Registered::firstName:"+firstName+";lastname:"+lastName+";id:"+id+";;";
}

// destructor - nothing inside to destroy alongside this
Registered::~Registered() = default;