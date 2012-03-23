#
# Root CMakeLists.txt to build all the HVT tools
# 
cmake_minimum_required(VERSION 2.6)

if (WIN32)
  cmake_policy(SET CMP0008 NEW)
endif (WIN32)

project(hot)

# run our helper process to grab the compile and link flags from hcustom

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/CMakeModules" )
# execute_process(COMMAND hdk-config.py --notag --cmake=${PROJECT_SOURCE_DIR}/CMakeModules/FindHDK.cmake)

find_package(HDK)

if (HDK_FOUND)

  # set(CMAKE_INSTALL_PREFIX ${HDK_HIH_DIR})
  
  # the 3rdparty libraries that I use can usually be found here ...
  #set (CMAKE_FIND_ROOT_PATH  ${PROJECT_SOURCE_DIR}/../3rdparty)
  
  
  add_subdirectory(src)
  
  #
  # packaging setup
  #
  INCLUDE(InstallRequiredSystemLibraries)
  SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "The Houdini Ocean Toolkit")
  SET(CPACK_PACKAGE_VENDOR "Drew.Whitehouse@anu.edu.au")
  SET(CPACK_PACKAGE_VERSION_MAJOR "1")
  SET(CPACK_PACKAGE_VERSION_MINOR "0")
  SET(CPACK_PACKAGE_VERSION_PATCH "rc7")
  
  IF(WIN32 AND NOT UNIX)
	SET(CPACK_GENERATOR "ZIP")
  ELSE(WIN32 AND NOT UNIX)
	SET(CPACK_SYSTEM_NAME "h$ENV{HOUDINI_VERSION}")
	#  SET(CPACK_SYSTEM_NAME "H$ENV{HOUDINI_VERSION}-gcc-$ENV{HOUDINI_BUILD_COMPILER}-$ENV{HOUDINI_BUILD_KERNEL}")
	SET(CPACK_GENERATOR "TGZ")
  ENDIF(WIN32 AND NOT UNIX)
  
  include(CPack)
  
endif ( HDK_FOUND )
