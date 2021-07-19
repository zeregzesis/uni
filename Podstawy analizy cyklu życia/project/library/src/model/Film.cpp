#include "Film.h"

// constructor - nothing to initialize
Film::Film() = default;

// constructor - initialize all fields while calling base class constructor
Film::Film(const pt::time_duration &length, const std::string &title, const pt::ptime &premiere) : length(length), title(title), premiere(premiere) {}

// begin - simple getters and setters
const pt::time_duration &Film::getLength() const {
    return length;
}

const std::string &Film::getTitle() const {
    return title;
}

const pt::ptime &Film::getPremiere() const {
    return premiere;
}
// end - simple getters and setters

// output object as string
std::string Film::toString() {
    return "Film::length:"+std::to_string(length.hours())+","+std::to_string(length.minutes())+";title:"+title+";premiere:"+pt::to_simple_string(premiere)+";;";
}

// destructor - nothing inside to destroy alongside this
Film::~Film() = default;
