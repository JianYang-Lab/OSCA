#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "asl" for configuration "Release"
set_property(TARGET asl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(asl PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "m"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libasl.a"
  )

list(APPEND _cmake_import_check_targets asl )
list(APPEND _cmake_import_check_files_for_asl "${_IMPORT_PREFIX}/lib/libasl.a" )

# Import target "asl2" for configuration "Release"
set_property(TARGET asl2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(asl2 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "m"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libasl2.a"
  )

list(APPEND _cmake_import_check_targets asl2 )
list(APPEND _cmake_import_check_files_for_asl2 "${_IMPORT_PREFIX}/lib/libasl2.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
