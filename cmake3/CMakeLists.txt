cmake_minimum_required(VERSION 2.8)
project(whymisslink)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-unused-function -march=broadwell -std=c++17")

add_library(aaa OBJECT aaa.cpp)
# add_library(aaa SHARED aaa.cpp)

add_library(bbb SHARED bbb.cpp)
target_link_libraries(bbb PUBLIC aaa)
