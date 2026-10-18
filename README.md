# JetAuto Pro - Mô phỏng và Transport Navigation với ROS 2

Hướng dẫn triển khai dự án JetAuto Pro gồm hai phần: chạy mô phỏng trên máy tính và chạy Transport Navigation trên robot thật. Dự án hướng tới điều hướng tự động kết hợp điều khiển tay máy để thực hiện nhiệm vụ vận chuyển vật thể.

---

## Yêu cầu

- Môi trường ROS 2 và các package phụ thuộc đã được cài đặt, build thành công.
- Với mô phỏng: máy tính đã cài các file urdf, mesh, plugin, SLAM và Navigation cần thiết của dự án.
- Với robot thật: JetAuto Pro đã khởi động, kết nối với máy thực thi lệnh; camera, servo và các phần cứng liên quan đã được bật.
- Source môi trường ROS 2 và workspace tương ứng trước khi chạy các lệnh.

Ví dụ, nếu sử dụng workspace `~/jetauto_simulation` trên PC:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/jetauto_simulation/install/setup.bash
```

> Trên robot thật, sử dụng đường dẫn workspace ROS 2 thực tế của robot. Các package `peripherals`, `servo_controller`, `example` phải có sẵn trong môi trường đã source.

---

## Phần 1 - Chạy mô phỏng JetAuto Pro

### Bước 1 - Chuẩn bị môi trường

Mở Terminal trên máy tính và source ROS 2 cùng workspace mô phỏng:

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
source ~/jetauto_simulation/install/setup.bash
```

### Bước 2 - Khởi động mô phỏng và Navigation

Chỉ cần chạy launch Nav2 của dự án:

```bash
ros2 launch jetauto_simulation nav2_launch.xml
```

Sau khi khởi động, quan sát robot trong môi trường mô phỏng và kiểm tra các thành phần Navigation theo giao diện/cấu hình của dự án.


---

## Phần 2 - Chạy Transport Navigation trên robot thật

Thực hiện lần lượt các bước sau. Mỗi lệnh nên chạy trong **một Terminal riêng**; trước mỗi lệnh, source ROS 2 và workspace đã cài các package của JetAuto Pro.

### Bước 1 - Khởi động camera

Mở Terminal thứ nhất trên môi trường robot:

```bash
ros2 launch peripherals usb_cam.launch.py
```

Đảm bảo camera được nhận và node khởi động thành công trước khi chuyển sang bước tiếp theo.

### Bước 2 - Khởi động bộ điều khiển servo

Mở Terminal thứ hai:

```bash
ros2 launch servo_controller servo_controller.launch.py
```

Giữ Terminal này hoạt động để duy trì node điều khiển servo/tay máy.

### Bước 3 - Khởi động node Transport Navigation

Mở Terminal thứ ba:

```bash
ros2 launch example navigation_transport.launch.py
```

Node này thực hiện chức năng Transport Navigation theo cấu hình và mã nguồn được cài trên robot. Quan sát log để xác nhận hệ thống hoạt động; chỉ bắt đầu thử nghiệm khi khu vực xung quanh robot an toàn.

### Thứ tự thực hiện

1. Camera: `peripherals usb_cam.launch.py`
2. Servo: `servo_controller servo_controller.launch.py`
3. Transport Navigation: `example navigation_transport.launch.py`

> Các lệnh trên là quy trình chạy **robot thật**, khác với launch mô phỏng ở Phần 1. Không cần chạy các launch của mô phỏng Gazebo trong quy trình này, trừ khi cấu hình hệ thống của bạn có yêu cầu riêng.

---

## Kết quả thử nghiệm

Thực hiện **10 lần kiểm thử** khả năng tự hành, tránh vật cản và kích hoạt tay máy gắp vật; hệ thống thành công **5/10 lần** trong các điều kiện: dữ liệu odometry và laser scan đáp ứng tần số cần thiết, sàn không trơn trượt, ảnh camera không bị trễ và CPU của Jetson Nano không bị quá tải.

Kết quả phản ánh các lần thử nghiệm đã thực hiện, không phải tỷ lệ thành công bảo đảm trong mọi điều kiện.

---

## Cấu trúc package mô phỏng

```text
jetauto_simulation/
├── bridge_config/
├── launch/
├── map/
├── meshes/
├── params/
├── plugin/
├── rviz_config/
├── transport_navigation/
├── urdf/
├── worlds/
├── CMakeLists.txt
└── package.xml
```

- `launch/`: các file launch của package mô phỏng.
- `urdf/`, `meshes/`: mô hình và cấu trúc robot.
- `worlds/`: môi trường mô phỏng.
- `map/`, `params/`: bản đồ và cấu hình.
- `transport_navigation/`: thành phần liên quan đến nhiệm vụ vận chuyển trong dự án.

---

## Video Demo

[![JetAuto Pro - Transport Navigation Demo](https://img.youtube.com/vi/KxRJGK9Ayho/0.jpg)](https://www.youtube.com/shorts/KxRJGK9Ayho)

