#include "Client.h"

// constructor - initialize all fields
Client::Client(int maxNumber, ClientType clientType) : maxNumber(maxNumber), clientType(clientType) {}

// constructor - nothing to initialize
Client::Client() = default;

// begin - simple getters and setters
int Client::getMaxNumber() const {
    return maxNumber;
}

void Client::setMaxNumber(int newMaxNumber) {
    Client::maxNumber = newMaxNumber;
}

ClientType Client::getClientType() const {
    return clientType;
}

void Client::setClientType(ClientType newClientType) {
    Client::clientType = newClientType;
}
// end - simple getters and setters

// discount based on client type (enum)
float Client::getDiscount() {
    switch (clientType)
    {
        case Regular:
            return 0.95;
        case Junior:
            return 0.5;
        case Senior:
            return 0.65;
        case Casual:
            return 1.0;
        case Premium:
            return 0.75;
    }
    return 0;
}

// output object as string
std::string Client::toString() {
    return "Client::maxNumber"+std::to_string(maxNumber)+";clientType:"+clientTypeMap[clientType]+";";
}

// destructor - nothing inside to destroy alongside this
Client::~Client() = default;
