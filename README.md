# moveturtle
로봇 시뮬레이션으로 로봇 움직임을 구현합니다

터틀봇을 제어하는 GUI화면을 구성하고 topic, service, action 기능을 포함한 터틀봇 제어 프로그래밍 구현합니다.

기능
- 버튼 기반으로 수동 이동이 가능합니다
- LiDAR기반 자율 주행을 합니다
- /cmd_vel 퍼블리시하고 /scan 구독하는 기능을 구현했습니다.

자동모드에선 0.2초 주기로 인식합니다.
장애물을 감지하고 장애물 좌우 거리를 인식하여 시야가 확보가 더 잘되는 방향으로 회전합니다.
장애물이 없는 경우 0.2m/s 속도로 직진합니다.

msx_speed를 통해 속도 변경이 가능하고
stop_distance를 통해 정지거리 변경이 가능합니다.

| 구분      | 이름          | 타입        | 설명        |
| ------- | ----------- | --------- | --------- |
| Topic   | /cmd_vel    | Twist     | 이동 명령     |
| Topic   | /scan       | LaserScan | LiDAR 데이터 |
| Service | set_statue  | MyService | 설정 변경     |
| Action  | move_target | MyAction  | 목표 이동     |



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
