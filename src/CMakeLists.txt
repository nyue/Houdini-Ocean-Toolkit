#
# This cmake script will build a basic Houdini DSO.
#
if (HDK_FOUND)
    add_definitions(${HDK_DEFINITIONS})
    include_directories(${HDK_INCLUDE_DIRS})
    link_directories(${HDK_LIBRARY_DIRS})
endif (HDK_FOUND)

# this command calls hdk-config.py to build a special file that will be the repository of the taginfo
#add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/sesitag.C
#                   DEPENDS ${SOP_Star_SRCS}
#                   COMMAND hdk-config.py --tagfile=${CMAKE_BINARY_DIR}/sesitag.C)
GenerateSESITagSourceFile( ${CMAKE_BINARY_DIR}/sesitag.C )

# find blitz
find_package(Blitz)
if (BLITZ_FOUND)
    include_directories(${BLITZ_INCLUDE_DIR})
    link_libraries(${BLITZ_LIBRARY})
else (BLITZ_FOUND)
    message(FATAL_ERROR "BLITZ NOT FOUND")
endif (BLITZ_FOUND)
# find fftw
find_package(FFTW)
if (FFTW_FOUND)
    include_directories(${FFTW_INCLUDE_DIR})
    link_libraries(${FFTW_LIBRARY})
else (FFTW_FOUND)
    message(FATAL_ERROR "FFTW NOT FOUND")
endif (FFTW_FOUND)

include_directories("3rdparty/include")

# SOP_Cleave
set(SOP_Cleave_SRCS SOP_Cleave.C)
add_library(SOP_Cleave SHARED ${SOP_Cleave_SRCS} ${CMAKE_BINARY_DIR}/sesitag.C)
target_link_libraries(SOP_Cleave ${HDK_LIBRARIES})
set_target_properties(SOP_Cleave PROPERTIES PREFIX "")
install(TARGETS SOP_Cleave DESTINATION dso)
install(FILES SOP_Cleave.icon DESTINATION config/Icons)

# SOP_Ocean
set(SOP_Ocean_SRCS SOP_Ocean.C)
add_library(SOP_Ocean SHARED ${SOP_Ocean_SRCS} ${CMAKE_BINARY_DIR}/sesitag.C)
target_link_libraries(SOP_Ocean ${HDK_LIBRARIES} )
set_target_properties(SOP_Ocean PROPERTIES PREFIX "")
install(TARGETS SOP_Ocean DESTINATION dso)
install(FILES SOP_Ocean.png DESTINATION config/Icons)

# VEX_Ocean
set(VEX_Ocean_SRCS VEX_Ocean.C)
add_library(VEX_Ocean SHARED ${VEX_Ocean_SRCS} ${CMAKE_BINARY_DIR}/sesitag.C)
target_link_libraries(VEX_Ocean ${HDK_LIBRARIES} )
set_target_properties(VEX_Ocean PROPERTIES PREFIX "")
install(TARGETS VEX_Ocean DESTINATION dso)
