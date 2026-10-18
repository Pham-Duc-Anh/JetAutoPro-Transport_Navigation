#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

try:
    from servo_controller_msgs.msg import ServosPosition
except ImportError:
    print("Warning: servo_controller_msgs not found, servo translation will not work.")
    ServosPosition = None

class ServoToGazebo(Node):
    def __init__(self):
        super().__init__('servo_to_gazebo')
        
        if ServosPosition is None:
            self.get_logger().error("servo_controller_msgs.msg.ServosPosition not found!")
            return

        self.subscription = self.create_subscription(
            ServosPosition,
            '/servo_controller',
            self.servo_callback,
            10
        )
        
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        self.joint_pubs = {}
        for i in range(1, 6):
            topic = f'/arm/joint{i}/cmd_pos'
            self.joint_pubs[i] = self.create_publisher(Float64, topic, 10)
            
        self.joint_pubs[10] = (
            self.create_publisher(Float64, '/arm/r_joint/cmd_pos', 10),
            self.create_publisher(Float64, '/arm/l_joint/cmd_pos', 10)
        )
        
        # Interpolation states
        self.current_rads = {i: 0.0 for i in range(1, 12)}
        self.target_rads = {i: 0.0 for i in range(1, 12)}
        self.step_rads = {i: 0.0 for i in range(1, 12)}
        
        self.initialized = False
        
        # Mapping from Gazebo joint names to servo IDs
        self.joint_name_to_id = {
            'joint1': 1,
            'joint2': 2,
            'joint3': 3,
            'joint4': 4,
            'joint5': 5,
            'r_joint': 10,
            'l_joint': 10
        }
        
        # Direction signs for servos to match Gazebo URDF physical orientation
        # (Based on manufacturer's PWM poses vs Gazebo joint axes)
        self.joint_signs = {
            1: 1.0,
            2: 1.0,
            3: -1.0,  # Flipped mechanical axis
            4: -1.0,  # Flipped mechanical axis
            5: 1.0,
            10: 1.0
        }
        
        self.pending_msg = None
        
        # 50Hz interpolation timer
        self.timer = self.create_timer(0.02, self.timer_callback)
            
        self.get_logger().info('Servo to Gazebo translator node started with Interpolation. Waiting for /joint_states...')

    def joint_state_callback(self, msg):
        if not self.initialized:
            for name, position in zip(msg.name, msg.position):
                if name in self.joint_name_to_id:
                    servo_id = self.joint_name_to_id[name]
                    self.current_rads[servo_id] = position
                    self.target_rads[servo_id] = position
            self.initialized = True
            self.get_logger().info('Initialized joint states from Gazebo. Ready for /servo_controller commands.')
            if self.pending_msg:
                self.get_logger().info('Processing cached servo command.')
                self.servo_callback(self.pending_msg)
                self.pending_msg = None

    def servo_callback(self, msg):
        if not self.initialized:
            self.get_logger().warn('Received servo command before joint states initialization. Caching.')
            self.pending_msg = msg
            return
            
        duration = msg.duration
        steps = int(duration / 0.02)
        if steps <= 0:
            steps = 1
            
        for servo in msg.position:
            servo_id = servo.id
            pwm = servo.position
            
            # Map pwm to radians (0-1000 corresponds to 0-240 degrees)
            # 240 degrees = 4.18879 radians. 4.18879 / 1000 = 0.004189
            # Apply mechanical mounting sign to match Gazebo URDF
            sign = self.joint_signs.get(servo_id, 1.0)
            target = sign * (pwm - 500) * 0.004189
            
            if servo_id in self.joint_pubs:
                self.target_rads[servo_id] = float(target)
                self.step_rads[servo_id] = (self.target_rads[servo_id] - self.current_rads[servo_id]) / steps

    def timer_callback(self):
        if not self.initialized:
            return
            
        for i, pub in self.joint_pubs.items():
            diff = self.target_rads[i] - self.current_rads[i]
            if abs(diff) > 0.0001:
                # If step is larger than remaining difference, snap to target
                if abs(self.step_rads[i]) >= abs(diff) or self.step_rads[i] == 0:
                    self.current_rads[i] = self.target_rads[i]
                else:
                    self.current_rads[i] += self.step_rads[i]
                
                out_msg = Float64()
                out_msg.data = self.current_rads[i]
                
                if i == 10:
                    pub[0].publish(out_msg)
                    pub[1].publish(out_msg)
                else:
                    pub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ServoToGazebo()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
