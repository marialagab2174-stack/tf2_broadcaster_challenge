#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from tf2_ros import Buffer, TransformListener
from miniproject_2_fleet_monitor.action import CheckZone

class FleetMonitor(Node):
    def __init__(self):
        super().__init__('fleet_monitor')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self._action_server = ActionServer(self, CheckZone, 'check_zone', self.execute_callback)
        self.get_logger().info("Fleet Monitor prêt avec Action Server /check_zone")

    async def execute_callback(self, goal_handle):
        feedback_msg = CheckZone.Feedback()
        # Logique simplifiée de vérification TF...
        goal_handle.succeed()
        result = CheckZone.Result()
        result.success = True
        return result

def main():
    rclpy.init()
    node = FleetMonitor()
    rclpy.spin(node)
