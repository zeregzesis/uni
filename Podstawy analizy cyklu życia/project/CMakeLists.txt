cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_C_FLAGS_DEBUG "-g3 -gdwarf-4")
set(CMAKE_CXX_FLAGS_DEBUG "-g3 -gdwarf-4")
enable_language(CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_VERBOSE_MAKEFILE TRUE)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wpedantic -Wno-unused-parameter -Wextra  -fconcepts")

project(Cinema)

add_subdirectory(library)
add_subdirectory(program)


include_directories(
        library/include/model
        library/include/facade
        library/include/utils
        program/include
        library/include/managers
        library/include/saveState)

add_executable(Cinema
        program/src/main.cpp)

target_link_libraries(Cinema Library)

enable_testing()