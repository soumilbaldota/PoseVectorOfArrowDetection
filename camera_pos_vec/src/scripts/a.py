#!/usr/bin/env python3
import yaml
import numpy as np
import cv2
import rospy
from std_msgs.msg import Float32MultiArray

def callback(data):

    filepath="/home/soumil/catkin_ws/src/camera_pos_vec/src/scripts"
    filename="untitled"
    camera_parameters=open(f"{filepath+'/'+filename}.yaml")
    camera_parameters=yaml.load(camera_parameters,Loader=yaml.FullLoader)
    camera_matrix=camera_parameters['camera_matrix']
    camera_matrix=np.array(camera_matrix['data'])
    camera_matrix=np.reshape(camera_matrix,(3,3))
    distortion_coefficients=camera_parameters['distortion_coefficients']

    distortion_coefficients=np.array(distortion_coefficients['data'])
    object_points= np.array([(-150.0,100.0,0.0),(150.0,100.0,0.0),(150.0,-100.0,0.0),(-150.0,-100,0.0)])
    # image_points=np.array()#get from ros
    image_points=np.array(data.data)
    image_points=np.array((
        (image_points[0],image_points[1]),
        (image_points[2],image_points[1]),
        (image_points[2],image_points[3]),
        (image_points[0],image_points[3]),
        )
    )
    print(type(image_points[0][0]))
    success,rotation_vector,translation_vector=cv2.solvePnP(
    	object_points,
    	image_points,
    	camera_matrix,
    	distortion_coefficients,
      flags=cv2.SOLVEPNP_IPPE
    	)
    print ("translation_vector = ",translation_vector)
    print ("rotation_vector = ",rotation_vector)


def listener():
  rospy.init_node('pos_vector_calc', anonymous=True)
  rospy.Subscriber('yolo_xyxy', Float32MultiArray, callback)
  rospy.spin()

if __name__ == '__main__':
    listener()