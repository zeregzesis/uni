#include "SeanceManager.h"
#include "Seance.h"
#include "Film.h"

// constructor - nothing to initialize
SeanceManager::SeanceManager() = default;

// constructor - if repository was created before we can initialize manager with it
SeanceManager::SeanceManager(const RepositoryPtr<SeancePtr, SeancePredicate> &seances) : seances(seances) {}

// create new Film object and add it to repository
SeancePtr SeanceManager::createSeance(pt::ptime date, int seats, const FilmPtr& film) {

    // protection from Seance without existing Film
    try {
        if (film == nullptr) throw std::logic_error("no movie provided");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
	
	// protection against duplicate entriers
    SeancePredicate pred = [date, film](const SeancePtr &s) -> bool {
        return ((date < s->getDate() && s->getDate() < date + film->getLength()) ||
                (s->getDate() < date && date < s->getDate() + s->getFilm()->getLength()));
        };
    try {
        if (seances->find(pred) != nullptr) throw std::logic_error("seance already exists or times overlap");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
	
    SeancePtr seance = std::make_shared<Seance>(date, seats, film);
    seances->add(seance);
    return seance;
}

// toString calling same name method in repository
std::string SeanceManager::toString() {
    return "SeanceManager::"+seances->toString()+";;";
}

// get the repository containing all seances as const, to protect from changing it outside of this class
const RepositoryPtr<SeancePtr,SeancePredicate> &SeanceManager::getSeances() const {
    return seances;
}

// destructor - smart pointers handle contained object's destruction
SeanceManager::~SeanceManager() = default;
