#include <boost/test/unit_test.hpp>
#include "typedefs.h"
#include "includeHeader.h"
#include "Company.h"

struct CompanyData{
    int maxNumber = 4;
    ClientType clientType = Casual;
    std::string name="PolBudex";
    std::string nip="0000";
    AddressPtr a;
    std::string city="Wadowice";
    std::string street="JanaPawla";
    std::string number="9/11";
    Company* c;
    CompanyData(){
        a=std::make_shared<Address>(city,street,number);
        c=new Company(maxNumber,clientType,name,nip,a);
    }
    ~CompanyData(){
        delete c;
    }
};
BOOST_FIXTURE_TEST_SUITE(TestSuiteCompany,CompanyData)
    BOOST_AUTO_TEST_CASE(getterTest){
        BOOST_TEST(c->getName()=="PolBudex");
        BOOST_TEST(c->getNip()=="0000");
        BOOST_TEST(c->getAddress() == a);
    }
    BOOST_AUTO_TEST_CASE(getDiscountTest){
        BOOST_TEST(c->getDiscount()==0.9,boost::test_tools::tolerance(0.01));
    }
BOOST_AUTO_TEST_SUITE_END()


