# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-src"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-build"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/tmp"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/src"
  "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/eigen-subbuild/eigen-populate-prefix/src/eigen-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
