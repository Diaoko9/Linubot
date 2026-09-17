#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from gpiozero import Motor

class LinubotNode(Node):
    def __init__(self):
        super().__init__('linubot_controller')

        # Initialize L293D motors natively with the Enable pins
        # Left Motor (Motor A): IN1=5, IN2=6, ENA=12
        self.left_motor = Motor(forward=5, backward=6, enable=12)

        # Right Motor (Motor B): IN3=23, IN4=24, ENB=13
        self.right_motor = Motor(forward=23, backward=24, enable=13)

        # Subscribe to the PS4 Bluetooth controller topic
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10
        )
        self.get_logger().info("Linubot L293 controller successfully started.")

    def joy_callback(self, msg):
        # Left stick vertical for throttle (Up = 1.0, Down = -1.0)
        # Using index 1 which corresponds to the standard up/down axis
        throttle = msg.axes[1]
        # Left stick horizontal for steering
        # Joystick pushed Left = 1.0, Right = -1.0

        steering = msg.axes[0]
        # Differential drive mixing algorithm
        left_speed = throttle - steering
        right_speed = throttle + steering

        # Normalize speeds to guarantee they stay within the -1.0 to 1.0 PWM limit
        max_speed = max(abs(left_speed), abs(right_speed), 1.0)
        left_speed /= max_speed
        right_speed /= max_speed

        # Apply PWM speed and direction to the left motor
        if left_speed > 0:
            self.left_motor.forward(left_speed)
        elif left_speed < 0:
            self.left_motor.backward(abs(left_speed))
        else:
            self.left_motor.stop()

        # Apply PWM speed and direction to the right motor
        if right_speed > 0:
            self.right_motor.forward(right_speed)
        elif right_speed < 0:
            self.right_motor.backward(abs(right_speed))
        else:
            self.right_motor.stop()

def main(args=None):
    rclpy.init(args=args)
    node = LinubotNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Failsafe: Ensure motors stop when the node is killed
        node.left_motor.stop()
        node.right_motor.stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
