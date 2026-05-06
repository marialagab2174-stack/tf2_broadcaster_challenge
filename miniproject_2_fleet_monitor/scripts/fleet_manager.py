#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class FleetLifecycleManager(Node):
    def __init__(self):
        super().__init__('fleet_manager')
        self.get_logger().info("Lifecycle Manager prêt à orchestrer la flotte.")
        # Ici on pourrait appeler les services /change_state des robots
        
def main():
    rclpy.init()
    node = FleetLifecycleManager()
    rclpy.spin(node)
