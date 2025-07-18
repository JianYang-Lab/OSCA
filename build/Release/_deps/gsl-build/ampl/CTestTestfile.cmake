# CMake generated Testfile for 
# Source directory: /Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl
# Build directory: /Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-build/ampl
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(amplgsl-test "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-build/bin/amplgsl-test")
set_tests_properties(amplgsl-test PROPERTIES  _BACKTRACE_TRIPLES "/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/CMakeLists.txt;58;add_test;/Users/houjunren/Desktop/OSCA_cis-trans/build/Release/_deps/gsl-src/ampl/CMakeLists.txt;0;")
subdirs("thirdparty/asl")
subdirs("thirdparty/test-support")
