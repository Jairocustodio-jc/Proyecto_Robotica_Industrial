import rospy
from open_manipulator_msgs.srv import SetJointPosition, SetJointPositionRequest
from sensor_msgs.msg import JointState
import numpy as np
from copy import copy

cos = np.cos
sin = np.sin
pi = np.pi

# Funciones de Cinemática
def dh(d, theta, a, alpha):
    cth = cos(theta)
    sth = sin(theta)
    ca = cos(alpha)
    sa = sin(alpha)
    T = np.array([[cth, -ca * sth, sa * sth, a * cth],
                  [sth, ca * cth, -sa * cth, a * sth],
                  [0, sa, ca, d],
                  [0, 0, 0, 1]])
    return T

def fkine_open_manipulator(q):
    beta = 11 * pi / 180
    T1 = dh(0.077, q[0] + pi, 0, pi / 2)
    T2 = dh(0, q[1] + pi / 2 + beta, 0.13, 0)
    T3 = dh(0, q[2] + pi / 2 - beta, 0.124, 0)
    T4 = dh(0, q[3], 0.126, 0)
    T = T1.dot(T2).dot(T3).dot(T4)
    return T

def jacobian_open_manipulator(q, delta=0.0001):
    J = np.zeros((3, 4))
    T = fkine_open_manipulator(q)
    for i in range(4):
        dq = copy(q)
        dq[i] += delta
        dT = fkine_open_manipulator(dq)
        J[0, i] = (dT[0, 3] - T[0, 3]) / delta
        J[1, i] = (dT[1, 3] - T[1, 3]) / delta
        J[2, i] = (dT[2, 3] - T[2, 3]) / delta
    return J

def ik_gradient_open_manipulator(xdes, q0, fixed_joint_index=None, fixed_joint_value=None):
    epsilon = 0.001
    max_iter = 1000
    delta = 0.00001
    alfa = 0.5
    q = copy(q0)
    for i in range(max_iter):
        if fixed_joint_index is not None:
            q[fixed_joint_index] = fixed_joint_value

        J = jacobian_open_manipulator(q, delta)
        T = fkine_open_manipulator(q)
        f = T[0:3, 3]
        e = xdes - f

        q = q + alfa * np.dot(J.T, e)
        
        if np.linalg.norm(e) < epsilon:
            break
    return q