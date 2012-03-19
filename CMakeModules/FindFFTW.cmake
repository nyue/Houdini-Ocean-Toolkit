# - Find the native FFTW includes and library
#
# This module defines
#
#  FFTW_INCLUDE_DIR, where to find png.h, etc.
#  FFTW_LIBRARY, the libraries to link against to use FFTW.
#
#  FFTW_FOUND

find_path(FFTW_INCLUDE_DIR fftw3.h
          PATHS ${CMAKE_SOURCE_DIR}/../3rdparty/include;
                ${CMAKE_SOURCE_DIR}/3rdparty/include)

find_library(FFTW_LIBRARY fftw3f
             PATHS ${CMAKE_SOURCE_DIR}/../3rdparty/lib;
                   ${CMAKE_SOURCE_DIR}/3rdparty/lib)

if (FFTW_INCLUDE_DIR AND FFTW_LIBRARY)
   set(FFTW_FOUND TRUE)
else (FFTW_INCLUDE_DIR AND FFTW_LIBRARY)
   set(FFTW_FOUND FALSE)
endif (FFTW_INCLUDE_DIR AND FFTW_LIBRARY)
    
