#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "Repository.h"
#include "Ticket.h"

struct RepositoryInstanceData{

    int seatsInitial1 = 2;
    int seatsInitial2 = 4;
    int priceInitial = 1000;
    TicketType ticketTypeInitial = Normal;
    TicketPtr ticket1;
    TicketPtr ticket2;

    RepositoryPtr<TicketPtr,TicketPredicate> repo;

    RepositoryInstanceData(){
        
        ticket1 = std::make_shared<Ticket>(seatsInitial1,priceInitial,ticketTypeInitial, nullptr, nullptr);
        ticket2 = std::make_shared<Ticket>(seatsInitial2,priceInitial,ticketTypeInitial, nullptr, nullptr);
        repo = std::make_shared<Repository<TicketPtr,TicketPredicate>>();
        repo->add(ticket1);
    }
};

BOOST_FIXTURE_TEST_SUITE(RepositoryClassTests, RepositoryInstanceData)

    BOOST_AUTO_TEST_CASE(AddAndSizeTests){
        BOOST_TEST_REQUIRE(repo->size() == 1);
        repo->add(ticket2);
        BOOST_TEST(repo->size() == 2);
    }

    BOOST_AUTO_TEST_CASE(RemoveTests) {
        repo->remove(ticket1);
        BOOST_TEST(repo->size() == 0);
    }

    BOOST_AUTO_TEST_CASE(GetTests){

        //id in range
        repo->add(ticket2);
        BOOST_TEST(repo->get(1) == ticket2);

        //id out of range
    //BOOST_CHECK_THROW(repo->get(10),std::logic_error);
    }

    BOOST_AUTO_TEST_CASE(FindTests){
        repo->add(ticket2);
        //copy, because lambda can't capture
        int seatsCopy = seatsInitial1;
        TicketPredicate pred = [seatsCopy](TicketPtr t){return t->getSeats() == seatsCopy;};

        //when at least one object exists to be found
        BOOST_TEST(repo->find(pred) == ticket1);

        //when not found
        repo->remove(ticket1);
        BOOST_TEST(repo->find(pred)== nullptr);
    }

    BOOST_AUTO_TEST_CASE(FindAllTests){
        repo->add(ticket2);
        int priceCopy = priceInitial;
        TicketPredicate pred = [priceCopy](TicketPtr t){return t->getPrice() == priceCopy;};
        std::list<TicketPtr> list = repo->findAll(pred);
        std::_List_const_iterator<TicketPtr> it = list.begin();
        BOOST_TEST(*it == ticket1);
        std::advance(it,1);
        BOOST_TEST(*it == ticket2);
    }

BOOST_AUTO_TEST_SUITE_END()