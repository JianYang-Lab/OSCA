#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "GSL::gsl" for configuration "Release"
set_property(TARGET GSL::gsl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(GSL::gsl PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgsl.a"
  )

list(APPEND _cmake_import_check_targets GSL::gsl )
list(APPEND _cmake_import_check_files_for_GSL::gsl "${_IMPORT_PREFIX}/lib/libgsl.a" )

# Import target "GSL::gslcblas" for configuration "Release"
set_property(TARGET GSL::gslcblas APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(GSL::gslcblas PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgslcblas.a"
  )

list(APPEND _cmake_import_check_targets GSL::gslcblas )
list(APPEND _cmake_import_check_files_for_GSL::gslcblas "${_IMPORT_PREFIX}/lib/libgslcblas.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
