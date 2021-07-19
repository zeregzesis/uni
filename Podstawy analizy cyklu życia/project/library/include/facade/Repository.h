#ifndef CINEMA_REPOSITORY_H
#define CINEMA_REPOSITORY_H

#include "includeHeader.h"
#include "typedefs.h"

// generic class to serve as in-program storage for objects of given type
// allows object lookup based on given predicate

template <typename T, typename P>
class Repository {
private:
    friend class boost::serialization::access;
    template<class Archive>
    void serialize(Archive & ar, const unsigned int version)
    {
        ar & list;
    }
    std::list<T> list;
public:
    Repository();

    virtual ~Repository();

    const std::list<T> &getList() const;

    T get(int id);

    T find(P pred);

    std::list<T> findAll(P pred);

    void add(T ptr);

    void remove(T ptr);

    int size();

    std::string toString();
};

#endif //CINEMA_REPOSITORY_H
