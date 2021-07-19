#include <boost/test/unit_test.hpp>
#include "typedefs.h"
#include "ClientManager.h"
#include "Client.h"
#include "Address.h"

struct ClientManagerData{
    ClientType clientType = Casual;
    ClientType clientType1 = Regular;
    ClientType clientType2 = Junior;
    ClientType clientType3 = Senior;
    ClientType clientType4 = Premium;
    std::string name="PolBudex";
    std::string nip="0000";
    AddressPtr a;
    std::string city="Wadowice";
    std::string street="JanaPawla";
    std::string number="9/11";

    std::string firstName="Janusz";
    std::string lastName="Nosacz";
    std::string id="2137420";

    ClientManagerPtr cman;
    ClientManagerData(){
        a=std::make_shared<Address>(city,street,number);
        cman=std::make_shared<ClientManager>();
    }

};
BOOST_FIXTURE_TEST_SUITE(ClientManagerTest,ClientManagerData)
    BOOST_AUTO_TEST_CASE(RegisteredCreate){
        ClientPtr c1;
        BOOST_CHECK(c1=cman->createRegistered(clientType,firstName,lastName,id));
        ClientPredicate pred = [c1](ClientPtr c){return c==c1;};
        BOOST_TEST(cman->getClients()->find(pred)==c1);
        //BOOST_CHECK_THROW(cman->createRegistered(clientType,firstName,lastName,id),std::logic_error);
    }
    BOOST_AUTO_TEST_CASE(CompanyCreate){
        ClientPtr c2;
        BOOST_CHECK(c2=cman->createCompany(clientType,name,nip,a));
        ClientPredicate pred = [c2](ClientPtr c){return c==c2;};
        BOOST_TEST(cman->getClients()->find(pred)==c2);
        //BOOST_CHECK_THROW(cman->createCompany(clientType,name,nip,a),std::logic_error);
    }
    BOOST_AUTO_TEST_CASE(ModifyMaxNumber){
        ClientPtr c1=cman->createRegistered(clientType,firstName,lastName,id);
        BOOST_TEST(c1->getMaxNumber()==6);
        cman->getClients()->remove(c1);
        ClientPtr c2=cman->createRegistered(clientType1,firstName,lastName,id);
        BOOST_TEST(c2->getMaxNumber()==8);
        cman->getClients()->remove(c2);
        ClientPtr c3=cman->createRegistered(clientType2,firstName,lastName,id);
        BOOST_TEST(c3->getMaxNumber()==9);
        cman->getClients()->remove(c3);
        ClientPtr c4=cman->createRegistered(clientType3,firstName,lastName,id);
        BOOST_TEST(c4->getMaxNumber()==10);
        cman->getClients()->remove(c4);
        ClientPtr c5=cman->createRegistered(clientType4,firstName,lastName,id);
        BOOST_TEST(c5->getMaxNumber()==15);
        cman->getClients()->remove(c5);
        ClientPtr c6=cman->createCompany(clientType,name,nip,a);
        BOOST_TEST(c6->getMaxNumber()==38);
        cman->getClients()->remove(c6);
        ClientPtr c7=cman->createCompany(clientType1,name,nip,a);
        BOOST_TEST(c7->getMaxNumber()==40);
        cman->getClients()->remove(c7);
        ClientPtr c8=cman->createCompany(clientType2,name,nip,a);
        BOOST_TEST(c8->getMaxNumber()==41);
        cman->getClients()->remove(c8);
        ClientPtr c9=cman->createCompany(clientType3,name,nip,a);
        BOOST_TEST(c9->getMaxNumber()==42);
        cman->getClients()->remove(c9);
        ClientPtr c10=cman->createCompany(clientType4,name,nip,a);
        BOOST_TEST(c10->getMaxNumber()==79);
        cman->getClients()->remove(c10);
    }
BOOST_AUTO_TEST_SUITE_END()