#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.publisher_ = self.create_publisher(
            Image,
            'camera/image_raw',
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.bridge = CvBridge()

        # Open default camera (0)
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.get_logger().error('Could not open camera')
            rclpy.shutdown()

        self.get_logger().info('Image publisher started')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('Failed to capture image')
            return

        # Convert OpenCV image to ROS Image message
        msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')

        self.publisher_.publish(msg)
        self.get_logger().debug('Published image frame')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
