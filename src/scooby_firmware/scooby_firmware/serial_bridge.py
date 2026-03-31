import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
MAX_PWM = 175


class SerialBridge(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_separation', 0.2)  # metri
        self.declare_parameter('max_speed', 1.0)  # m/s

        port = self.get_parameter('port').value
        baud = self.get_parameter('baudrate').value
        self.wheel_sep = self.get_parameter('wheel_separation').value
        self.max_speed = self.get_parameter('max_speed').value

        try:
            self.ser = serial.Serial(port, baud, timeout=0.1)
            self.get_logger().info(f"Connesso a {port} @ {baud}")
        except Exception as e:
            self.get_logger().error(f"Errore apertura seriale: {e}")
            self.ser = None

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)

    def cmd_vel_callback(self, msg):
        if not self.ser or not self.ser.is_open:
            self.get_logger().error("Seriale non disponibile!")
            return
        v = msg.linear.x
        w = msg.angular.z
        # Cinematica differenziale: v = (vr + vl)/2, w = (vr - vl)/L
        # Ricavo vr e vl
        vr = v - (3*w * self.wheel_sep)
        vl = v + (3*w * self.wheel_sep)
        # Mappatura PWM [-255, 255] rispetto a max_speed
        pwm_r = int(max(min(vr / self.max_speed * MAX_PWM, MAX_PWM), -MAX_PWM))
        pwm_l = int(max(min(vl / self.max_speed * MAX_PWM, MAX_PWM), -MAX_PWM))
        command = f"L{pwm_l};R{pwm_r}\n"
        self.get_logger().info(f"Comando seriale inviato: {command.strip()}")
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
