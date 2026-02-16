# moveturtle
로봇 시뮬레이션으로 로봇 움직임을 구현합니다

터틀봇을 제어하는 GUI화면을 구성하고 topic, service, action 기능을 포함한 터틀봇 제어 프로그래밍 구현합니다.

report_one_interface/

├─ action/

│   └─ MoveTurtle.action max_speed= 최대속도, goal_point 충돌감지지점

├─ msg/

├─ srv/

│   └─ MyService.srv stop_distance 충돌감지 인식할 거리

├─ src/

├─ package.xml

└─ CMakeLists.txt

============================

report_one_pkg/

├─ report_one_pkg/

│   └─ guipub.py 속도값을 받고 /cmd_vel 토픽에 전송하는 Publisher

│   └─ mygui.py GUI버튼으로 수동 조종하고, 자동모드 전환시 장애물 감지 및 회피, ROS2와 Qt를 멀티스레드로 동시에 실행

│   └─ mymoving.py 진행률을 보내는 Action 서버

│   └─ mymode.py 속도 및 정지 거리 값을 변경해주는 Service 서버

├─ launch/

│   └─ report.launch.py/ 위 노드들을 한번에 실행하기 위한 설정파일 LAUNCH

├─ package.xml

└─  setup.py

============================

실행 방법
ros2 launch report_one_pkg report.launch.py
