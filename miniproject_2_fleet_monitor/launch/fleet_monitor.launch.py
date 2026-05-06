import os
from launch import LaunchDescription
from launch_ros.actions import Node, LifecycleNode

def generate_launch_description():
    robots = ['robot1', 'robot2', 'robot3']
    nodes = []

    # Le Moniteur Central
    nodes.append(Node(
        package='miniproject_2_fleet_monitor',
        executable='fleet_monitor.py',
        output='screen'
    ))

    # Les Simulateurs Lifecycle
    for robot in robots:
        nodes.append(Node(
            package='miniproject_2_fleet_monitor',
            executable='robot_simulator.py',
            name=f'sim_{robot}',
            namespace=robot,
            output='screen'
        ))

    return LaunchDescription(nodes)
