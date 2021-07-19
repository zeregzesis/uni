#ifndef CINEMA_TICKETMANAGER_H
#define CINEMA_TICKETMANAGER_H

#include "typedefs.h"
#include "includeHeader.h"
#include "Repository.h"
#include "Ticket.h"

// manage all Ticket instances, with division between only reserved and already paid for

class TicketManager {
private:
    RepositoryPtr<TicketPtr, TicketPredicate> reservation = std::make_shared<Repository<TicketPtr,TicketPredicate>>();
    RepositoryPtr<TicketPtr, TicketPredicate> paid = std::make_shared<Repository<TicketPtr,TicketPredicate>>();
public:

    TicketManager();
    const RepositoryPtr<TicketPtr, TicketPredicate>getReservation() const;

    const RepositoryPtr<TicketPtr, TicketPredicate>getPaid() const;
    TicketManager(const RepositoryPtr<TicketPtr, TicketPredicate> &reservation, const RepositoryPtr<TicketPtr, TicketPredicate> &paid);

    TicketPtr createTicket(int seats, TicketType ticketType, SeancePtr seance, ClientPtr client, int baseTicketPrice = 20);

    void pay(TicketPtr ticket);

    void cancel(TicketPtr ticket);

    std::string toString();

    virtual ~TicketManager();
};


#endif //CINEMA_TICKETMANAGER_H
