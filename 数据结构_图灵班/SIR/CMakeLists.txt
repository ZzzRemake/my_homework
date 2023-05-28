cmake_minimum_required(VERSION 3.23)
project(SIR)

set(CMAKE_CXX_STANDARD 17)

add_executable(SIR main.cpp SortNetwork_SIR.cpp SortNetwork_SIR.h)
