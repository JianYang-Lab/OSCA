cmake_minimum_required(VERSION 3.16)

project(osca LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_STATIC "Build static libraries" OFF)
set(CUSTOM_INCLUDE_SEARCH_PATH "" CACHE PATH "Additional include search path")
set(CUSTOM_LIB_SEARCH_PATH "" CACHE PATH "Additional library search path")

message(STATUS "CPU_ARCH: ${CMAKE_HOST_SYSTEM_PROCESSOR}")

# Detect OS
if (UNIX AND NOT APPLE)
    set(OS_NAME "Linux")
elseif(APPLE)
    set(OS_NAME "MacOS")
elseif(WIN32)
    set(OS_NAME "Windows")
else()
    message(FATAL_ERROR "Unsupported OS")
endif()
message(STATUS "Operating System: ${OS_NAME}")

# Compiler version checks
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    message(STATUS "Compiler: GCC ${CMAKE_CXX_COMPILER_VERSION}")
    if(NOT (CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 6.1))
        message(FATAL_ERROR "GCC >= 6.1 required")
    endif()
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(STATUS "Compiler: Clang ${CMAKE_CXX_COMPILER_VERSION}")
    if(NOT (CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 8.0))
        message(FATAL_ERROR "Clang >= 8.0 required")
    endif()
else()
    message(FATAL_ERROR "Unsupported compiler: only GCC or Clang supported")
endif()

# Download CPM for dependency management
if(NOT EXISTS "${CMAKE_BINARY_DIR}/cmake/CPM.cmake")
    message(STATUS "Downloading CPM.cmake...")
    file(DOWNLOAD
        https://github.com/cpm-cmake/CPM.cmake/releases/latest/download/CPM.cmake
        "${CMAKE_BINARY_DIR}/cmake/CPM.cmake"
        TLS_VERIFY ON)
endif()
include("${CMAKE_BINARY_DIR}/cmake/CPM.cmake")

# Dependencies
CPMAddPackage("gh:madler/zlib@1.3.1")
CPMAddPackage("gh:eigen-mirror/eigen#3.4.0")
CPMAddPackage(
  NAME gsl
  GITHUB_REPOSITORY ampl/gsl
  GIT_TAG v2.7.0
)

find_package(Threads REQUIRED)

# Find OpenMP
if(APPLE)
    # Use manual flags for OpenMP with Apple Clang
    set(OpenMP_C_FLAGS "-Xpreprocessor -fopenmp")
    set(OpenMP_C_LIB_NAMES "omp")
    set(OpenMP_C_INCLUDE_DIR "/opt/homebrew/opt/libomp/include")
    set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp")
    set(OpenMP_CXX_LIB_NAMES "omp")
    set(OpenMP_CXX_INCLUDE_DIR "/opt/homebrew/opt/libomp/include")
    set(OpenMP_omp_LIBRARY "/opt/homebrew/opt/libomp/lib/libomp.dylib")
endif()

if(LINUX)
    if(NOT OMP_LIBRARY)
        set(OMP_LIBRARY "/usr/lib64/libgomp.so.1")
    endif()
    if(NOT MKL_DIR)
        set(MKL_DIR "/soft/compiler/intel/oneapi-2022.2/mkl/2022.1.0/lib/cmake/mkl")
    endif()
    set(MKL_INTERFACE "lp64")
    set(MKL_THREADING "gnu_thread")
    set(MKL_ROOT "/soft/compiler/intel/oneapi-2022.2/mkl/2022.1.0")
    set(MKL_INCLUDE_DIR "${MKL_ROOT}/include")
    find_package(MKL REQUIRED)
endif()

if(WIN32)
    set(OpenMP_omp_LIBRARY "${LLVM_ROOT}/lib/libomp.lib")
    set(OpenMP_C_FLAGS "-fopenmp") 
    set(OpenMP_C_LIB_NAMES "omp")
    set(OpenMP_CXX_FLAGS "-fopenmp")
    set(OpenMP_CXX_LIB_NAMES "omp")
    set(OpenMP_CXX_INCLUDE_DIR "${LLVM_ROOT}/lib/clang/20/include")

    if(NOT MKL_DIR)
        set(MKL_DIR "C:/Program Files (x86)/Intel/oneAPI/mkl/latest")
    endif()
    set(MKL_INTERFACE "lp64")
    find_package(MKL REQUIRED)
endif()

find_package(OpenMP REQUIRED)

# Rmath
if (NOT DEFINED RMATH_INCLUDE_DIR OR NOT DEFINED RMATH_LIBRARY)
    if (OS_NAME STREQUAL "Linux")
        find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /storage/yangjianLab/sharedata/softwares/Rmath_v3.6.3_d20211126/include)
        find_library(RMATH_LIBRARY Rmath PATHS /storage/yangjianLab/sharedata/softwares/Rmath_v3.6.3_d20211126/lib)
    elseif(OS_NAME STREQUAL "MacOS")
        execute_process(COMMAND uname -m OUTPUT_VARIABLE ARCHITECTURE OUTPUT_STRIP_TRAILING_WHITESPACE)
        if("${ARCHITECTURE}" STREQUAL "arm64")
            find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /opt/homebrew/include)
            find_library(RMATH_LIBRARY Rmath PATHS /opt/homebrew/lib)
        else()
            find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /usr/local/include)
            find_library(RMATH_LIBRARY Rmath PATHS /usr/local/lib)
        endif()
    elseif(OS_NAME STREQUAL "Windows")
        find_path(RMATH_INCLUDE_DIR Rmath.h PATHS "C:/R/include")
        find_library(RMATH_LIBRARY Rmath PATHS "C:/R/lib")
    endif()
