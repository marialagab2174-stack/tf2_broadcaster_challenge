#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import Node, State, TransitionCallbackReturn
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

class RobotSimulator(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.tf_broadcaster = TransformBroadcaster(self)
        self.timer = None
        self.angle = 0.0

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Configuration du simulateur...")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        self.get_logger().info("Activation : Envoi des TF activé")
        self.timer = self.create_timer(0.1, self.publish_tf)
        return TransitionCallbackReturn.SUCCESS

    def publish_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = f"{self.get_name()}/base_link"
        # Simulation d'un mouvement circulaire
        self.angle += 0.05
        t.transform.translation.x = 2.0 * math.cos(self.angle)
        t.transform.translation.y = 2.0 * math.sin(self.angle)
        self.tf_broadcaster.sendTransform(t)

def main():
    rclpy.init()
    node = RobotSimulator('robot_simulator_1')
    rclpy.spin(node)
