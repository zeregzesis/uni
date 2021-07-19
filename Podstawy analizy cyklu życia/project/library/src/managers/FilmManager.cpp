#include "FilmManager.h"

// constructor - nothing to initialize
FilmManager::FilmManager() = default;

// constructor - if repository was created before we can initialize manager with it
FilmManager::FilmManager(const RepositoryPtr<FilmPtr, FilmPredicate> &films) : films(films) {}

// create new Film object and add it to repository
FilmPtr FilmManager::createFilm(pt::time_duration length, std::string title, pt::ptime premiere) {

	// protection against duplicate entriers
    FilmPredicate find1= [title](FilmPtr f2){return f2->getTitle()==title;};
    try {
        if (films->find(find1) != nullptr) throw std::logic_error("Film already exists");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
	
    FilmPtr f1= std::make_shared<Film>(length,title,premiere);
    films->add(f1);
    return f1;
}

// get the repository containing all films as const, to protect from changing it outside of this class
const RepositoryPtr<FilmPtr,FilmPredicate> &FilmManager::getFilms() const {
    return films;
}

// toString calling same name method in repository
std::string FilmManager::toString() {
    return "FilmManager::"+films->toString()+";;";
}

// destructor - smart pointers handle contained object's destruction
FilmManager::~FilmManager() = default;
