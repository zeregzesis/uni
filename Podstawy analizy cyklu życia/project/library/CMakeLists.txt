cmake_minimum_required(VERSION 3.4)
project(Library)

set(SOURCE_FILES
        src/model/Client.cpp
        src/model/Registered.cpp
        src/model/Company.cpp
        src/model/Address.cpp
        src/model/Seance.cpp
        src/model/Film.cpp
        src/model/Ticket.cpp
        src/facade/Repository.cpp
        src/managers/FilmManager.cpp
        src/managers/ClientManager.cpp
        src/managers/SeanceManager.cpp
        src/managers/TicketManager.cpp include/saveState/saveState.h)

add_library(Library ${SOURCE_FILES})

target_include_directories(Library PUBLIC include)

enable_testing()

find_package (Boost 1.67.0 COMPONENTS unit_test_framework serialization date_time REQUIRED)

target_link_libraries(Library ${Boost_LIBRARIES})

include_directories(
        ${CMAKE_CURRENT_SOURCE_DIR}/include/model
        ${CMAKE_CURRENT_SOURCE_DIR}/include/managers
        ${CMAKE_CURRENT_SOURCE_DIR}/include/facade
        ${CMAKE_CURRENT_SOURCE_DIR}/include/utils
        ${CMAKE_CURRENT_SOURCE_DIR}/include/saveState
        ${Boost_INCLUDE_DIRS}
)

set(SOURCE_TEST_FILES
        test/master.cpp
        test/ClientTest.cpp
        test/RegisteredTest.cpp
        test/CompanyTest.cpp
        test/FilmTest.cpp
        test/SeanceTest.cpp
        test/SeanceManagerTest.cpp
        test/TicketTest.cpp
        test/RepositoryTest.cpp
        test/TicketManagerTest.cpp
        test/FilmManagerTest.cpp
        test/ClientManagerTest.cpp)

add_executable (LibraryTest ${SOURCE_TEST_FILES})

target_link_libraries (LibraryTest
        Library
        ${Boost_UNIT_TEST_FRAMEWORK_LIBRARY}
        )

add_test(LibraryTest1 LibraryTest
        --report_level=detailed
        --log_level=all
        --color_output=yes
        )

add_custom_target(check ${CMAKE_COMMAND} -E env CTEST_OUTPUT_ON_FAILURE=1 BOOST_TEST_LOG_LEVEL=all
        ${CMAKE_CTEST_COMMAND} -C $<CONFIGURATION> --verbose
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR})