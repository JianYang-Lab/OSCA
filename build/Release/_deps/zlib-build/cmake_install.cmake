# Install script for directory: /Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/Library/Developer/CommandLineTools/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.1.3.1.dylib;/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.1.dylib")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib" TYPE SHARED_LIBRARY FILES
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/libz.1.3.1.dylib"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/libz.1.dylib"
    )
  foreach(file
      "$ENV{DESTDIR}/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.1.3.1.dylib"
      "$ENV{DESTDIR}/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.1.dylib"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/strip" -x "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.dylib")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib" TYPE SHARED_LIBRARY FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/libz.dylib")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.a")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib" TYPE STATIC_LIBRARY FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/libz.a")
  if(EXISTS "$ENV{DESTDIR}/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.a")
    execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/ranlib" "$ENV{DESTDIR}/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/lib/libz.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/include/zconf.h;/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/include/zlib.h")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/include" TYPE FILE FILES
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/zconf.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-src/zlib.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/share/man/man3/zlib.3")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/share/man/man3" TYPE FILE FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-src/zlib.3")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/share/pkgconfig/zlib.pc")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/installed/usr/share/pkgconfig" TYPE FILE FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/zlib-build/zlib.pc")
endif()

