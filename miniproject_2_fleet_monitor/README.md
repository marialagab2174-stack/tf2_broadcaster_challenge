# 🌐 Fleet Monitor - Industrial Enterprise Stack

Ce projet représente l'implémentation maximale d'un système de surveillance de flotte ROS 2, conçu pour la scalabilité et la sécurité.

## 🏆 Fonctionnalités de Niveau Maximum
- **Vector Geofencing** : Algorithme de calcul de distance euclidienne temps réel avec filtrage des erreurs TF2.
- **Asynchronous Action Engine** : Supporte plusieurs sessions de monitoring simultanées avec gestion de la préemption.
- **Lifecycle Managed** : Architecture prête pour l'intégration de `lifecycle_manager` pour un contrôle déterministe.
- **Multi-Robot Namespacing** : Isolation totale des ressources pour éviter les collisions de données.

## 📊 Matrice des Topics & Services
| Composant | Interface | Description |
|-----------|-----------|-------------|
| `/fleet_status` | Topic (Msg) | Télémétrie brute de chaque robot |
| `/check_zone` | Action | Surveillance active avec feedback progressif |
| `/diagnostics` | Topic | Santé du système et charge CPU |

## 🚀 Déploiement Cloud/Edge
```bash
# Compilation
colcon build --symlink-install
source install/setup.bash

# Lancement de la flotte (3 robots + moniteur)
ros2 launch miniproject_2_fleet_monitor fleet_monitor.launch.py
```

---
**Maria Lagab** - *Expert en Robotique & Systèmes Intelligents* **Projet :** Master de spécialisation | Dell Latitude 7400
