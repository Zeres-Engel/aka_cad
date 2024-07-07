cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_VERBOSE_MAKEFILE ON)

project(aka_cad)

find_package(Boost REQUIRED)

if(NOT Boost_FOUND)
    message(STATUS "This project requires the Boost library, and will not be compiled.")
    return()
endif()

add_subdirectory(lib/pybind11)
add_subdirectory(lib/libnest2d)

pybind11_add_module(aka_cad src/main.cpp)
target_link_libraries(aka_cad PUBLIC libnest2d)
