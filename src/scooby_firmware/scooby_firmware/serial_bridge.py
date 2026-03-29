import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time

class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        
        # Parametri configurabili
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_separation', 0.2) # Metri (adattare al robot reale)

        port = self.get_parameter('port').value
        baud = self.get_parameter('baudrate').value
        self.wheel_sep = self.get_parameter('wheel_separation').value

        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.get_logger().info(f"Connesso ad Arduino su {port} @ {baud}")
        except Exception as e:
            self.get_logger().error(f"Errore connessione seriale: {e}")
            exit(1)

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)

    def cmd_vel_callback(self, msg):
        # Cinematica differenziale: v = (vr + vl) / 2, w = (vr - vl) / L
        v = msg.linear.x
        w = msg.angular.z

        # Calcolo velocità ruote (m/s)
        vel_l = v - (w * self.wheel_sep / 2.0)
        vel_r = v + (w * self.wheel_sep / 2.0)

        # Mappatura su range PWM (es: -255 a 255)
        # Assumiamo una velocità max di 1.0 m/s -> 255 PWM
        pwm_l = int(max(min(vel_l * 255, 255), -255))
        pwm_r = int(max(min(vel_r * 255, 255), -255))

        # Formato stringa: "L<valore>;R<valore>\n"
        command = f"L{pwm_l};R{pwm_r}\n"
        
        try:
            self.ser.write(command.encode('utf-8'))
        except Exception as e:
            self.get_logger().error(f"Errore invio seriale: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = SerialBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()