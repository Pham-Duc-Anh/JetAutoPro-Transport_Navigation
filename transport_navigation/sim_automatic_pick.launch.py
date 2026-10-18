import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction

def launch_setup(context):
    try:
        example_package_path = get_package_share_directory('example')
    except:
        example_package_path = '/home/ducanh1/ros2_ws3/src/example'

    debug = LaunchConfiguration('debug', default='false')
    enable_display = LaunchConfiguration('enable_display', default='true')
    place_without_color = LaunchConfiguration('place_without_color', default='true')
    place_position = LaunchConfiguration('place_position', default="[-2.5, 1.5, 0.0, 0.0, 0.0]")
    robot_name = LaunchConfiguration('robot_name', default=os.environ.get('HOST', ''))

    debug_arg = DeclareLaunchArgument('debug', default_value=debug)
    enable_display_arg = DeclareLaunchArgument('enable_display', default_value=enable_display)
    place_without_color_arg = DeclareLaunchArgument('place_without_color', default_value=place_without_color)
    place_position_arg = DeclareLaunchArgument('place_position', default_value=place_position)
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value=robot_name)

    automatic_pick_node = Node(
        package='jetauto_simulation',
        executable='pick.py',
        output='screen',
        parameters=[
            os.path.join(example_package_path, 'config/automatic_pick_roi.yaml'), 
            {
                'debug': debug, 
                'enable_display': enable_display, 
                'place_without_color': place_without_color, 
                'place_position': place_position,
                'use_sim_time': True # ADDED use_sim_time for simulation
            }
        ]
    )

    servo_to_gazebo_node = Node(
        package='jetauto_simulation',
        executable='servo_to_gazebo.py',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return [debug_arg, 
            enable_display_arg,
            place_without_color_arg, 
            place_position_arg,
            robot_name_arg, 
            automatic_pick_node,
            servo_to_gazebo_node
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
