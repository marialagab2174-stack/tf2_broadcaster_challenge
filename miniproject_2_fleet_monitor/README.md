# 📊 Fleet Monitor Enterprise - Spécification Maximum

Ce projet est un système de surveillance de flotte industrielle développé sous **ROS 2 Jazzy**. Il permet de gérer le cycle de vie de plusieurs robots simulés et de garantir leur sécurité via un système de **Geofencing Vectoriel** asynchrone.

## 🚀 Architecture du Système

### 1. Nodes Lifecycle (Gestion du Cycle de Vie)
- **robot_simulator_N** : Nœuds managés (`rclpy_lifecycle`) simulant le comportement physique et cinématique des robots.
- **État Contrôlé** : Support des transitions `Configure`, `Activate` et `Deactivate` pour une mise en service sécurisée.

### 2. Monitoring & Geofencing (TF2)
- **TF2 Buffer** : Écouteur de transformations haute fréquence (`world -> robotN/base_link`).
- **Calcul de Distance** : Algorithme de calcul euclidien temps réel : $d = \sqrt{x^2 + y^2}$.
- **Alertes Dynamiques** : Niveaux d'avertissement progressifs basés sur la proximité des limites de zone.

### 3. Action Server /check_zone
Le cœur de la surveillance repose sur une **Action ROS 2** permettant :
- **Feedback continu** : Envoi de la distance actuelle et du niveau de danger à l'opérateur.
- **Preemption** : Possibilité d'annuler ou de modifier une mission de surveillance en cours.
- **Rapport Final** : Diagnostic complet envoyé à la fin de chaque session de monitoring.

## 📋 Spécifications Techniques

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Middleware** | ROS 2 Jazzy | Communication inter-nodes |
| **Coordination** | TF2_ROS | Gestion des repères spatiaux |
| **Interface** | Action Server | Protocole de surveillance asynchrone |
| **Config** | YAML | Paramétrage des rayons et fréquences |

## 🛠 Installation et Déploiement

### Compilation
```bash
cd ~/ros2_ws
colcon build --packages-select miniproject_2_fleet_monitor
source install/setup.bash
```

### Lancement de la Flotte Complète
```bash
# Lance le moniteur et 3 simulateurs de robots
ros2 launch miniproject_2_fleet_monitor fleet_monitor.launch.py
```

### Test d'une Action de Surveillance
```bash
ros2 action send_goal /check_zone miniproject_2_fleet_monitor/action/CheckZone "{robot_id: 'robot1', radius: 5.0}" --feedback
```

## 📈 Visualisation
Utilisez **rqt_graph** pour visualiser l'isolation des namespaces et **RViz2** pour suivre les transformations TF des robots en temps réel.

---
**Développeur :** Maria Lagab  
**Spécialité :** Robotique et Système Intelligent  
**Environnement :** Ubuntu 24.04 | Dell Latitude 7400
