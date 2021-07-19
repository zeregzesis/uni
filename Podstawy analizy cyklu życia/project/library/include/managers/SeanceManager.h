#ifndef CINEMA_SEANCEMANAGER_H
#define CINEMA_SEANCEMANAGER_H

#include "includeHeader.h"
#include "typedefs.h"

#include "Seance.h"
#include "Repository.h"

//manage all Seance instances

class SeanceManager {
private:
    RepositoryPtr<SeancePtr,SeancePredicate> seances = std::make_shared<Repository<SeancePtr,SeancePredicate>>();
public:
    SeanceManager();

    SeanceManager(const RepositoryPtr<SeancePtr,SeancePredicate> &seances);

    SeancePtr createSeance(pt::ptime date, int seats, const FilmPtr& film);
    std::string toString();

    const RepositoryPtr<SeancePtr,SeancePredicate> &getSeances() const;

    virtual ~SeanceManager();
};


#endif //CINEMA_SEANCEMANAGER_H
