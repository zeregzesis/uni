#ifndef CINEMA_TICKET_H
#define CINEMA_TICKET_H

#include "typedefs.h"
#include "includeHeader.h"
#include "utils/EnumString.h"

// issued ticket
// can be paid for or only reserved, handeled by manager class

// all ticket types, as per cinema policy
enum TicketType{
    Normal,
    Group,
    Family
};
Begin_Enum_String( TicketType )
    {
        Enum_String( Normal );
        Enum_String( Group );
        Enum_String( Family );
    }
End_Enum_String;

class Ticket {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version)
    {
        ar & seats;
        ar & price;
        ar & ticketType;
        ar & seance;
        ar & client;
    }
    int seats;
    int price;
    TicketType ticketType;
    SeancePtr seance;
    ClientPtr client;
    std::map<TicketType,std::string> ticketTypeMap = {{Normal,"Normal"},{Group,"Group"},{Family,"Family"}};
public:
    Ticket(int seats, int price, TicketType ticketType, const SeancePtr &seance, const ClientPtr &client);

    Ticket();

    int getSeats() const;

    int getPrice() const;

    TicketType getTicketType() const;

    const SeancePtr &getSeance() const;

    const ClientPtr &getClient() const;

    std::string toString();

    void setSeance(const SeancePtr &newSeance);

    void setClient(const ClientPtr &newClient);

    virtual ~Ticket();
};


#endif //CINEMA_TICKET_H
