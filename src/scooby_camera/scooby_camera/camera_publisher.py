#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'scooby/camera/image_raw', 10)
        self.timer = self.create_timer(0.100, self.timer_callback)  
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)
        # Imposta il frame rate a 30 FPS
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not self.cap.isOpened():
            self.get_logger().error('Could not open camera.')
        self.frame_count = 0
        self.last_fps_time = self.get_clock().now().nanoseconds / 1e9

    def timer_callback(self):
        self.get_logger().debug('Timer callback triggered')
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher_.publish(msg)
            self.frame_count += 1
            now = self.get_clock().now().nanoseconds / 1e9
            if now - self.last_fps_time >= 1.0:
                self.get_logger().info(f'FPS: {self.frame_count}')
                self.frame_count = 0
                self.last_fps_time = now
        else:
            self.get_logger().warning('No frame received from camera.')
            # Prova a riaprire la camera se fallisce
            self.cap.release()
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not self.cap.isOpened():
                self.get_logger().error('Could not reopen camera.')

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
