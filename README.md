# moveturtle
로봇 시뮬레이션으로 로봇 움직임을 구현합니다

터틀봇을 제어하는 GUI화면을 구성하고 topic, service, action 기능을 포함한 터틀봇 제어 프로그래밍 구현합니다.

---
기능 설명서

1. 수동 이동 기능
GUI 버튼 입력을 통해 로봇을 수동으로 이동 제어합니다.

입력 : 전진, 후진, 좌회전, 우회전, 정지 버튼

처리 : 버튼을 누르면 /cmd_vel 토픽으로 Twist메세지를 퍼블리시합니다.

출력 : 로봇 이동 명령을 전송합니다.

--

2. 자동 주행 기능
LiDAR 데이터를 기반으로 장애물을 감지하고 회피하며 자율 주행 합니다.

입력 : /scan 토픽 (0.2초 주기)

처리 : 전방 거리를 측정하고, stop_distance로 장애물 존재하는지 판단합니다.
좌우 거리를 비교해 더 넓은 방향으로 회전하고 장애물이 없다면 직진을 유지합니다.

출력 : 
장애물X = 0.2m/s 직진
장애물 O= 회전 명령

--

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
