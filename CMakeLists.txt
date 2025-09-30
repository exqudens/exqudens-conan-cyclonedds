cmake_minimum_required(VERSION "3.25" FATAL_ERROR)

string(REPLACE "." ";" PRESET_NAME_ELEMENTS "${PRESET_NAME}")

set(CMAKE_UTIL_FILE "" CACHE STRING "...")
set(USE_CONAN "1" CACHE BOOL "...")

if("${USE_CONAN}")
    if("windows" IN_LIST "PRESET_NAME_ELEMENTS")
        find_program(CONAN_COMMAND NAMES "conan.exe" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    else()
        find_program(CONAN_COMMAND NAMES "conan" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    endif()
endif()

if("${CMAKE_UTIL_FILE}" STREQUAL "")
    if("$ENV{CMAKE_UTIL_FILE}" STREQUAL "")
        if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake")
            if("${USE_CONAN}")
                #[[execute_process(
                    COMMAND "${CONAN_COMMAND}" "user" "$ENV{CONAN_LOGIN_USERNAME}" "-r" "artifactory" "-p"
                    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )]]
                execute_process(
                    COMMAND "${CONAN_COMMAND}" "install" "--tool-requires=exqudens-cmake/0.0.1" "--deployer" "direct_deploy" "--deployer-folder" "${CMAKE_SOURCE_DIR}/build/dependencies"
                    COMMAND_ECHO "STDERR"
                    ENCODING "UTF-8"
                    COMMAND_ERROR_IS_FATAL "ANY"
                )
                set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
            else()
                message(FATAL_ERROR "Unable to resolve CMAKE_UTIL_FILE: '${CMAKE_UTIL_FILE}'")
            endif()
        else()
            set(CMAKE_UTIL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/build/dependencies/direct_deploy/exqudens-cmake/cmake/util.cmake" CACHE STRING "..." FORCE)
        endif()
    else()
        set(CMAKE_UTIL_FILE "$ENV{CMAKE_UTIL_FILE}" CACHE STRING "..." FORCE)
    endif()
endif()

include("${CMAKE_UTIL_FILE}")

if("msvc-x64-x64" IN_LIST "PRESET_NAME_ELEMENTS")
    if(NOT EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../msvc-x64-x64-toolchain.cmake")
        set_msvc_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            VERSION "17"
            HOST "x64"
            TARGET "x64"
            SET_CMAKE_SYSTEM_NAME "0"
            OUTPUT_FILE "${CMAKE_CURRENT_BINARY_DIR}/../msvc-x64-x64-toolchain.cmake"
        )
    endif()
elseif("gcc" IN_LIST PRESET_NAME_ELEMENTS)
    if(NOT EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../gcc-toolchain.cmake")
        find_file(COMPILER_FILE NAMES "gcc" PATHS ENV GCC_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
        set_gnu_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            PATH "${COMPILER_FILE}"
            SET_CMAKE_SYSTEM_NAME "0"
            OUTPUT_FILE "${CMAKE_CURRENT_BINARY_DIR}/../gcc-toolchain.cmake"
        )
    endif()
endif()

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/name-version.json" NAME_VERSION_JSON)
string(JSON NAME GET "${NAME_VERSION_JSON}" "name")
string(JSON VERSION GET "${NAME_VERSION_JSON}" "version")
project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

enable_language("C")
enable_language("CXX")
#include("GenerateExportHeader")
#enable_testing()
#include("GoogleTest")

set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/cmake-install" CACHE PATH "..." FORCE)
set(CMAKE_VERBOSE_MAKEFILE "1" CACHE BOOL "..." FORCE)
set(CMAKE_EXPORT_COMPILE_COMMANDS "1" CACHE BOOL "..." FORCE)

set(CMAKE_OBJECT_PATH_MAX 1000)
set(CMAKE_SHARED_LIBRARY_PREFIX "")
set(CMAKE_SHARED_MODULE_PREFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_IMPORT_LIBRARY_PREFIX "")
set(CMAKE_STAGING_PREFIX "")
set(CMAKE_FIND_LIBRARY_PREFIXES "" "lib")
set(CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH FALSE)
set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH TRUE)
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_ROOT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_PATH TRUE)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG FALSE)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS FALSE)
set(CMAKE_BUILD_RPATH "\$ORIGIN")
set(CMAKE_INSTALL_RPATH "\$ORIGIN")
set(CMAKE_SKIP_BUILD_RPATH TRUE)
set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)
set(CMAKE_CXX_VISIBILITY_PRESET "hidden")
set(CMAKE_VISIBILITY_INLINES_HIDDEN TRUE)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED TRUE)
set(CMAKE_C_EXTENSIONS FALSE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_CXX_EXTENSIONS FALSE)

