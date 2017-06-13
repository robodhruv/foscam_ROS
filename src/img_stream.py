#!/usr/bin/env python

# Script edited for extracting Polaris-H image stream at Orion
# Radiation Measurement Group, University of Michigan


import rospy
import numpy as np
import cv2
import time
import requests
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import urllib

class IP_Cam():

	def __init__(self, url):
		self.stream = requests.get(url, stream=True)
		print "camera initialised"
		self.image_pub = rospy.Publisher("ipcam",Image)
		self.bridge = CvBridge()
		rospy.init_node('image_converter', anonymous=True)
		print "publisher set"

		
	def start(self):
		print "camera stream started"
		
	def run(self):
		bytes=''
		while (1):
			resp = urllib.urlopen(url)
			img = np.asarray(bytearray(resp.read()), dtype="uint8")
			image = cv2.imdecode(image, cv2.IMAGE_COLOR)
			# image_message = cv2_to_imgmsg(img, encoding="passthrough")
			try:
				ros_img = self.bridge.cv2_to_imgmsg(img, "bgr8")
				ros_img.header.stamp = rospy.get_rostime()
				ros_img.header.frame_id = "video_stuff"
				self.image_pub.publish(ros_img)
			except CvBridgeError as e:
				print(e)
			# cv2.imshow('cam',img)
			if cv2.waitKey(1) ==27:
				exit(0)
	
		
if __name__ == "__main__":
	# url = 'http://10.101.202.9:183/videostream.cgi?user=martian_eye&pwd=rover2409'
	url = '192.168.3.26/optical.jpg'
	cam = IP_Cam(url)
	cam.start()
	cam.run()