endif()

if (NOT RMATH_INCLUDE_DIR OR NOT RMATH_LIBRARY)
    message(FATAL_ERROR "Could NOT find Rmath (Rmath.h and libRmath). You can set -DRMATH_INCLUDE_DIR=... -DRMATH_LIBRARY=...")
endif()

add_subdirectory(lib)

set(PROJECT_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/include)
set(SOURCE_FILES
    src/l0_com.cpp src/l0_io.cpp src/l0_mem.cpp src/l0_stat.cpp
    src/l1_op_geno.cpp src/l1_stat.cpp
    src/l2_besd.cpp src/l2_bfile.cpp src/l2_efile.cpp src/l2_enet.cpp
    src/l2_reml.cpp
    src/l3_efile.cpp src/l3_ewas.cpp src/l3_glmnet.cpp src/l3_gwas.cpp src/l3_permutation.cpp
    src/l3_smr.cpp src/l3_vqtl.cpp
    src/l4_osc.cpp src/cis_learn_beta.cpp
    src/dcdflib.cpp src/Module_vqtl_drm_svlm.c
)

add_executable(osca ${SOURCE_FILES})

# Includes per target
target_include_directories(osca PRIVATE
    ${PROJECT_INCLUDE_DIR}
    ${zlib_SOURCE_DIR}
    ${gsl_SOURCE_DIR}/include
    ${eigen_SOURCE_DIR}
    ${MKL_INCLUDE}
    ${RMATH_INCLUDE_DIR}
)

# Compiler flags
if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
    target_compile_options(osca PRIVATE -fopenmp)
elseif(CMAKE_C_COMPILER_ID STREQUAL "Clang" AND NOT CMAKE_C_COMPILER_VERSION MATCHES "Apple")
    target_compile_options(osca PRIVATE -fopenmp)
elseif(MSVC)
    target_compile_options(osca PRIVATE /openmp)
endif()

# Link libraries (per arch)cd
if(OS_NAME STREQUAL "Linux" AND CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "x86_64")
    target_link_libraries(osca PRIVATE
        ${RMATH_LIBRARY}
        OpenMP::OpenMP_CXX
        Threads::Threads
        MKL::MKL
        z
        gsl
        gslcblas
        oscalib
        gomp
        pthread
        m
        dl
        uuid
    )
elseif(OS_NAME STREQUAL "MacOS")
    target_link_libraries(osca PRIVATE
        OpenMP::OpenMP_CXX
        Threads::Threads
        z
        gsl
        gslcblas
        ${RMATH_LIBRARY}
        oscalib
    )
    find_library(ACCELERATE_LIBRARY Accelerate)
    if(ACCELERATE_LIBRARY)
        target_link_libraries(osca PRIVATE ${ACCELERATE_LIBRARY})
    endif()
elseif(OS_NAME STREQUAL "Windows")
    target_link_libraries(osca PRIVATE
        MKL::MKL
        ${RMATH_LIBRARY}
        OpenMP::OpenMP_CXX
        Threads::Threads
        z
        gsl
        gslcblas
        oscalib
    )
endif()

# aarch64 macOS only
# if(CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "arm64" AND OS_NAME STREQUAL "MacOS")
#     target_link_libraries(osca PRIVATE
#         /opt/homebrew/lib/libz.a
#         /opt/homebrew/lib/libgsl.a
#         /opt/homebrew/lib/libgslcblas.a
#         /opt/homebrew/lib/libomp.a
#         ${CMAKE_BINARY_DIR}/lib/liboscalib.a
#         ${RMATH_LIBRARY}
#         pthread
#         m
#     )
# endif()

# Optional custom search path
if(CUSTOM_INCLUDE_SEARCH_PATH)
    target_include_directories(osca PRIVATE ${CUSTOM_INCLUDE_SEARCH_PATH})
endif()
if(CUSTOM_LIB_SEARCH_PATH)
    link_directories(${CUSTOM_LIB_SEARCH_PATH})
endif()

# Install
if(LINUX)
    set(CMAKE_INSTALL_RPATH "\$ORIGIN/../lib")
    set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH OFF)

    set_target_properties(osca PROPERTIES
        INSTALL_RPATH "\$ORIGIN/../lib"
        BUILD_WITH_INSTALL_RPATH TRUE
    )

    install(TARGETS osca ${PROJECT_LIBS}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

    install(FILES ${RMATH_LIBRARY} DESTINATION lib)
    install(FILES ${CMAKE_SOURCE_DIR}/resources/osca.desktop DESTINATION share/applications)
    install(FILES ${CMAKE_SOURCE_DIR}/resources/osca.png DESTINATION share/icons/hicolor/256x256/apps)
    install(FILES ${CMAKE_SOURCE_DIR}/resources/osca.svg DESTINATION share/icons/hicolor/scalable/apps)

elseif(WIN32)
    install(TARGETS osca ${PROJECT_LIBS} DESTINATION bin)

    file(GLOB RUNTIME_DLLS "${CMAKE_BINARY_DIR}/*.dll")
    install(FILES ${RUNTIME_DLLS} DESTINATION bin)

    # 可选：MKL DLLs 等
    # install(FILES ${MKL_ROOT}/bin/mkl_core.dll ... DESTINATION bin)

elseif(APPLE)
    set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
    set(CMAKE_BUILD_WITH_INSTALL_RPATH OFF)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH OFF)

    install(TARGETS osca ${PROJECT_LIBS}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
endif()

message(STATUS "OSCA build configuration complete.")