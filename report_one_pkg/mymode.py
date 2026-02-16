import rclpy
from rclpy.node import Node
from report_one_interface.srv import MyService

class ModeService(Node):
    def __init__(self):
        super().__init__('mymode_node')
        self.srv = self.create_service(MyService, 'set_statue', self.callback)
        self.max_speed = 2.2
        self.stop_distance = 0.3

    def callback(self, request, response):
        self.max_speed = request.max_speed
        self.stop_distance = request.stop_distance
        self.get_logger().info(f'Update: speed={self.max_speed}, dist={self.stop_distance}')
        response.success = True
        response.message = "Config Updated"
        return response

def main():
    rclpy.init()
    rclpy.spin(ModeService())
    rclpy.shutdown()
