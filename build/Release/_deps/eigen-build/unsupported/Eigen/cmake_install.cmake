# Install script for directory: /Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen

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

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE FILE FILES
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/AdolcForward"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/AlignedVector3"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/ArpackSupport"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/AutoDiff"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/BVH"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/EulerAngles"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/FFT"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/IterativeSolvers"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/KroneckerProduct"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/LevenbergMarquardt"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/MatrixFunctions"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/MoreVectorization"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/MPRealSupport"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/NonLinearOptimization"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/NumericalDiff"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/OpenGLSupport"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/Polynomials"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/Skyline"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/SparseExtra"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/SpecialFunctions"
    "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/Splines"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Devel" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE DIRECTORY FILES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src/unsupported/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-build/unsupported/Eigen/CXX11/cmake_install.cmake")

endif()

