
#include "ClientManager.h"
#include "Registered.h"
#include "Company.h"

// constructor - nothing to initialize
ClientManager::ClientManager() = default;

// constructor - if repository was created before we can initialize manager with it
ClientManager::ClientManager(const RepositoryPtr<ClientPtr,ClientPredicate> &clients) : clients(clients) {}

// create new Client of subtype Registered and add to repository
ClientPtr ClientManager::createRegistered(ClientType clientType, std::string firstName, std::string lastName, std::string id) {
    ClientPredicate find1 = [id](ClientPtr c2) { return typeid(*c2) == typeid(Registered) && std::dynamic_pointer_cast<Registered>(c2)->getId() == id; };
    try {
        if (clients->find(find1) != nullptr) throw std::logic_error("Registered client already exists");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
    int maxNumber = 4;
    modifyMaxNumber(maxNumber, clientType);
    ClientPtr c1 = std::make_shared<Registered>(maxNumber, clientType, firstName, lastName, id);
    clients->add(c1);
    return c1;
}

// create new Client of subtype Company and add to repository
ClientPtr ClientManager::createCompany(ClientType clientType, std::string name, std::string nip, AddressPtr address) {
    ClientPredicate find1 = [nip](ClientPtr c2) { return typeid(*c2) == typeid(Company) && std::dynamic_pointer_cast<Company>(c2)->getNip() == nip; };
    try {
        if (clients->find(find1) != nullptr) throw std::logic_error("Company client already exists");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
    int maxNumber = 20;
    modifyMaxNumber(maxNumber, clientType);
    ClientPtr c1 = std::make_shared<Company>(maxNumber, clientType, name, nip, address);
    clients->add(c1);
    return c1;
}

// get the repository containing all clients as const, to protect from changing it outside of this class
const RepositoryPtr<ClientPtr,ClientPredicate>&ClientManager::getClients() const {
    return clients;
}

// toString calling same name method in repository
std::string ClientManager::toString() {
    return "ClientManager::"+clients->toString()+";;";
}

// destructor - smart pointers handle contained object's destruction
ClientManager::~ClientManager() = default;