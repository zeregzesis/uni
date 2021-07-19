#ifndef CINEMA_INCLUDEHEADER_H
#define CINEMA_INCLUDEHEADER_H

// include all libraries and use namespaces
// collected in one file to de-bloat other files

#include <iostream>
#include <boost/date_time.hpp>
#include <memory>
#include <list>
#include <string>
#include <map>
#include <random>
#include <functional>
#include <fstream>

#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/serialization/base_object.hpp>
#include <boost/serialization/shared_ptr.hpp>
#include <boost/serialization/export.hpp>
#include <boost/serialization/list.hpp>
#include <boost/date_time/gregorian/greg_serialize.hpp>
#include <boost/date_time/posix_time/time_serialize.hpp>
#include <stdexcept>

namespace pt = boost::posix_time;
namespace gr = boost::gregorian;

#endif //CINEMA_INCLUDEHEADER_H
