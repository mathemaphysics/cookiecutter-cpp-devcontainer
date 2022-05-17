cmake_minimum_required(VERSION 3.9)

# Set a name and a version number for your project:
project({{ cookiecutter.project_slug }} VERSION 0.0.1 LANGUAGES CXX)

# Initialize some default paths
include(GNUInstallDirs)
include(FetchContent)

# Define the minimum C++ standard that is required
set(CMAKE_CXX_STANDARD {{ cookiecutter.cxx_minimum_standard }})
set(CMAKE_CXX_STANDARD_REQUIRED ON)

{% if cookiecutter.python_bindings == "Yes" -%}
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
{%- endif %}

# Add GoogleTest at configure time for linking unit tests
if(BUILD_TESTING)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        release-1.11.0
  )
endif()

{% if cookiecutter.fetch_spdlog == "Yes" -%}
# Add spdlog at configure time for logging
FetchContent_Declare(
  spdlog
  GIT_REPOSITORY https://github.com/gabime/spdlog.git
  GIT_TAG        v1.9.1
)
{%- endif %}

{% if cookiecutter.fetch_jsoncpp == "Yes" -%}
# Add jsoncpp at configure time for configuration input
FetchContent_Declare(
  jsoncpp
  GIT_REPOSITORY https://github.com/open-source-parsers/jsoncpp.git
  GIT_TAG        1.9.4		
)
{%- endif %}

# Compilation options
{%- if cookiecutter.python_bindings == "Yes" %}
option(BUILD_PYTHON "Enable building of Python bindings" ON)
{%- endif %}
{%- if cookiecutter.doxygen == "Yes" or cookiecutter.readthedocs == "Yes" %}
option(BUILD_DOCS "Enable building of documentation" ON)
{%- endif %}

if(BUILD_TESTING)
# Make GTest::gtest etc. available here
  FetchContent_MakeAvailable(googletest)
endif()
{% if cookiecutter.fetch_spdlog == "Yes" -%}
FetchContent_MakeAvailable(spdlog)
{%- endif %}
{% if cookiecutter.fetch_jsoncpp == "Yes" -%}
FetchContent_MakeAvailable(jsoncpp)
{%- endif %}

{%- if cookiecutter.header_only == "No" %}

# Compile the library
add_subdirectory(src)
{% else %}
# Add an interface target for our header-only library
add_library({{ cookiecutter.project_slug }} INTERFACE)
target_include_directories({{ cookiecutter.project_slug }} INTERFACE
  $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}/include/>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
{%- endif %}

# Compile the application
add_subdirectory(app)

# Compile the tests
include(CTest)
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()

{% if cookiecutter.doxygen == "Yes" -%}
if(BUILD_DOCS)
  # Add the documentation
  add_subdirectory(doc)
endif()
{%- endif %}
{%- if cookiecutter.python_bindings == "Yes" %}
if(BUILD_PYTHON)
  # Add Python bindings
  {%- if cookiecutter.use_submodules == "Yes" %}
  add_subdirectory(ext/pybind11)
  {% else %}
  find_package(pybind11)
  {%- endif %}
  # Compile the Pybind11 module
  {%- set modname = cookiecutter.project_slug.replace("-", "") %}
  pybind11_add_module(_{{ modname }} python/{{ modname }}/_{{ cookiecutter.project_slug }}.cpp)
  target_link_libraries(_{{ modname }} PUBLIC {{ cookiecutter.project_slug }})

  # Install the Python module shared library
  install(TARGETS _{{ modname }} DESTINATION .)
endif()
{%- endif %}

# Add an alias target for use if this project is included as a subproject in another project
add_library({{ cookiecutter.project_slug }}::{{ cookiecutter.project_slug }} ALIAS {{ cookiecutter.project_slug }})

# Install targets and configuration
install(
  TARGETS {{ cookiecutter.project_slug }}
  EXPORT {{ cookiecutter.project_slug }}-config
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(
  EXPORT {{ cookiecutter.project_slug }}-config
  NAMESPACE {{ cookiecutter.project_slug }}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/{{ cookiecutter.project_slug }}
)

install(
  DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# This prints a summary of found dependencies
include(FeatureSummary)
feature_summary(WHAT ALL)
