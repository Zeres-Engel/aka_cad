# Install script for directory: /app/lib/libnest2d

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
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

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D/Libnest2DTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D/Libnest2DTargets.cmake"
         "/app/build/lib/libnest2d/CMakeFiles/Export/lib/cmake/Libnest2D/Libnest2DTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D/Libnest2DTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D/Libnest2DTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D" TYPE FILE FILES "/app/build/lib/libnest2d/CMakeFiles/Export/lib/cmake/Libnest2D/Libnest2DTargets.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/libnest2d.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/nester.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/geometry_traits.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/geometry_traits_nfp.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/common.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/parallel.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/optimizer.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/metaloop.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/rotfinder.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/rotcalipers.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/bigint.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/rational.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/utils" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/utils/boost_alg.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/placers" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/placers/placer_boilerplate.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/placers" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/placers/bottomleftplacer.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/placers" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/placers/nfpplacer.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/selections" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/selections/selection_boilerplate.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/selections" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/selections/filler.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/selections" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/selections/firstfit.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/selections" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/selections/djd_heuristic.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/backends/clipper" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/backends/clipper/geometries.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/backends/clipper" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/backends/clipper/clipper_polygon.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/optimizers/nlopt" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/optimizers/nlopt/simplex.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/optimizers/nlopt" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/optimizers/nlopt/subplex.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/optimizers/nlopt" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/optimizers/nlopt/genetic.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/libnest2d/optimizers/nlopt" TYPE FILE FILES "/app/lib/libnest2d/include/libnest2d/optimizers/nlopt/nlopt_boilerplate.hpp")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D" TYPE FILE FILES
    "/app/build/lib/libnest2d/Libnest2DConfig.cmake"
    "/app/build/lib/libnest2d/Libnest2DConfigVersion.cmake"
    "/app/lib/libnest2d/cmake_modules/FindClipper.cmake"
    "/app/lib/libnest2d/cmake_modules/FindNLopt.cmake"
    "/app/lib/libnest2d/cmake_modules/FindTBB.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Libnest2D" TYPE FILE FILES "/app/build/lib/libnest2d/rp_packages_build/RPPackageVersions.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/app/build/lib/libnest2d/include/libnest2d/backends/clipper/cmake_install.cmake")
  include("/app/build/lib/libnest2d/include/libnest2d/optimizers/nlopt/cmake_install.cmake")

endif()

