import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction, OpaqueFunction, TimerAction, ExecuteProcess

def launch_setup(context):
    try:
        slam_package_path = get_package_share_directory('slam')
        navigation_package_path = get_package_share_directory('navigation')
        jetauto_simulation_path = get_package_share_directory('jetauto_simulation')
    except:
        slam_package_path = '/home/ducanh1/ros2_ws3/src/slam'
        navigation_package_path = '/home/ducanh1/ros2_ws3/src/navigation'
        jetauto_simulation_path = '/home/ducanh1/jetauto_simulation'

    map_name = LaunchConfiguration('map', default='map5').perform(context)
    debug = LaunchConfiguration('debug', default='false')
    place_without_color = LaunchConfiguration('place_without_color', default='true')
    place_position = LaunchConfiguration('place_position', default="[-2.5, 1.5, 0.0, 0.0, 0.0]")
    robot_name = LaunchConfiguration('robot_name', default=os.environ.get('HOST', ''))

    map_name_arg = DeclareLaunchArgument('map', default_value=map_name)
    debug_arg = DeclareLaunchArgument('debug', default_value=debug)
    place_without_color_arg = DeclareLaunchArgument('place_without_color', default_value=place_without_color)
    place_position_arg = DeclareLaunchArgument('place_position', default_value=place_position)
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value=robot_name)

    sim_automatic_pick_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sim_automatic_pick.launch.py')

    automatic_pick_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(sim_automatic_pick_path),
        launch_arguments={
            'debug': debug,
            'place_without_color': place_without_color,
            'place_position': place_position,
            'robot_name': robot_name,
            'enable_display': 'false',
        }.items(),
    )

    navigation_transport_node = Node(
        package='jetauto_simulation',
        executable='transport.py',
        output='screen',
        parameters=[{'map_frame': 'map', 'nav_goal': '/nav_goal', 'use_sim_time': True}] # ADDED use_sim_time
    )

    bringup_launch = GroupAction(
     actions=[
         PushRosNamespace(robot_name),
         automatic_pick_launch,
      ]
    )

    return [map_name_arg, 
            debug_arg, 
            place_without_color_arg, 
            place_position_arg,
            robot_name_arg,
            bringup_launch, 
            navigation_transport_node
            ]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function = launch_setup)
    ])

if __name__ == '__main__':
    ld = generate_launch_description()
    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
