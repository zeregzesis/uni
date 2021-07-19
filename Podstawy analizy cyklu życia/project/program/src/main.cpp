#include <boost/smart_ptr/shared_ptr.hpp>
#include "typedefs.h"
#include "includeHeader.h"


#include "saveState.h"

int main(){

    //declaring all needed variables;
    char sign;
    ClientManagerPtr clientManager;
    FilmManagerPtr filmManager;
    SeanceManagerPtr seanceManager;
    TicketManagerPtr ticketManager;
    std::cout << "Restore configuration(if exists)? <t/n>: ";
    std::cin >> sign;

	//restoring (or not) previous state
    if(sign == 't'){
        RepositoryPtr<ClientPtr,ClientPredicate> cr = RestoreClientRepository();
        clientManager = std::make_shared<ClientManager>(cr);
        RepositoryPtr<FilmPtr,FilmPredicate> fr = RestoreFilmRepository();
        filmManager = std::make_shared<FilmManager>(fr);
        RepositoryPtr <SeancePtr,SeancePredicate> sr = RestoreSeanceRepository(fr);
        seanceManager = std::make_shared<SeanceManager>(sr);
        RepositoryPtr<TicketPtr,TicketPredicate> trReservation = RestoreTicketRepository(sr, cr,"reservation.txt");
        RepositoryPtr<TicketPtr,TicketPredicate> trPaid = RestoreTicketRepository(sr, cr,"paid.txt");
        ticketManager = std::make_shared<TicketManager>(trReservation,trPaid);
    }

    else if(sign != 'n'){
        std::cout<<"Incorrect sign, terminating program...";
        return 0;
    }

    else{
        clientManager = std::make_shared<ClientManager>();
        filmManager = std::make_shared<FilmManager>();
        seanceManager = std::make_shared<SeanceManager>();
        ticketManager = std::make_shared<TicketManager>();
    }


    
	//varables used in main program loop
    bool endFlag = false;
    char choice;
    std::string temp;

	//main program loop
    while(!endFlag){
		
		//list different option menu's
        std::cout << std::endl <<
            "[1] Client options\n"
            "[2] Film options\n"
            "[3] Seance options\n"
            "[4] Ticket options\n"
            "[5] Terminate program\n"
            "Choose: ";
        std::cin >> choice;
		
		//declaration of variables used in different cases described with first occurence

        //variables for registered client
        ClientType cType;
        std::string firstName, lastName, id;

        //variables for company client
        std::string name, nip, city, street, number;

        //variables for film
        pt::time_duration length;
        int year, month, day;
        std::string title;

        //variables for seance
        FilmPtr film;
        int seats, hour, minute;

        //variables for ticket
        TicketType tType;
        SeancePtr seance;
        ClientPtr client;
        TicketPtr ticket;

		//main switch, allows to choose object type and gives options available for it
        switch(choice){
            case '1':
				//list options for Client
                std::cout << "[1] Add registered client\n"
                             "[2] Add company client\n"
                             "[3] List all clients\n"
                             "[4] Delete client\n"
                             "Choose: ";
                std::cin >> choice;
				
				//Client switch, handles options for clients
                switch(choice){
					
					//adding client of subtype Registered
                    case '1':
					
						//get all needed data from user
                        std::cout << "Client type: ";
                        std::cin >> temp;
                        EnumString<ClientType>::To( cType, temp );

                        std::cout << "First name: ";
                        std::cin >> firstName;

                        std::cout << "Last name: ";
                        std::cin >> lastName;

                        std::cout << "ID: ";
                        std::cin >> id;

						//forward object creation to manager
                        clientManager->createRegistered(cType, firstName, lastName, id);

                        break;
						
					//adding client of subtype Company
                    case '2':
					
						//get all needed data from user
                        std::cout << "Client type: ";
                        std::cin >> temp;
                        EnumString<ClientType>::To( cType, temp );

                        std::cout << "Name: ";
                        std::cin >> name;

                        std::cout << "NIP: ";
                        std::cin >> nip;

                        std::cout << "City: ";
                        std::cin >> city;

                        std::cout << "Street: ";
                        std::cin >> street;

                        std::cout << "Number: ";
                        std::cin >> number;

						//forward object creation to manager
                        clientManager->createCompany(cType, name, nip, std::make_shared<Address>(city, street, number));

                        break;
						
					//list all clients
                    case '3':
                        for (ClientPtr c : clientManager->getClients()->getList()){
                            std::cout << c->toString() << std::endl;
                        }
                        break;
						
					//delete client by ID
                    case '4':
                        std::cout << "Client ID: ";
                        std::cin >> id;
                        client = clientManager->getClients()->get(std::stoi(id));
                        clientManager->getClients()->remove(client);
                        break;
						
					//handle unexpected input
                    default:
                        std::cout << "Wrong option!" << std::endl;
                        break;
                }
                break;
            case '2':
				//list options for Film
                std::cout << "[1] Add film\n"
                             "[2] List all films\n"
                             "[3] Delete film\n"
                             "Choose: ";
                std::cin >> choice;

				//Film switch, handles options for films
                switch(choice) {
                    case '1':
					
						//get all needed data from user
                        std::cout << "Length: ";
                        std::cin >> temp;
                        length = pt::minutes(std::stoi(temp));

                        std::cout << "Title: ";
                        std::cin >> title;

                        std::cout << "Premiere year: ";
                        std::cin >> temp;
                        year = std::stoi(temp);

                        std::cout << "Premiere month: ";
                        std::cin >> temp;
                        month = std::stoi(temp);

                        std::cout << "Premiere day: ";
                        std::cin >> temp;
                        day = std::stoi(temp);

						//forward object creation to manager
                        filmManager->createFilm(length, title, pt::ptime(gr::date(year,month,day)));

                        break;
						
					//list all films
                    case '2':
                        for (FilmPtr f : filmManager->getFilms()->getList()){
                            std::cout << f->toString() << std::endl;
                        }
                        break;
						
					//delete film by ID
                    case '3':
                        std::cout << "Film ID: ";
                        std::cin >> id;
                        film = filmManager->getFilms()->get(std::stoi(id));
                        filmManager->getFilms()->remove(film);
                        break;
						
					//handle unexpected input
                    default:
                        std::cout << "Wrong option!" << std::endl;
                        break;
                }
                break;
            case '3':
				//list options for Seance
                std::cout << "[1] Add seance\n"
                             "[2] List all seances\n"
                             "[3] Delete seance\n"
                             "Choose: ";
                std::cin >> choice;

				//Seance switch, handles options for seances
                switch(choice) {
                    case '1':
					
						//get all needed data from user
                        std::cout << "Number of seats: ";
                        std::cin >> temp;
                        seats = std::stoi(temp);

                        std::cout << "Film ID: ";
                        std::cin >> id;
                        film = filmManager->getFilms()->get(std::stoi(id));

                        std::cout << "Seance year: ";
                        std::cin >> temp;
                        year = std::stoi(temp);

                        std::cout << "Seance month: ";
                        std::cin >> temp;
                        month = std::stoi(temp);

                        std::cout << "Seance day: ";
                        std::cin >> temp;
                        day = std::stoi(temp);

                        std::cout << "Seance hour: ";
                        std::cin >> temp;
                        hour = std::stoi(temp);

                        std::cout << "Seance minute: ";
                        std::cin >> temp;
                        minute = std::stoi(temp);

						//forward object creation to manager
                        seanceManager->createSeance(pt::ptime(gr::date(year,month,day)) + pt::hours(hour) + pt::minutes(minute), seats, film);

                        break;
						
					//list all seances
                    case '2':
                        for (SeancePtr s : seanceManager->getSeances()->getList()){
                            std::cout << s->toString() << std::endl;
                        }
                        break;,
					
					//delete seance by ID
                    case '3':
                        std::cout << "Seance ID: ";
                        std::cin >> id;
                        seance = seanceManager->getSeances()->get(std::stoi(id));
                        seanceManager->getSeances()->remove(seance);
                        break;
						
					//handle unexpected input
                    default:
                        std::cout << "Wrong option!" << std::endl;
                        break;
                }

                break;
            case '4':
				//list options for Ticket(no delete of paid tickets is a design choice)
                std::cout << "[1] Create reservation(unpaid ticket)\n"
                             "[2] Mark existing ticket as paid\n"
                             "[3] Cancel reservation\n"
                             "[4] List all reservations\n"
                             "[5] List all paid tickets\n"
                             "Choose: ";
                std::cin >> choice;

				//Ticket switch, handles options for tickets
                switch(choice) {
                    case '1':
					
						//get all needed data from user
                        std::cout << "Number of seats: ";
                        std::cin >> temp;
                        seats = std::stoi(temp);

                        std::cout << "Ticket type: ";
                        std::cin >> temp;
                        EnumString<TicketType>::To( tType, temp );

                        std::cout << "Seance ID: ";
                        std::cin >> id;
                        seance = seanceManager->getSeances()->get(std::stoi(id));

                        std::cout << "Client ID: ";
                        std::cin >> id;
                        client = clientManager->getClients()->get(std::stoi(id));

						//forward object creation to manager
                        ticketManager->createTicket(seats, tType, seance, client);

                        break;
						
					//change ticket status(by ID) from unpaid to paid
                    case '2':
                        std::cout << "Ticket ID: ";
                        std::cin >> id;
                        ticket = ticketManager->getReservation()->get(std::stoi(id));
                        ticketManager->pay(ticket);
                        break;
						
					//delete unpaid ticket by ID(synonymous to canceling reservation)
                    case '3':
                        std::cout << "Ticket ID: ";
                        std::cin >> id;
                        ticket = ticketManager->getReservation()->get(std::stoi(id));
                        ticketManager->cancel(ticket);
                        break;
						
					//list all unpaid tickets
                    case '4':
                        for (TicketPtr t : ticketManager->getReservation()->getList()){
                            std::cout << t->toString() << std::endl;
                        }
                        break;
						
					//list all paid tickets
                    case '5':
                        for (TicketPtr t : ticketManager->getPaid()->getList()){
                            std::cout << t->toString() << std::endl;
                        }
                        break;
						
					//handle unexpected input
                    default:
                        std::cout << "Wrong option!" << std::endl;
                        break;
                }
                break;
				
			//allow for program termination
            case '5':
                endFlag = true;
                break;
				
			//handle unexpected input
            default:
                std::cout << "Wrong option!" << std::endl;
                break;
        }
    }

    //saving state at termination
    saveAppState(filmManager->getFilms(),clientManager->getClients(),seanceManager->getSeances(),ticketManager->getReservation(),ticketManager->getPaid());
	
    return 0;
}