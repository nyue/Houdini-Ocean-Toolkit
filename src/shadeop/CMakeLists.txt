
set( CMAKE_CONFIGURATION_TYPES "Release" CACHE STRING "" FORCE )
set( CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE )
cmake_minimum_required( VERSION 2.6 )
project( ocean )

find_package( 3Delight )

add_definitions( -D_Windows )

include_directories( 3rdparty/include )
include_directories( 3rdparty/include/loki )
include_directories( 3rdparty/include/loki/flex )
include_directories( 3rdparty/include/loki/yasli )
include_directories( 3rdparty/win32 )
include_directories( ${3Delight_INCLUDE_DIR} )

add_library( ocean SHARED RSL_ocean.cpp )

target_link_libraries( ocean ${3Delight_LIBRARY} )
target_link_libraries( ocean 3rdparty/win32/blitz )
target_link_libraries( ocean 3rdparty/win32/libfftw3f-3 )



