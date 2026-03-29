# scooby_camera

Questo pacchetto ROS2 pubblica i dati della camera Raspberry Pi su un topic visualizzabile da RViz.

## Installazione dipendenze

Assicurati di avere installato:
- ROS2 (Humble o successivo)
- `opencv-python`
- `cv_bridge`

## Build del pacchetto

Da dentro la root del workspace ROS2:

```
colcon build --packages-select scooby_camera
```

## Esecuzione del nodo

```
source install/setup.bash
ros2 run scooby_camera camera_publisher
```

## Visualizzazione in RViz

Su un altro PC connesso alla stessa rete, lancia RViz e aggiungi una visualizzazione di tipo `Image` sul topic:

```
/scooby/camera/image_raw
```

Assicurati che le variabili di ambiente ROS_DOMAIN_ID e ROS_MASTER_URI siano configurate correttamente per la comunicazione in rete.
