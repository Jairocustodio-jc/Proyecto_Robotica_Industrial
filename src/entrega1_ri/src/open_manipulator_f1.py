#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState

from markers import *
from functions import *

if __name__ == '__main__':

  rospy.init_node("testForwardKinematics")
  pub = rospy.Publisher('joint_states', JointState, queue_size=1)
  bmarker = BallMarker(color['GREEN'])

  # Nombres de las articulaciones
  jnames = ['joint1', 'joint2', 'joint3', 'joint4']
  # Configuración de las articulaciones
  q = [-0.55, 0.2, 0.15, 0.2]

  # Efector final respecto a la base
  T = fkine_open_manipulator(q)
  print(np.round(T, 3))
  bmarker.position(T)

  # Objeto (mensaje) cuyo tipo es JointState
  jstate = JointState()
  # Asignar valores al mensaje
  jstate.header.stamp = rospy.Time.now()
  jstate.name = jnames
  # Añadir el valor de las articulaciones
  jstate.position = q

  # Frecuencia de lazo (en Hz)
  rate = rospy.Rate(20)
  # Lazo de ejecución continua
  while not rospy.is_shutdown():
    # Tiempo actual (necesario para ROS)
    jstate.header.stamp = rospy.Time.now()
    # Publicar el mensaje
    pub.publish(jstate)
    bmarker.publish()
    # Esperar la siguiente iteración
    rate.sleep()
