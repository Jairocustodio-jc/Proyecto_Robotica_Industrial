#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from entrega1_ri.msg import ArrayXY

class Lidar(object):
    def __init__(self):
        # Crear el suscriptor al tópico del LiDAR
        topic = 'scan'
        self.sub = rospy.Subscriber(topic, LaserScan, self.callback)
        self.Scan = None
        self.stop_threshold = 0.4  # Umbral de distancia para detener el movimiento
        self.camera_exclusion_radius = 0.15  # Radio de exclusión para la cámara
        
        # Precalcular un vector de numpy que contenga los ángulos para cada rango.
        self.angles = None
        rospy.loginfo("Inicializado Lidar y suscriptor al tópico 'scan'")
        
    def callback(self, msg):
        # Callback para el suscriptor
        self.Scan = msg
        
        # Precalcular los ángulos solo la primera vez
        if self.angles is None:
            self.angles = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment, dtype=float)
            if len(self.angles) < len(msg.ranges):
                self.angles = np.append(self.angles, msg.angle_max)
            rospy.loginfo("Ángulos del LiDAR precalculados.")

    def get_xy(self):
        """ Retorna los valores x,y de la medición, en el sistema del LiDAR """
        if self.Scan is None:
            rospy.logwarn("No se ha recibido ningún mensaje de LiDAR.")
            return np.array([]), np.array([])

        # Obtener los rangos medidos
        scan = self.Scan
        ranges = np.array(scan.ranges).flatten()

        # Filtrar los rangos que no son válidos: mantener solo los rangos válidos y sus correspondientes ángulos
        mask = np.isfinite(ranges)
        
        # Filtrar el array original con la máscara booleana
        ranges_filtered = ranges[mask]
        angles_filtered = self.angles[mask] if self.angles is not None else np.array([])

        if len(ranges_filtered) == 0:
            rospy.logwarn("No hay rangos válidos después de filtrar.")
            return np.array([]), np.array([])

        # Eliminar puntos que están muy cerca de la cámara (umbral de 0.15 metros)
        valid_indices = np.where(ranges_filtered > self.camera_exclusion_radius)
        ranges_filtered = ranges_filtered[valid_indices]
        angles_filtered = angles_filtered[valid_indices]

        # Convertir los rangos válidos en x, y
        x = ranges_filtered * np.cos(angles_filtered)
        y = ranges_filtered * np.sin(angles_filtered)

        # Imprimir los valores de x e y después de aplicar el filtro
        #rospy.loginfo("Valores de x después del filtro: %s", x)
        #rospy.loginfo("Valores de y después del filtro: %s", y)

        if len(x) == 0 or len(y) == 0:
            rospy.logwarn("No hay puntos válidos después de eliminar los cercanos.")

        return x, y


if __name__ == "__main__":
    # Inicializar el nodo
    rospy.init_node('nodo_leer_lidar')

    # Objeto que lee el escaneo
    lidar = Lidar()

    # Declarar del publicador
    topic = 'lidar_xy'
    pub = rospy.Publisher(topic, ArrayXY, queue_size=1)

    # Instancia
    valores_x_y = ArrayXY()

    # Esperar hasta que se reciba el primer mensaje de LiDAR
    rospy.loginfo("Esperando mensajes de LiDAR...")
    while lidar.Scan is None and not rospy.is_shutdown():
        rospy.sleep(0.1)

    if rospy.is_shutdown():
        rospy.loginfo("Nodo terminado antes de recibir mensajes de LiDAR.")
        exit()

    rospy.loginfo("Mensaje de LiDAR recibido. Comenzando el procesamiento...")

    # Tiempo de ejecución del bucle (en Hz)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            # Lectura de los valores x, y
            x, y = lidar.get_xy()

            # Publicar valores filtrados si hay datos válidos
            if x.size > 0 and y.size > 0:
                valores_x_y.x = x
                valores_x_y.y = y
                pub.publish(valores_x_y)

                # Chequear si hay algún obstáculo cerca, excluyendo la cámara
                distances = np.abs(np.sqrt(x**2 + y**2))
                if np.any(distances < lidar.stop_threshold):
                    rospy.loginfo("¡Obstáculo detectado! Deteniéndose.")

            # Esperar
            rate.sleep()
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            rospy.logwarn("ROS time moved backwards. Ignorando y continuando el bucle.")
            continue
