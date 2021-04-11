#! /usr/bin/python

import rospy
import numpy as np
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point32
from sensor_msgs.msg import PointCloud

class cloud:

	def __init__(self):

		self.sub_laser = rospy.Subscriber(
			"/scan",
			LaserScan,
			callback=self.judge
		)
		self.pub_marker = rospy.Publisher(
			"/mk_array",
			MarkerArray,
			queue_size=5
		)
		
		#self.pub_laser = rospy.Publisher("/scan_c",

	def judge(self,_ls):

		currentRadian=_ls.angle_min
		_angle=_ls.angle_increment

		_mkArray=MarkerArray()

		pc=PointCloud()
		#distance_list=[]
		_dgroup=0.0052 # m
		_dp=6.16/1000
		_points=[]
		_cluster_new=[]
		_cluster_countinue=[]
		
		for i in range(0, len(_ls.ranges)):
			po=Point32()
			_x= _ls.ranges[i] *math.cos(currentRadian)
			
			_y= _ls.ranges[i] *math.sin(currentRadian)

			po.x=_x
			po.y=_y

			#_points.append([po.x,po.y])
			if math.isinf(_x)==True:
				_x=0
			if math.isinf(_y)==True:
				_y=0
			
			self.pc1Callback(po.x,po.y)

			_mkArray.markers.append(self.setMarker((_x,_y),i,2))
			
			currentRadian += _angle
		print(self.pc1Callback())
		self.pub_marker.publish(_mkArray)

	def setMarker(self, _p, _id, _op):
		marker = Marker()
		_length=len(_p)

		marker.header.frame_id = "laser"
		marker.ns = "position"
		marker.id= _id
		marker.lifetime = rospy.Duration.from_sec(0.3)

		marker.type = Marker.SPHERE
		marker.action = Marker.ADD

		marker.pose.position.x = _p[0]
		marker.pose.position.y = _p[1]
		marker.pose.position.z = 0.01
		
		marker.pose.orientation.x = 0.0
		marker.pose.orientation.y = 0.0
		marker.pose.orientation.z = 0.0
		marker.pose.orientation.w = 1.0

		marker.scale.x = 0.02
		marker.scale.y = 0.02
		marker.scale.z = 0.02

		marker.color.r = 0.0
		marker.color.g = 0.0
		marker.color.b = 0.0
		marker.color.a = 1.0
		if _op is 0:
			marker.color.r = 1.0
		elif _op is 1:
			marker.color.g = 1.0
		else:
			marker.color.b = 1.0
			marker.color.g = 0.5
			marker.color.r = 0.5
		return marker

	def pc1Callback(self,_x,_y):
		_points=[]
		_points.append([_x,_y])
		
		return _points
	
		


if __name__ == "__main__":
	rospy.init_node("cluster", anonymous=False)
	cl=cloud()
	rate = rospy.Rate(0.1)
	while not rospy.is_shutdown():
		cl
		rate.sleep()