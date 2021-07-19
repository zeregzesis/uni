#include "Repository.h"
#include "Client.h"
#include "Film.h"
#include "Seance.h"
#include "Ticket.h"

// list all used templates
template class Repository<ClientPtr, ClientPredicate>;
template class Repository<FilmPtr, FilmPredicate>;
template class Repository<SeancePtr, SeancePredicate>;
template class Repository<TicketPtr, TicketPredicate>;

// constructor - nothing to initialize
template <typename T, typename P>
Repository<T,P>::Repository() = default;

// destructor - smart pointers handle contained object's destruction
template <typename T, typename P>
Repository<T,P>::~Repository() = default;

// getter for entire list
template<typename T, typename P>
const std::list<T> &Repository<T, P>::getList() const {
    return list;
}

// getter by position in list(id)
template <typename T, typename P>
T Repository<T,P>::get(int id) {
    try {
        //exceptions!!
        if (size() < id) throw std::logic_error("id is out of range");
    }
    catch(std::logic_error &e){
        std::cout<<e.what();
    }
        std::_List_const_iterator<T> q = list.begin();
        std::advance(q, id);
        return *q;


}

// find first object that meets criteria specified by predicate function passed to it
template <typename T, typename P>
T Repository<T,P>::find(P pred) {
    for(auto &obj : list){
        if(pred(obj)) return obj;
    }

    return nullptr;
}

// same as find, but returns all ocurences in the list
template <typename T, typename P>
std::list<T> Repository<T,P>::findAll(P pred) {
    std::list<T> results;
    for(auto &obj : list){
        if(pred(obj)) results.push_back(obj);
    }
    return results;
}

// add object to the list
template <typename T, typename P>
void Repository<T,P>::add(T obj) {
    list.push_back(obj);
}

//remove object from the list(ending it's life unless you hold a reference to it somwhere)
template <typename T, typename P>
void Repository<T,P>::remove(T obj) {
    list.erase(std::find(list.begin(),list.end(),obj));
}

// get number of elements in list(list size)
template <typename T, typename P>
int Repository<T,P>::size() {
    return list.size();
}

// recursive toString listing all contained objects as one string
template <typename T, typename P>
std::string Repository<T,P>::toString(){
    std::string result="Repository::";
    for(T ptr:list){
        result+= ptr->toString();
    }
    return result+";;";
}