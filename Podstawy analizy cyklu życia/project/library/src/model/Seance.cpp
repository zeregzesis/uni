#include "Seance.h"
#include "Film.h"

// constructor - initialize all fields while calling base class constructor
Seance::Seance(const pt::ptime &date, int seats, FilmPtr film) : date(date), seats(seats), film(std::move(film)) {}

// constructor - nothing to initialize
Seance::Seance() = default;

// begin - simple getters and setters
const pt::ptime &Seance::getDate() const {
    return date;
}

int Seance::getSeats() const {
    return seats;
}

const FilmPtr &Seance::getFilm() const {
    return film;
}

void Seance::setFilm(const FilmPtr &newFilm) {
    Seance::film = newFilm;
}
// end - simple getters and setters

// output object as string, call same method for contained objects
std::string Seance::toString() {
    return "Seance::date:"+pt::to_simple_string(date)+";seats:"+std::to_string(seats)+film->toString()+";;";
}

// destructor - smart pointers handle contained object's destruction
Seance::~Seance() = default;