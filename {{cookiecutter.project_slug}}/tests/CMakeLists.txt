add_executable(tests tests.cpp {{ cookiecutter.project_slug }}_t.cpp)
target_link_libraries(
  tests PUBLIC
  {{ cookiecutter.project_slug }}
  GTest::gtest
  GTest::gtest_main
  GTest::gmock
  GTest::gmock_main
)

# Allow user to run tests with `make test` or `ctest`
gtest_discover_tests(tests)
add_test(NAME tests COMMAND tests)