#[[separate_arguments(CMAKE_CXX_FLAGS NATIVE_COMMAND "${CMAKE_CXX_FLAGS}")
if(MSVC)
    if(NOT "/EHa" IN_LIST CMAKE_CXX_FLAGS AND "/EHsc" IN_LIST CMAKE_CXX_FLAGS)
        list(REMOVE_ITEM CMAKE_CXX_FLAGS "/EHsc")
        list(APPEND CMAKE_CXX_FLAGS "/EHa")
    endif()
endif()
string(JOIN " " CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})]]

string(TOLOWER "${PROJECT_NAME}" PROJECT_NAME_LOWER)
set(PROJECT_VERSION_NOTWEAK "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

cmake_path(CONVERT "$ENV{CMAKE_USER_HOME}" TO_CMAKE_PATH_LIST CMAKE_USER_HOME NORMALIZE)
if("" STREQUAL "${CMAKE_USER_HOME}")
    cmake_path(CONVERT "$ENV{HOME}" TO_CMAKE_PATH_LIST HOME NORMALIZE)
else()
    set(HOME "${CMAKE_USER_HOME}")
endif()
if(NOT EXISTS "${HOME}" OR NOT IS_DIRECTORY "${HOME}")
    message(FATAL_ERROR "HOME: '${HOME}' not exists or not directory.")
endif()
set(CMAKE_HOME "${HOME}/.cmake")
if(NOT EXISTS "${CMAKE_HOME}")
    file(MAKE_DIRECTORY "${CMAKE_HOME}")
endif()
if(NOT EXISTS "${CMAKE_HOME}" OR NOT IS_DIRECTORY "${CMAKE_HOME}")
    message(FATAL_ERROR "CMAKE_HOME: '${CMAKE_HOME}' not exists or not directory.")
endif()
set(CMAKE_DOWNLOADS "${CMAKE_HOME}/downloads")
if(NOT EXISTS "${CMAKE_DOWNLOADS}")
    file(MAKE_DIRECTORY "${CMAKE_DOWNLOADS}")
endif()
if(NOT EXISTS "${CMAKE_DOWNLOADS}" OR NOT IS_DIRECTORY "${CMAKE_DOWNLOADS}")
    message(FATAL_ERROR "CMAKE_DOWNLOADS: '${CMAKE_DOWNLOADS}' is not directory.")
endif()
if(NOT EXISTS "${CMAKE_DOWNLOADS}/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip")
    message(STATUS "download ...")
    file(MAKE_DIRECTORY "${PROJECT_BINARY_DIR}/tmp")
    file(DOWNLOAD
        "https://github.com/eclipse-cyclonedds/cyclonedds/archive/refs/tags/${PROJECT_VERSION_NOTWEAK}.zip"
        "${PROJECT_BINARY_DIR}/tmp/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip"
        EXPECTED_MD5 "768b83b76ea5a3715f0bb79465e2a8ab"
        STATUS downloadStatus
    )
    if(NOT "${downloadStatus}" STREQUAL "0;\"No error\"")
        message(FATAL_ERROR "downloadStatus: '${downloadStatus}'")
    endif()
    file(COPY "${PROJECT_BINARY_DIR}/tmp/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip" DESTINATION "${CMAKE_DOWNLOADS}")
    message(STATUS "... done")
endif()
if(NOT EXISTS "${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip")
    message(STATUS "copy from downloads ...")
    file(COPY "${CMAKE_DOWNLOADS}/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip" DESTINATION "${PROJECT_SOURCE_DIR}/build")
    message(STATUS "... done")
endif()
if(NOT EXISTS "${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}")
    message(STATUS "extract ...")
    file(ARCHIVE_EXTRACT INPUT "${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}.zip" DESTINATION "${PROJECT_SOURCE_DIR}/build")
    message(STATUS "... done")
endif()
set(BUILD_DIR "${PROJECT_SOURCE_DIR}/build")
cmake_path(RELATIVE_PATH "BUILD_DIR" BASE_DIRECTORY "${PROJECT_SOURCE_DIR}" OUTPUT_VARIABLE "BUILD_DIR_REL")

if("${USE_CONAN}")
    set_conan_architecture(CONAN_ARCH "${CMAKE_SYSTEM_PROCESSOR}")
    set_conan_os(CONAN_OS "${CMAKE_SYSTEM_NAME}")
    set_conan_compiler(CONAN_COMPILER "${CMAKE_C_COMPILER_ID}")
    set_conan_compiler_version(CONAN_COMPILER_VERSION "${CMAKE_C_COMPILER_ID}" "${CMAKE_C_COMPILER_VERSION}" MAX_ELEMENTS "1")
    set_conan_compiler_runtime(CONAN_COMPILER_RUNTIME "${CMAKE_MSVC_RUNTIME_LIBRARY}")
    set_conan_compiler_runtime_type(CONAN_COMPILER_RUNTIME_TYPE "${CMAKE_MSVC_RUNTIME_LIBRARY}")

    set_python_boolean(CONAN_BUILD_SHARED_LIBS "${BUILD_SHARED_LIBS}")

    set_conan_settings(CONAN_SETTINGS
        "arch=${CONAN_ARCH}"
        "os=${CONAN_OS}"
        "compiler=${CONAN_COMPILER}"
        "compiler.version=${CONAN_COMPILER_VERSION}"
        "compiler.cstd=${CMAKE_C_STANDARD}"
        "compiler.cppstd=${CMAKE_CXX_STANDARD}"
        "compiler.runtime=${CONAN_COMPILER_RUNTIME}"
        "compiler.runtime_type=${CONAN_COMPILER_RUNTIME_TYPE}"
        "compiler.libcxx=${CONAN_COMPILER_LIBCXX}"
        "build_type=${CMAKE_BUILD_TYPE}"
    )
    set_conan_options(CONAN_OPTIONS
        "&:shared=${CONAN_BUILD_SHARED_LIBS}"
        "*:shared=${CONAN_BUILD_SHARED_LIBS}"
    )
endif()

#if("${ENABLE_SECURITY}" STREQUAL "")
#    set(ENABLE_SECURITY "0" CACHE STRING "..." FORCE)
#endif()
#set(BUILD_IDLC "1" CACHE STRING "..." FORCE)
#set(BUILD_EXAMPLES "1" CACHE STRING "..." FORCE)

message(STATUS "CMAKE_TOOLCHAIN_FILE: '${CMAKE_TOOLCHAIN_FILE}'")
message(STATUS "PROJECT_NAME: '${PROJECT_NAME}'")
message(STATUS "PROJECT_VERSION: '${PROJECT_VERSION}'")
message(STATUS "PROJECT_NAME_LOWER: '${PROJECT_NAME_LOWER}'")
message(STATUS "PROJECT_VERSION_NOTWEAK: '${PROJECT_VERSION_NOTWEAK}'")
message(STATUS "BUILD_DIR: '${BUILD_DIR}'")
message(STATUS "BUILD_DIR_REL: '${BUILD_DIR_REL}'")
message(STATUS "CONAN_SETTINGS: '${CONAN_SETTINGS}'")
message(STATUS "CONAN_OPTIONS: '${CONAN_OPTIONS}'")

add_subdirectory("${BUILD_DIR_REL}/${PROJECT_NAME_LOWER}-${PROJECT_VERSION_NOTWEAK}")

add_custom_command(
    OUTPUT "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME_LOWER}/lib/cmake/CycloneDDS/CycloneDDSConfig.cmake"
    COMMAND "${CMAKE_COMMAND}" "--install" "${PROJECT_BINARY_DIR}" "--prefix" "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME_LOWER}"
    #DEPENDS "ddsc"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("cmake-install"
    DEPENDS "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME_LOWER}/lib/cmake/CycloneDDS/CycloneDDSConfig.cmake"
)

if("${USE_CONAN}")
    add_custom_target("conan-export"
        COMMAND "${CONAN_COMMAND}" "export-pkg"
                "--output-folder" "${CMAKE_INSTALL_PREFIX}/${PROJECT_NAME_LOWER}"
                ${CONAN_SETTINGS}
                ${CONAN_OPTIONS}
                #"--user" "gitlab-group+gitlab-sub-group+${PROJECT_NAME}"
                #"--channel" "stable"
                "${PROJECT_SOURCE_DIR}/conanfile.py"
        DEPENDS "cmake-install"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-remove"
        COMMAND "${CONAN_COMMAND}" "remove" "-c" "${PROJECT_NAME_LOWER}/${PROJECT_VERSION}"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_target("conan-list"
        COMMAND "${CONAN_COMMAND}" "list" "${PROJECT_NAME_LOWER}/${PROJECT_VERSION}:*"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )
endif()
