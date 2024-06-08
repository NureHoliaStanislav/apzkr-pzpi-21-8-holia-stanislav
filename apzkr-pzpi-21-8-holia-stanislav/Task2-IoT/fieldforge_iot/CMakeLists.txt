cmake_minimum_required(VERSION 3.10)

# set the project name
project(FieldForge)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# set the cpr_DIR variable
set(CPR_DIR "${CMAKE_CURRENT_SOURCE_DIR}/cpr")

# add the executable
add_executable(FieldForge main.cpp)

set(CMAKE_PREFIX_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cpr)

find_package(CPR CONFIG REQUIRED)
target_link_libraries(FieldForge PRIVATE cpr)
