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

# MKL：用户可自行设置 MKL_ROOT 环境变量或通过 -DMKL_ROOT=path 来指定
if(OS_NAME STREQUAL "Linux" OR OS_NAME STREQUAL "Windows")
    if(NOT DEFINED MKL_ROOT)
        set(MKL_ROOT "/opt/intel/mkl" CACHE PATH "Intel MKL root directory")
    endif()
    find_package(MKL REQUIRED PATHS ${MKL_ROOT} NO_DEFAULT_PATH)
endif()

# OpenMP
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    message(STATUS "OpenMP found")
else()
    message(WARNING "OpenMP not found, trying manual setup")
    if(APPLE)
        message(STATUS "Trying manual OpenMP setup on macOS")
        set(OpenMP_C_FLAGS "-Xpreprocessor -fopenmp")
        set(OpenMP_C_LIB_NAMES "omp")
        set(OpenMP_C_INCLUDE_DIR "/opt/homebrew/opt/libomp/include")
        set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp")
        set(OpenMP_CXX_LIB_NAMES "omp")
        set(OpenMP_CXX_INCLUDE_DIR "/opt/homebrew/opt/libomp/include")
        set(OpenMP_omp_LIBRARY "/opt/homebrew/opt/libomp/lib/libomp.dylib")
        find_package(OpenMP REQUIRED)
    elseif(UNIX)
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fopenmp")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")
        find_package(OpenMP REQUIRED)
    elseif(WIN32)
        set(OpenMP_C_FLAGS "-fopenmp")
        set(OpenMP_CXX_FLAGS "-fopenmp")
        set(OpenMP_omp_LIBRARY "${LLVM_ROOT}/lib/libomp.lib")
        find_package(OpenMP REQUIRED)
    endif()
endif()

# === Detect and configure Rmath (Rmath.h + libRmath) for different systems ===
if (UNIX AND NOT APPLE)
    find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /usr/include /usr/local/include)
    find_library(RMATH_LIBRARY Rmath PATHS /usr/lib /usr/local/lib)
elseif(APPLE)
    execute_process(
        COMMAND uname -m
        OUTPUT_VARIABLE ARCHITECTURE
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    
    if("${ARCHITECTURE}" STREQUAL "arm64")
        find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /opt/homebrew/include)
        find_library(RMATH_LIBRARY Rmath PATHS /opt/homebrew/lib)
    else()
        find_path(RMATH_INCLUDE_DIR Rmath.h PATHS /usr/local/include)
        find_library(RMATH_LIBRARY Rmath PATHS /usr/local/lib)
    endif()
elseif(WIN32)
    find_path(RMATH_INCLUDE_DIR Rmath.h PATHS "C:/R/include")
    find_library(RMATH_LIBRARY Rmath PATHS "C:/R/lib")
endif()

if (NOT RMATH_INCLUDE_DIR OR NOT RMATH_LIBRARY)
    message(FATAL_ERROR "Could NOT find Rmath (Rmath.h and libRmath)")
endif()

include_directories(${RMATH_INCLUDE_DIR})

add_subdirectory(lib)

find_package(Threads REQUIRED)

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

target_link_libraries(osca PRIVATE ${RMATH_LIBRARY})

target_include_directories(osca PRIVATE
    ${PROJECT_INCLUDE_DIR}
    ${zlib_SOURCE_DIR}
    ${gsl_SOURCE_DIR}/include
    ${eigen_SOURCE_DIR}
    ${RMATH_INCLUDE_DIR}   
)

if(DEFINED MKL_INCLUDE_DIR)
    target_include_directories(osca PRIVATE ${MKL_INCLUDE_DIR})
endif()

if(BUILD_STATIC)
    message(WARNING "Static linking requested: please ensure static libs installed on your system.")
endif()

if(CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "x86_64")
    if(OS_NAME STREQUAL "Linux")
        if(CMAKE_C_COMPILER_ID STREQUAL "GNU")
            target_compile_options(osca PRIVATE -fopenmp)
            if(BUILD_STATIC)
                target_link_libraries(osca PRIVATE
                    -static
                    z
                    Threads::Threads
                    OpenMP::OpenMP_CXX
                    mkl_core mkl_intel_lp64 mkl_gnu_thread
                    gomp pthread
                    Rmath gsl gslcblas
                    m oscalib dl uuid
                )
            else()
                target_link_libraries(osca PRIVATE
                    z
                    Threads::Threads
                    OpenMP::OpenMP_CXX
                    mkl_core mkl_intel_lp64 mkl_gnu_thread
                    gomp pthread
                    Rmath gsl gslcblas
                    m oscalib dl uuid
                )
            endif()
        elseif(CMAKE_C_COMPILER_ID STREQUAL "Clang")
            target_compile_options(osca PRIVATE -fopenmp)
            target_link_libraries(osca PRIVATE
                z
                Threads::Threads
                OpenMP::OpenMP_CXX
                mkl_core mkl_intel_lp64 mkl_gnu_thread
                gomp pthread
                Rmath gsl gslcblas
                m oscalib dl uuid
            )
        endif()
    elseif(OS_NAME STREQUAL "MacOS")
        find_package(OpenMP REQUIRED)
        target_compile_options(osca PRIVATE -Xpreprocessor -fopenmp)
        target_link_libraries(osca PRIVATE
            z
            Threads::Threads
            OpenMP::OpenMP_CXX
            gsl gslcblas Rmath m oscalib
        )
        find_library(ACCELERATE_LIBRARY Accelerate)
        if(ACCELERATE_LIBRARY)
            target_link_libraries(osca PRIVATE ${ACCELERATE_LIBRARY})
        endif()
    elseif(OS_NAME STREQUAL "Windows")
        target_compile_options(osca PRIVATE /openmp)
        target_link_libraries(osca PRIVATE
            z
            gsl gslcblas Rmath m oscalib
            Threads::Threads
            OpenMP::OpenMP_CXX
        )
    endif()
elseif(CMAKE_HOST_SYSTEM_PROCESSOR STREQUAL "arm64")
    if(OS_NAME STREQUAL "MacOS")
        target_include_directories(osca PRIVATE
            /opt/homebrew/include
            /opt/homebrew/include/gsl
        )
        target_link_libraries(osca PRIVATE
            /opt/homebrew/lib/libz.a
            /opt/homebrew/lib/libgsl.a
            /opt/homebrew/lib/libgslcblas.a
            /opt/homebrew/lib/libomp.a
            ${CMAKE_BINARY_DIR}/lib/liboscalib.a
            Rmath pthread m 
        )

    else()
        message(FATAL_ERROR "arm64 only supported on MacOS currently.")
    endif()
else()
    message(WARNING "Only x86_64 and arm64 architectures tested.")
endif()

if(CUSTOM_INCLUDE_SEARCH_PATH)
    target_include_directories(osca PRIVATE ${CUSTOM_INCLUDE_SEARCH_PATH})
endif()
if(CUSTOM_LIB_SEARCH_PATH)
    link_directories(${CUSTOM_LIB_SEARCH_PATH})
endif()

install(TARGETS osca RUNTIME DESTINATION bin)

message(STATUS "OSCA build configuration complete.")