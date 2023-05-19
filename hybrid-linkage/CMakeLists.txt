cmake_minimum_required(VERSION 2.8)
project(hybrid_linkage)

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-unused-function -O3 -march=broadwell")
set(CMAKE_CXX_STANDARD 20)

add_library(static STATIC static.cpp)
add_library(dynamic dynamic.cpp)

set(EXE main.cpp)

add_executable(hybrid_linkage ${EXE})

target_link_libraries(hybrid_linkage PRIVATE static dynamic)
