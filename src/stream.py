#!/usr/bin/env python

import rospy
import numpy as np
import cv2
import time
import requests
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

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
			bytes+=self.stream.raw.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				jpg = bytes[a:b+2]
				bytes= bytes[b+2:]
				img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
				# image_message = cv2_to_imgmsg(img, encoding="passthrough")
				try:
					self.image_pub.publish(self.bridge.cv2_to_imgmsg(img, encoding="passthrough"))
				except CvBridgeError as e:
					print(e)
				# cv2.imshow('cam',img)
				if cv2.waitKey(1) ==27:
					exit(0)

	
		
if __name__ == "__main__":
	url = 'http://10.101.202.9:183/videostream.cgi?user=martian_eye&pwd=rover2409'
	cam = IP_Cam(url)
	cam.start()
	cam.run()