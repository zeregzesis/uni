#ifndef CINEMA_TYPEDEFS_H
#define CINEMA_TYPEDEFS_H

#include "includeHeader.h"

//pre-declatarion of core classes
class Client;
class Registered;
class Company;
class Ticket;
class Seance;
class Film;
class Address;

//pre-declatarion of repository classes
class ClientRepository;
class TicketRepository;
class SeanceRepository;
class FilmRepository;

template <typename T, typename P>
class Repository;

//pre-declatarion of manager classes
class ClientManager;
class TicketManager;
class SeanceManager;
class FilmManager;


//typedefs of core classes
typedef std::shared_ptr<Client> ClientPtr;
typedef std::shared_ptr<Seance> SeancePtr;
typedef std::shared_ptr<Ticket> TicketPtr;
typedef std::shared_ptr<Film> FilmPtr;
typedef std::shared_ptr<Address> AddressPtr;

//typedefs of repository classes
typedef std::shared_ptr<ClientRepository> ClientRepositoryPtr;
typedef std::shared_ptr<SeanceRepository> SeanceRepositoryPtr;
typedef std::shared_ptr<TicketRepository> TicketRepositoryPtr;
typedef std::shared_ptr<FilmRepository> FilmRepositoryPtr;

template <typename T, typename P>
using RepositoryPtr = std::shared_ptr<Repository<T,P>>;

//typedefs of manager classes
typedef std::shared_ptr<ClientManager> ClientManagerPtr;
typedef std::shared_ptr<SeanceManager> SeanceManagerPtr;
typedef std::shared_ptr<TicketManager> TicketManagerPtr;
typedef std::shared_ptr<FilmManager> FilmManagerPtr;

//typedefs of predicates used in repositories functions
typedef std::function<bool(ClientPtr)> ClientPredicate;
typedef std::function<bool(SeancePtr)> SeancePredicate;
typedef std::function<bool(TicketPtr)> TicketPredicate;
typedef std::function<bool(FilmPtr)> FilmPredicate;

#endif //CINEMA_TYPEDEFS_H
