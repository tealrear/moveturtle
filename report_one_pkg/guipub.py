import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class GuiPublisher(Node):
    def __init__(self):
        super().__init__('guipub_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def publish_move(self, v, a):
        msg = Twist()
        msg.linear.x = v
        msg.angular.z = a
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: v={v}, a={a}')
