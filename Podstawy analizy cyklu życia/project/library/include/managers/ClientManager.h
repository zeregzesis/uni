#ifndef CINEMA_CLIENTMANAGER_H
#define CINEMA_CLIENTMANAGER_H

#include "includeHeader.h"
#include "typedefs.h"
#include "Client.h"
#include "Repository.h"

//manage all Client instances, including child classes

class ClientManager {
private:
    RepositoryPtr<ClientPtr,ClientPredicate> clients = std::make_shared<Repository<ClientPtr,ClientPredicate>>();
    void modifyMaxNumber(int &maxNumber, ClientType clientType){
        switch (clientType) {
            case Regular:
                maxNumber = maxNumber * 2;
                break;
            case Junior:
                maxNumber = (maxNumber * 2) + 1;
                break;
            case Senior:
                maxNumber = (maxNumber * 2) + 2;
                break;
            case Casual:
                maxNumber = (maxNumber * 2) - 2;
                break;
            case Premium:
                maxNumber = (maxNumber * 4) - 1;
                break;
        };
    }
public:
    ClientManager();

    ClientManager(const RepositoryPtr<ClientPtr,ClientPredicate> &clients);

    ClientPtr createRegistered(ClientType clientType,std::string firstName,std::string lastName,std::string id);
    ClientPtr  createCompany(ClientType clientType,std::string name,std::string nip,AddressPtr address);
    std::string toString();
    const RepositoryPtr<ClientPtr,ClientPredicate> &getClients() const;

    virtual ~ClientManager();

};


#endif //CINEMA_CLIENTMANAGER_H
