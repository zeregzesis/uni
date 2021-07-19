#ifndef CINEMA_FILM_H
#define CINEMA_FILM_H
#include "typedefs.h"
#include "includeHeader.h"

// all needed data about given movie that's available for screening

class Film {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version){
        ar & length;
        ar & title;
        ar & premiere;
    }
    pt::time_duration length;
    std::string title;
    pt::ptime premiere;
public:
    Film();

    Film(const pt::time_duration &length, const std::string &title, const pt::ptime &premiere);

    const pt::time_duration &getLength() const;

    const std::string &getTitle() const;

    const pt::ptime &getPremiere() const;

    std::string toString();

    virtual ~Film();
};


#endif //CINEMA_FILM_H
