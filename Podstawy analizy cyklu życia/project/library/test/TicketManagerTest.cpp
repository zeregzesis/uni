#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "TicketManager.h"
#include "Seance.h"
#include "Film.h"
#include "Ticket.h"
#include "Client.h"

struct TicketManagerInstanceData{

    pt::ptime dateInitial1 = pt::ptime(gr::date(2020,5,1),pt::hours(9)+pt::minutes(25));
    int seanceSeatsInitial = 200;
    SeancePtr seanceInitial;

    pt::time_duration filmLength = pt::hours(1) + pt::minutes(35);
    std::string filmTitle = "Shrek";
    pt::ptime filmPremiere = pt::ptime(gr::date(2001,4,22));
    FilmPtr filmInitial;

    ClientPtr clientInitial;

    TicketManagerPtr man;

    TicketManagerInstanceData(){
        filmInitial = std::make_shared<Film>(filmLength, filmTitle, filmPremiere);
        seanceInitial = std::make_shared<Seance>(dateInitial1, seanceSeatsInitial, filmInitial);
        clientInitial = std::make_shared<Client>(2, Regular);
        man = std::make_shared<TicketManager>();
    }
};

BOOST_FIXTURE_TEST_SUITE(TicketManagerClassTests, TicketManagerInstanceData)

BOOST_AUTO_TEST_CASE(CreateTicketMethodTests){

    //create needed variables
    int seats;
    TicketType type = Normal;
    TicketPtr ticket;

    //maxNumber smaller than seats
    //seats = 10;
    //BOOST_CHECK_THROW(ticket = man->createTicket(seats,type,seanceInitial,clientInitial),std::logic_error);

    //ticketType incompltible with number of seats
    //seats = 1;
    //type = Group;

    //BOOST_CHECK_THROW(ticket = man->createTicket(seats,type,seanceInitial,clientInitial),std::logic_error);

    //type = Family;
    //BOOST_CHECK_THROW(ticket = man->createTicket(seats,type,seanceInitial,clientInitial),std::logic_error);

    //correct ticket, that creates condition for seats > freeSeats test
    ClientPtr clientNew = std::make_shared<Client>(200, Regular);
    seats = 200;
    type = Family;

    BOOST_CHECK(ticket = man->createTicket(seats,type,seanceInitial,clientNew));

    BOOST_TEST(ticket->getPrice() == 307800);

    //more seats than available
    //seats = 1;
    //type = Normal;
    //BOOST_CHECK_THROW(ticket = man->createTicket(seats,type,seanceInitial,clientInitial),std::logic_error);
}

BOOST_AUTO_TEST_CASE(PayMethodTests){
    TicketPtr ticket = man->createTicket(1, Normal, seanceInitial, clientInitial);
    TicketPredicate pred = [ticket](TicketPtr t){return t == ticket;};
    BOOST_TEST(man->getReservation()->find(pred) == ticket);
    man->pay(ticket);
    BOOST_TEST(man->getPaid()->find(pred) == ticket);
}

    BOOST_AUTO_TEST_CASE(CancelMethodTests){
        TicketPtr ticket = man->createTicket(1, Normal, seanceInitial, clientInitial);
        TicketPredicate pred = [ticket](TicketPtr t){return t == ticket;};
        BOOST_TEST(man->getReservation()->find(pred) == ticket);
        man->cancel(ticket);
        BOOST_TEST(man->getReservation()->find(pred)==nullptr);
    }


BOOST_AUTO_TEST_SUITE_END()
//, boost::test_tools::tolerance(0.01)