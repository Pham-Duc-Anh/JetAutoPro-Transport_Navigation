cmake_minimum_required(VERSION 3.8)
project(jetauto_simulation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(DIRECTORY
  launch
  urdf
  worlds
  bridge_config
  rviz_config
  meshes
  map
  params
  plugin
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  transport_navigation/pick.py
  transport_navigation/transport.py
  transport_navigation/servo_to_gazebo.py
  DESTINATION lib/${PROJECT_NAME}
)

install(FILES
  transport_navigation/sim_automatic_pick.launch.py
  transport_navigation/sim_navigation_transport.launch.py
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
