#ifndef CINEMA_FILMMANAGER_H
#define CINEMA_FILMMANAGER_H

#include "includeHeader.h"
#include "typedefs.h"
#include "Repository.h"
#include "Film.h"

//manage all Film instances

class FilmManager {
private:
    RepositoryPtr<FilmPtr, FilmPredicate> films = std::make_shared<Repository<FilmPtr,FilmPredicate>>();
public:
    FilmManager();

    FilmManager(const RepositoryPtr<FilmPtr, FilmPredicate> &films);

    FilmPtr createFilm(pt::time_duration length, std::string title,pt::ptime premiere);

    const RepositoryPtr<FilmPtr,FilmPredicate> &getFilms() const;

    std::string toString();

    virtual ~FilmManager();
};


#endif //CINEMA_FILMMANAGER_H
