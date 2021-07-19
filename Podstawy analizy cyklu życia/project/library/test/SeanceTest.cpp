#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "Seance.h"
#include "Film.h"

struct SeanceInstanceData{

    pt::ptime dateInitial = pt::ptime(gr::date(2020,5,1),pt::hours(9)+pt::minutes(25));
    int seatsInitial = 200;
    SeancePtr seance;

    pt::time_duration filmLength = pt::hours(1) + pt::minutes(35);
    std::string filmTitle = "Shrek";
    pt::ptime filmPremiere = pt::ptime(gr::date(2001,4,22));
    FilmPtr filmInitial;

    SeanceInstanceData(){
        filmInitial = std::make_shared<Film>(filmLength, filmTitle, filmPremiere);
        seance = std::make_shared<Seance>(dateInitial,seatsInitial,filmInitial);
    }
};

BOOST_FIXTURE_TEST_SUITE(SeanceClassTests, SeanceInstanceData)

BOOST_AUTO_TEST_CASE(ConstructorAndGetterTests){
    BOOST_TEST(seance->getDate() == dateInitial);
    BOOST_TEST(seance->getSeats() == seatsInitial);
    BOOST_TEST(seance->getFilm() == filmInitial);
}

BOOST_AUTO_TEST_SUITE_END()