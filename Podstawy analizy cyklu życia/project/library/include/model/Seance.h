#ifndef CINEMA_SEANCE_H
#define CINEMA_SEANCE_H

#include "includeHeader.h"
#include "typedefs.h"

// every screening of every movie is contained as this class's object
// used to control available seats and keep track of dates

class Film;

class Seance {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version){
        ar & date;
        ar & seats;
        ar & film;
    }
    pt::ptime date;
    int seats;
    FilmPtr film;
public:
    Seance(const pt::ptime &date, int seats, FilmPtr film);

    Seance();

    virtual ~Seance();

    const pt::ptime &getDate() const;

    int getSeats() const;

    const FilmPtr &getFilm() const;

    std::string toString();
    void setFilm(const FilmPtr &newFilm);

};


#endif //CINEMA_SEANCE_H
