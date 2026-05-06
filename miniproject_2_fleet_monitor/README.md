# 📊 Fleet Monitor - Professional Monitoring System

## 🌟 Points Forts du Développement
- **Geofencing Dynamique** : Calcul en temps réel de la distance euclidienne par rapport à l'origine du monde via **TF2**.
- **Action-Driven Safety** : Utilisation d'un serveur d'action asynchrone pour surveiller les dépassements de zone avec des niveaux d'alerte (OK / Warning / Critical).
- **Lifecycle Architecture** : Préparation des nodes pour une gestion d'état industrielle (Configure/Activate).
- **Multi-Robot Scalability** : Launch file automatisé pour gérer N robots sans modification de code.

## 🛠 Spécifications du Système
- **Topics** : 
  - `fleet_status` : État consolidé de la flotte.
- **Actions** :
  - `check_zone` : Paramètres (`robot_id`, `radius`). Feedback (`current_distance`).

## 🚀 Utilisation Avancée
```bash
# Lancer tout le système
ros2 launch miniproject_2_fleet_monitor fleet_monitor.launch.py

# Tester une surveillance via Action (dans un autre terminal)
ros2 action send_goal /check_zone miniproject_2_fleet_monitor/action/CheckZone "{robot_id: 'robot1', radius: 3.0}" --feedback
```

---
**Maria Lagab** - *Ingénierie des Systèmes Intelligents*
