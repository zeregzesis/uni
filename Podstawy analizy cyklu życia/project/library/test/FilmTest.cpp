#include <boost/test/unit_test.hpp>
#include "typedefs.h"
#include "includeHeader.h"
#include "Film.h"

struct FilmData{
        pt::time_duration length=pt::hours(2) + pt::minutes(30);
        std::string title="Smolensk";
        pt::ptime premiere=pt::ptime(gr::date(2020,1,21));
        FilmPtr f;
        FilmData(){
            f=std::make_shared<Film>(length,title,premiere);
        };
};

BOOST_FIXTURE_TEST_SUITE(TestSuiteFilm,FilmData)
    BOOST_AUTO_TEST_CASE(getterTest){
        BOOST_TEST(f->getLength() == pt::hours(2) + pt::minutes(30));
        BOOST_TEST(f->getTitle()=="Smolensk");
        BOOST_TEST(f->getPremiere()==pt::ptime(gr::date(2020,1,21)));
    }
BOOST_AUTO_TEST_SUITE_END()

