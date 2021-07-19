#include "Ticket.h"
#include "Seance.h"
#include "Client.h"

// constructor - initialize all fields while calling base class constructor
Ticket::Ticket(int seats, int price, TicketType ticketType, const SeancePtr &seance, const ClientPtr &client):
	seats(seats), price(price), ticketType(ticketType), seance(seance), client(client) {}

// constructor - nothing to initialize
Ticket::Ticket() = default;

// begin - simple getters and setters
int Ticket::getSeats() const {
    return seats;
}

int Ticket::getPrice() const {
    return price;
}

TicketType Ticket::getTicketType() const {
    return ticketType;
}

const SeancePtr &Ticket::getSeance() const {
    return seance;
}

const ClientPtr &Ticket::getClient() const {
    return client;
}

void Ticket::setSeance(const SeancePtr &newSeance) {
    Ticket::seance = newSeance;
}

void Ticket::setClient(const ClientPtr &newClient) {
    Ticket::client = newClient;
}
// end - simple getters and setters

// output object as string, call same method for contained objects
std::string Ticket::toString() {
    return "Ticket::seats:"+std::to_string(seats)+";price:"+ std::to_string(price)+";ticketType:"+ticketTypeMap[ticketType]+";seance:"+seance->toString()+";client:"
    +client->toString()+";;";
}

// destructor - smart pointers handle contained object's destruction
Ticket::~Ticket() = default;
