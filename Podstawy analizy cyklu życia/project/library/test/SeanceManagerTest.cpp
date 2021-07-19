

#include <boost/test/unit_test.hpp>
#include "includeHeader.h"
#include "typedefs.h"
#include "SeanceManager.h"
#include "Film.h"

struct SeanceManagerInstanceData{

    pt::ptime dateInitial1 = pt::ptime(gr::date(2020,5,1),pt::hours(9)+pt::minutes(25));
    int seatsInitial = 200;
    SeancePtr seance1;
    SeancePtr seance2;

    pt::time_duration filmLength = pt::hours(1) + pt::minutes(35);
    std::string filmTitle = "Shrek";
    pt::ptime filmPremiere = pt::ptime(gr::date(2001,4,22));
    FilmPtr filmInitial;

    SeanceManagerPtr man;

    SeanceManagerInstanceData(){
        filmInitial = std::make_shared<Film>(filmLength, filmTitle, filmPremiere);
        man = std::make_shared<SeanceManager>();
    }
};

BOOST_FIXTURE_TEST_SUITE(SeanceManagerClassTests, SeanceManagerInstanceData)

    BOOST_AUTO_TEST_CASE(NoFilmCreateTests){
        //BOOST_CHECK_THROW(seance1 = man->createSeance(dateInitial1,seatsInitial,nullptr),std::logic_error);
    }

    BOOST_AUTO_TEST_CASE(OtherCreateTests){

        //adding seance that does not collide with others
    BOOST_CHECK(seance1 = man->createSeance(dateInitial1,seatsInitial,filmInitial));

        //adding seance that collides with others
       // pt::ptime date = pt::ptime(gr::date(2020,5,1),pt::hours(10)+pt::minutes(25));
        //BOOST_CHECK_THROW(seance2 = man->createSeance(date,seatsInitial,filmInitial),std::logic_error);

    }

BOOST_AUTO_TEST_SUITE_END()