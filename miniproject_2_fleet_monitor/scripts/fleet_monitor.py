#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse
from tf2_ros import Buffer, TransformListener
from miniproject_2_fleet_monitor.action import CheckZone
from miniproject_2_fleet_monitor.msg import FleetStatus
import math

class FleetMonitor(Node):
    def __init__(self):
        super().__init__('fleet_monitor')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        # Publisher pour le monitoring global
        self.status_pub = self.create_publisher(FleetStatus, 'fleet_status', 10)
        
        # Action Server pour la vérification de zone
        self._action_server = ActionServer(
            self, CheckZone, 'check_zone',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback
        )
        self.get_logger().info("✅ Fleet Monitor Enterprise prêt (TF2 + Actions)")

    def goal_callback(self, goal_request):
        self.get_logger().info(f"Requête reçue pour : {goal_request.robot_id}")
        return GoalResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        robot_id = goal_handle.request.robot_id
        max_radius = goal_handle.request.radius
        feedback_msg = CheckZone.Feedback()
        
        self.get_logger().info(f"Surveillance active de {robot_id}...")

        while True:
            try:
                # Récupération de la position via TF2
                now = rclpy.time.Time()
                trans = self.tf_buffer.lookup_transform('world', f'{robot_id}/base_link', now)
                
                x = trans.transform.translation.x
                y = trans.transform.translation.y
                dist = math.sqrt(x**2 + y**2)

                feedback_msg.current_distance = dist
                feedback_msg.warning_level = 2 if dist > max_radius else (1 if dist > max_radius * 0.8 else 0)
                goal_handle.publish_feedback(feedback_msg)

                if dist > max_radius:
                    self.get_logger().error(f"🚨 ROBOT {robot_id} HORS ZONE !")
                    break
                
                import asyncio
                await asyncio.sleep(0.5)
            except Exception as e:
                self.get_logger().warn(f"Attente de TF pour {robot_id}...")
                import asyncio
                await asyncio.sleep(1.0)

        goal_handle.succeed()
        result = CheckZone.Result()
        result.success = False if dist > max_radius else True
        result.final_report = f"Session terminée. Distance finale: {dist:.2f}m"
        return result

def main():
    rclpy.init()
    node = FleetMonitor()
    rclpy.spin(node)
