# - Find the native BLITZ includes and library
#
# This module defines
#
#  BLITZ_INCLUDE_DIR, where to find png.h, etc.
#  BLITZ_LIBRARY, the libraries to link against to use BLITZ.
#
#  BLITZ_FOUND

find_path(BLITZ_INCLUDE_DIR blitz/array.h
          PATHS ${CMAKE_SOURCE_DIR}/../3rdparty/include;
                ${CMAKE_SOURCE_DIR}/3rdparty/include)

find_library(BLITZ_LIBRARY blitz
             PATHS ${CMAKE_SOURCE_DIR}/../3rdparty/lib;
                   ${CMAKE_SOURCE_DIR}/3rdparty/lib)

if (BLITZ_INCLUDE_DIR AND BLITZ_LIBRARY)
   set(BLITZ_FOUND TRUE)
else (BLITZ_INCLUDE_DIR AND BLITZ_LIBRARY)
   set(BLITZ_FOUND FALSE)
endif (BLITZ_INCLUDE_DIR AND BLITZ_LIBRARY)
    
