#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "Ticket.h"
#include "Seance.h"
#include "Client.h"

struct TicketInstanceData{

    pt::ptime dateInitial = pt::ptime(gr::date(2020,5,1),pt::hours(9)+pt::minutes(25));
    int seanceSeatsInitial = 200;
    SeancePtr seance;

    int maxNumberInitial = 4;
    ClientType clientTypeInitial = Casual;
    ClientPtr client;

    int ticketSeatsInitial = 2;
    int priceInitial = 1000;
    TicketType ticketTypeInitial = Normal;

    TicketPtr ticket;

    TicketInstanceData(){
        seance = std::make_shared<Seance>(dateInitial,seanceSeatsInitial, nullptr);
        client = std::make_shared<Client>(maxNumberInitial,clientTypeInitial);
        ticket = std::make_shared<Ticket>(ticketSeatsInitial,priceInitial,ticketTypeInitial,seance,client);
    }
};

BOOST_FIXTURE_TEST_SUITE(TicketClassTests, TicketInstanceData)

    BOOST_AUTO_TEST_CASE(ConstructorAndGetterTests){
        BOOST_TEST(ticket->getSeats() == ticketSeatsInitial);
        BOOST_TEST(ticket->getPrice() == priceInitial);
        BOOST_TEST(ticket->getTicketType() == ticketTypeInitial);
        BOOST_TEST(ticket->getSeance() == seance);
        BOOST_TEST(ticket->getClient() == client);
    }

BOOST_AUTO_TEST_SUITE_END()