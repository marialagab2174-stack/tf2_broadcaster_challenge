#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from tf2_ros import Buffer, TransformListener, LookupException, ConnectivityException, ExtrapolationException
from miniproject_2_fleet_monitor.action import CheckZone
from miniproject_2_fleet_monitor.msg import FleetStatus
import math
import asyncio

class FleetMonitor(Node):
    def __init__(self):
        super().__init__('fleet_monitor')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.status_pub = self.create_publisher(FleetStatus, 'fleet_status', 10)
        
        self._action_server = ActionServer(
            self, CheckZone, 'check_zone',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
        self.get_logger().info("🚀 SYSTÈME DE SURVEILLANCE MAXIMUM DÉPLOYÉ")

    def goal_callback(self, goal_request):
        # Validation de la requête
        if goal_request.radius <= 0:
            self.get_logger().error("Rayon invalide reçu!")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().warn("Annulation de la mission demandée.")
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        robot_id = goal_handle.request.robot_id
        max_radius = goal_handle.request.radius
        feedback_msg = CheckZone.Feedback()
        
        self.get_logger().info(f"Démarrage du Geofencing Vectoriel pour {robot_id}")

        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return CheckZone.Result(success=False, final_report="Mission annulée par l'opérateur")

            try:
                # Calcul de haute précision (Interpolation TF)
                t = self.tf_buffer.lookup_transform('world', f'{robot_id}/base_link', rclpy.time.Time())
                
                pos_x = t.transform.translation.x
                pos_y = t.transform.translation.y
                dist = math.sqrt(pos_x**2 + pos_y**2)

                # Mise à jour du Feedback
                feedback_msg.current_distance = dist
                # Niveaux : 0=Normal, 1=Attention (80%), 2=CRITIQUE
                feedback_msg.warning_level = 2 if dist > max_radius else (1 if dist > max_radius * 0.8 else 0)
                goal_handle.publish_feedback(feedback_msg)

                # Publication sur le topic de status
                status = FleetStatus()
                status.robot_id = robot_id
                status.distance_to_center = dist
                status.is_in_zone = dist <= max_radius
                self.status_pub.publish(status)

                if dist > max_radius:
                    self.get_logger().error(f"🔴 VIOLATION DE ZONE : {robot_id} est à {dist:.2f}m !")
                    break

                await asyncio.sleep(0.2) # Fréquence 5Hz

            except (LookupException, ConnectivityException, ExtrapolationException):
                self.get_logger().debug(f"TF momentanément indisponible pour {robot_id}...")
                await asyncio.sleep(0.5)

        goal_handle.succeed()
        return CheckZone.Result(success=True, final_report="Surveillance terminée avec succès")

def main():
    rclpy.init()
    node = FleetMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
