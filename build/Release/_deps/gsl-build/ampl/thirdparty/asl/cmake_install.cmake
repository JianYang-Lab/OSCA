# Install script for directory: /Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl

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

if(CMAKE_INSTALL_COMPONENT STREQUAL "asl" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/asl" TYPE FILE FILES
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/arith.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/asl.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/asl_pfg.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/asl_pfgh.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/avltree.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/errchk.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/funcadd.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/getstub.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/jac2dim.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/jacpdim.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/nlp.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/nlp2.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/obj_adj.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/psinfo.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/opcode.hd"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers/r_opn.hd"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/stdio1.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/arith.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "asl" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/asl2" TYPE FILE FILES
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/arith.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/asl.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/asl_pfg.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/asl_pfgh.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/avltree.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/errchk.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/funcadd.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/getstub.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/jac2dim.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/jacpdim.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/nlp.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/nlp2.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/obj_adj.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/opno2.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/psinfo.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/opcode.hd"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/thirdparty/asl/src/solvers2/r_opn.hd"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/stdio1.h"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/include/arith.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "asl" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/lib/libasl.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl.a")
    execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "asl" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/lib/libasl2.a")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl2.a" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl2.a")
    execute_process(COMMAND "/Library/Developer/CommandLineTools/usr/bin/ranlib" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libasl2.a")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/ampl-asl/ampl-asl-config.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/ampl-asl/ampl-asl-config.cmake"
         "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-build/ampl/thirdparty/asl/CMakeFiles/Export/cb0b1575a9af004344f59d6939d3b021/ampl-asl-config.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/ampl-asl/ampl-asl-config-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/ampl-asl/ampl-asl-config.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ampl-asl" TYPE FILE FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-build/ampl/thirdparty/asl/CMakeFiles/Export/cb0b1575a9af004344f59d6939d3b021/ampl-asl-config.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ampl-asl" TYPE FILE FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-build/ampl/thirdparty/asl/CMakeFiles/Export/cb0b1575a9af004344f59d6939d3b021/ampl-asl-config-release.cmake")
  endif()
endif()

