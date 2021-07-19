#include "TicketManager.h"
#include "SeanceManager.h"
#include "FilmManager.h"
#include "ClientManager.h"
#include "Ticket.h"
#include "Seance.h"
#include "Client.h"
#include "Film.h"

// constructor - nothing to initialize
TicketManager::TicketManager() = default;

// constructor - if repositories were created before we can initialize manager with them
TicketManager::TicketManager(const RepositoryPtr<TicketPtr, TicketPredicate> &reservation, const RepositoryPtr<TicketPtr, TicketPredicate> &paid) : reservation(reservation), paid(paid) {}

// get the repository containing all tickets that are not yet paid for as const, to protect from changing it outside of this class
const RepositoryPtr<TicketPtr, TicketPredicate>TicketManager::getReservation() const {
    return reservation;
}

// get the repository containing all tickets that were paid for as const, to protect from changing it outside of this class
const RepositoryPtr<TicketPtr, TicketPredicate>TicketManager::getPaid() const {
    return paid;
}

// create new Ticket object and add it to repository
TicketPtr TicketManager::createTicket(int seats, TicketType ticketType, SeancePtr seance, ClientPtr client, int baseTicketPrice) {
	
	//check if given client can buy this amount of seats
    try {
        if (client->getMaxNumber() < seats) throw std::logic_error("client can't buy this amount of seats");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }

	//check if ticket type matches expected number of seats
    try {
        if (ticketType == Group && seats < 8) throw std::logic_error("wrong ticket type or not enough places bought");
        if (ticketType == Family && seats < 3) throw std::logic_error("wrong ticket type or not enough places bought");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
	
    //check if there are seats available
    int seatsFree = seance->getSeats();
    TicketPredicate pred = [seance](TicketPtr t) { return t->getSeance() == seance; };
    std::list<TicketPtr> taken = reservation->findAll(pred);
    taken.merge(paid->findAll(pred));
    for (TicketPtr &ticket : taken) {
            seatsFree -= ticket->getSeats();
    }
    try {
        if (seatsFree < seats) throw std::logic_error("not enought free places");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
	
    //apply discount based on premiere and weekday
    float discount = client->getDiscount();
    if (seance->getFilm()->getPremiere() + pt::hours(72) >= seance->getDate()) discount *= 1.5;
    else {
        switch (seance->getDate().date().day_of_week()) {
            case 3:
            case 5:
                discount *= 0.9;
                break;
            case 6:
            case 7:
                discount *= 1.1;
                break;
            default:
                break;
            }
        }
		
    //apply discount based on ticketType
    if (ticketType == Group) discount *= 0.95;
    else if (ticketType == Family) discount *= 0.9;


    //price kept this way to preserve real prices((float)price/100)
    float price = 100.0 * baseTicketPrice * seats * discount;


    //create Ticket
    TicketPtr ticket = std::make_shared<Ticket>(seats, (int) price, ticketType, seance, client);
    reservation->add(ticket);
    return ticket;
}

// mark reserved ticket as paid
void TicketManager::pay(TicketPtr ticket) {
    reservation->remove(ticket);
    paid->add(ticket);
}

// cancel reservation
void TicketManager::cancel(TicketPtr ticket) {
    reservation->remove(ticket);
}

// // toString calling same name method in both repositories
std::string TicketManager::toString() {
    return "TicketManager::reservation"+reservation->toString()+";paid:"+paid->toString()+";;";
}

// destructor - smart pointers handle contained object's destruction
TicketManager::~TicketManager() = default;