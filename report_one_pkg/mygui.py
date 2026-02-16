import sys, rclpy, queue, math
from rclpy.node import Node
from rclpy.qos import QoSProfile, qos_profile_sensor_data
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import QThread
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import LaserScan
from report_one_pkg.rpt_ui import Ui_Form
from report_one_interface.srv import MyService
from report_one_interface.action import MyAction

###====================================###
### 스핀을 위한 Thread
###====================================###
class RclpyThread(QThread):
    def __init__(self, executor):
        super().__init__()
        self.executor = executor

    def run(self):
        self.executor.spin()

###====================================###
### GUI
###====================================###
class TurtleMoveGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Node
        self.node = Node('my_gui_node')
        self.qos_profile = QoSProfile(depth=10)
        # Publisher & Subscriber
        self.move_turtle_pub = self.node.create_publisher(Twist, '/cmd_vel', self.qos_profile)
        self.scan_sub = self.node.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile=qos_profile_sensor_data)

        # 변수 초기화
        self.velocity = 0.0
        self.angular = 0.0
        self.max_speed = 2.2
        self.stop_distance = 0.3
        self.scan_ranges = []
        self.has_scan_received = False
        self.is_auto_mode = True
        self.mv_cmd = queue.Queue()
        self.timer = self.node.create_timer(0.2, self.timer_callback)# (0.2초마다 제어 로직 실행)

        # 멀티쓰레드
        self.executor = MultiThreadedExecutor()
        self.executor.add_node(self.node)
        self.ros_thread = RclpyThread(self.executor)
        self.ros_thread.start()

        # 버튼 이벤트
        self.manual_btns = [self.ui.btn_go, self.ui.btn_back, self.ui.btn_right, self.ui.btn_left, self.ui.btn_stop]
        self.ui.btn_go.clicked.connect(self.btn_go_clicked)
        self.ui.btn_back.clicked.connect(self.btn_back_clicked)
        self.ui.btn_left.clicked.connect(self.btn_left_clicked)
        self.ui.btn_right.clicked.connect(self.btn_right_clicked)
        self.ui.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.ui.btn_A.clicked.connect(lambda: self.set_mode(True))
        self.ui.btn_M.clicked.connect(lambda: self.set_mode(False))
        self.set_mode(True)

    def set_mode(self, auto: bool):
        self.is_auto_mode = auto
        self.ui.btn_A.setEnabled(not auto)
        self.ui.btn_M.setEnabled(auto)
        for btn in self.manual_btns:
            btn.setEnabled(not auto)
        if auto:
            self.ui.lb_state.setText("자동 주행 중입니다!")
            self.ui.lb_state.setStyleSheet("color: blue; font-weight: bold;")
            self.ui.list_state.addItem("▶ 자동 주행 모드로 전환합니다.")
        else:
            self.ui.lb_state.setText("수동상태 [Manual]")
            self.ui.lb_state.setStyleSheet("color: green;")
            self.ui.list_state.addItem("수동 모드입니다. 로봇을 움직여주세요.")
        self.ui.list_state.scrollToBottom()
        self.velocity = 0.0
        self.angular = 0.0

    def scan_callback(self, msg):
        self.scan_ranges = msg.ranges
        self.has_scan_received = True

    def turtle_move(self):
        msg = Twist()
        msg.linear.x = self.velocity
        msg.angular.z = self.angular
        self.mv_cmd.put(msg)
        self.ui.list_state.addItem(f'Manual: v={msg.linear.x:.2f}, a={msg.angular.z:.2f}')
        self.ui.list_state.scrollToBottom()

    def btn_go_clicked(self):
        self.velocity += 0.1
        self.turtle_move()

    def btn_back_clicked(self):
        self.velocity -= 0.1
        self.turtle_move()

    def btn_left_clicked(self):
        self.angular += 0.1
        self.turtle_move()

    def btn_right_clicked(self):
        self.angular -= 0.1
        self.turtle_move()

    def btn_stop_clicked(self):
        self.is_auto_mode = False
        self.velocity = 0.0
        self.angular = 0.0
        while not self.mv_cmd.empty():
            try: self.mv_cmd.get_nowait()
            except queue.Empty: break
        stop_msg = Twist()
        self.move_turtle_pub.publish(stop_msg)
        self.ui.list_state.addItem("정지상태입니다.")

    def timer_callback(self):
        # 수동 명령 큐 처리
        manual_mode = False
        while True:
            try:
                msg = self.mv_cmd.get_nowait()
                self.move_turtle_pub.publish(msg)
                manual_mode = True
            except queue.Empty:
                break
        if manual_mode or not self.is_auto_mode or not self.has_scan_received:
            return

        # 자율 주행 로직
        twist = Twist()
        total_len = len(self.scan_ranges)
        left_vals = [v for v in self.scan_ranges[:total_len//4] if math.isfinite(v)]
        right_vals = [v for v in self.scan_ranges[total_len*3//4:] if math.isfinite(v)]
        if not left_vals or not right_vals:
            return
        left_min = min(left_vals)
        right_min = min(right_vals)
        obstacle_distance = min(left_min, right_min)
        if obstacle_distance < self.stop_distance:
            twist.linear.x = 0.0
            twist.angular.z = 0.3 if left_min > right_min else -0.3
        else:
            twist.linear.x = 0.2
            twist.angular.z = 0.0
        self.move_turtle_pub.publish(twist)

def main():
    rclpy.init()
    app = QApplication(sys.argv)
    win = TurtleMoveGUI()
    win.show()
    try:
        sys.exit(app.exec())
    finally:
        win.executor.shutdown()
        win.ros_thread.quit()
        win.ros_thread.wait()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
