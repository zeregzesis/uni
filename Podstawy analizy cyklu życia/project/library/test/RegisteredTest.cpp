#include <boost/test/unit_test.hpp>
#include "typedefs.h"
#include "includeHeader.h"
#include "Registered.h"

struct RegisteredData{
    int maxNumber = 4;
    ClientType clientType = Casual;
    std::string firstName="Janusz";
    std::string lastName="Nosacz";
    std::string id="2137420";
    std::string newFirstName="Jan";
    std::string newLastName="kowal";
    std::string newId="12345678";
    Registered* r;
    RegisteredData(){
        r= new Registered(maxNumber,clientType,firstName,lastName,id);
    }
    ~RegisteredData(){
        delete r;
    }
};
BOOST_FIXTURE_TEST_SUITE(TestSuiteRegistered,RegisteredData)
    BOOST_AUTO_TEST_CASE(getterTest1){
        BOOST_TEST(r->getFirstName()=="Janusz");
        BOOST_TEST(r->getLastName()=="Nosacz");
        BOOST_TEST(r->getId()=="2137420");
    }
    BOOST_AUTO_TEST_CASE(setterTest1){
        r->setFirstName(newFirstName);
        BOOST_TEST(r->getFirstName()=="Jan");
        r->setLastName(newLastName);
        BOOST_TEST(r->getLastName()=="kowal");
        r->setId(newId);
        BOOST_TEST(r->getId()=="12345678");
    }
    BOOST_AUTO_TEST_CASE(getDiscountTest1){
        BOOST_TEST(r->getDiscount()==0.95,boost::test_tools::tolerance(0.01));
    }
BOOST_AUTO_TEST_SUITE_END()
