
// outside-of-class collection of methods to handle saving and loading app state when exiting / turning on the system

#ifndef CINEMA_SAVESTATE_H
#define CINEMA_SAVESTATE_H

#include "typedefs.h"
#include "Registered.h"
#include "Company.h"
#include "Seance.h"
#include "Film.h"
#include "Ticket.h"
#include "Repository.h"
#include "TicketManager.h"
#include "ClientManager.h"
#include "FilmManager.h"
#include "SeanceManager.h"

BOOST_CLASS_EXPORT(Registered)
BOOST_CLASS_EXPORT(Company)

// serialize and save all objects to files
void saveAppState
        (RepositoryPtr<FilmPtr ,FilmPredicate> fr,
         RepositoryPtr<ClientPtr ,ClientPredicate> cr,
         RepositoryPtr<SeancePtr ,SeancePredicate> sr,
         RepositoryPtr<TicketPtr,TicketPredicate> trReservation,
         RepositoryPtr<TicketPtr,TicketPredicate> trPaid
        ){
    std::ofstream out("films.txt");
    boost::archive::text_oarchive outArchive(out);
    outArchive<<fr;
    out.close();
    out.open("clients.txt");
    outArchive<<cr;
    out.close();
    out.open("seances.txt");
    outArchive<<sr;
    out.close();
    out.open("reservations.txt");
    outArchive<<trReservation;
    out.close();
    out.open("paid.txt");
    outArchive<<trPaid;
    out.close();
}

// begin - collection of methods to restore given objects, divied by object class
RepositoryPtr<FilmPtr ,FilmPredicate> RestoreFilmRepository() {

    RepositoryPtr<FilmPtr ,FilmPredicate> fr;
    std::ifstream in("films.txt");
    boost::archive::text_iarchive inArchive(in);
    inArchive>>fr;
    return fr;
}

RepositoryPtr<ClientPtr ,ClientPredicate> RestoreClientRepository() {

    RepositoryPtr<ClientPtr ,ClientPredicate> cr;
    std::ifstream in("clients.txt");
    boost::archive::text_iarchive inArchive(in);
    inArchive>>cr;
    return cr;
}

RepositoryPtr<SeancePtr ,SeancePredicate> RestoreSeanceRepository(RepositoryPtr<FilmPtr ,FilmPredicate> fr) {

    RepositoryPtr<SeancePtr ,SeancePredicate> sr;
    std::ifstream in("seances.txt");
    boost::archive::text_iarchive inArchive(in);
    inArchive>>sr;
    for(FilmPtr f : fr->getList()){
        for(SeancePtr s : sr->getList()){
            if(s->getFilm()->getTitle() == f->getTitle()) s->setFilm(f);
        }
    }
    return sr;
}

RepositoryPtr<TicketPtr ,TicketPredicate> RestoreTicketRepository(RepositoryPtr<SeancePtr ,SeancePredicate> sr, RepositoryPtr<ClientPtr ,ClientPredicate> cr, std::string file){
    RepositoryPtr<TicketPtr ,TicketPredicate> tr;
    std::ifstream in(file);
    boost::archive::text_iarchive inArchive(in);
    inArchive>>tr;
    for(SeancePtr s : sr->getList()){
        for(TicketPtr t : tr->getList()){
            if(t->getSeance()->getDate() == s->getDate()) t->setSeance(s);
        }
    }
	
	// handle child classes of Client, as when saved no information of subtype is preserved
    for(ClientPtr c : cr->getList()){
        for(TicketPtr t : tr->getList()){
            if(typeid(*c) == typeid(*(t->getClient())) && typeid(*c) == typeid(Company)){
                if(std::dynamic_pointer_cast<Company>(c)->getNip() == std::dynamic_pointer_cast<Company>(t->getClient())->getNip()){
                    t->setClient(c);
                }
            }
            else if(typeid(*c) == typeid(*(t->getClient())) && typeid(*c) == typeid(Registered)){
                if(std::dynamic_pointer_cast<Registered>(c)->getId() == std::dynamic_pointer_cast<Registered>(t->getClient())->getId()){
                    t->setClient(c);
                }
            }
        }
    }
    return tr;
}
// end - collection of methods to restore given objects, divied by object class

#endif //CINEMA_SAVESTATE_H
