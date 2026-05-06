# 📊 Fleet Monitor - ROS 2 Lifecycle & Actions

Système de supervision avancé pour flotte de robots utilisant les états de cycle de vie et la gestion de zone par actions.

## 📋 Spécifications Techniques
- **Nodes Lifecycle** : Les simulateurs de robots utilisent `rclpy_lifecycle` pour un contrôle précis (Config, Activate, Deactivate).
- **TF2 Broadcast** : Chaque robot publie sa position `world -> robotN/base_link`.
- **Action Server** : Le node `fleet_monitor` expose une action `/check_zone` pour valider la position d'un robot avec feedback en temps réel.
- **Config YAML** : Seuils d'alerte et rayons de zone configurables dynamiquement.

## 🏗 Architecture
1. **Robot Simulator (N)** : Émet des transformations TF.
2. **Fleet Monitor** : Centralise les TF et gère la logique de sécurité.
3. **Action Client** : Permet d'interroger le moniteur sur la conformité d'un robot.

## 🚀 Lancement
```bash
# 1. Build
colcon build --packages-select miniproject_2_fleet_monitor
source install/setup.bash

# 2. Launch
ros2 launch miniproject_2_fleet_monitor fleet_monitor.launch.py
```

---
**Maria Lagab** - *Ingénierie Robotique*
