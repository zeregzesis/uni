#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "FilmManager.h"
#include "Film.h"

struct FilmManagerData{
    pt::time_duration length=pt::hours(2) + pt::minutes(13);
    std::string title="Bohemian Rhapsody";
    pt::ptime premiere=pt::ptime(gr::date(2018,11,2));
    FilmManagerPtr fman;
    FilmManagerData(){
        fman= std::make_shared<FilmManager>();
    }
};

BOOST_FIXTURE_TEST_SUITE(FilmManagerTest,FilmManagerData)
BOOST_AUTO_TEST_CASE(ManagerTest){
    FilmPtr f1;
    BOOST_CHECK(f1= fman->createFilm(length,title,premiere));
    FilmPredicate pred = [f1](FilmPtr f){return f==f1;};
    BOOST_TEST(fman->getFilms()->find(pred)==f1);
    //BOOST_CHECK_THROW(fman->createFilm(length,title,premiere),std::logic_error);
}
BOOST_AUTO_TEST_SUITE_END()
