#include <boost/test/unit_test.hpp>
#include "typedefs.h"
#include "includeHeader.h"
#include "Client.h"

struct ClientData{
    int maxNumber = 4;
    int newMaxNumber = 6;
    ClientType clientType = Casual;
    ClientType newClientType = Junior;
    ClientPtr c;

    ClientData(){
        c =std::make_shared<Client>(maxNumber,clientType);
    };
};

BOOST_FIXTURE_TEST_SUITE(TestSuiteClient,ClientData)
    BOOST_AUTO_TEST_CASE(getterTest){
        BOOST_TEST(c->getMaxNumber()==4);
        BOOST_TEST(c->getClientType() == Casual);
    }
    BOOST_AUTO_TEST_CASE(setterTest){
        c->setMaxNumber(newMaxNumber);
        BOOST_TEST(c->getMaxNumber()==6);
        c->setClientType(newClientType);
        BOOST_TEST(c->getClientType() == Junior);
    }
    BOOST_AUTO_TEST_CASE(getDiscountTest){
        BOOST_TEST(c->getDiscount()==1.0);
    }
BOOST_AUTO_TEST_SUITE_END()