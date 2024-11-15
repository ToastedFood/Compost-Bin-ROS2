from serial.tools import list_ports
import serial
import csv
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.serial_port = serial.Serial(getPort( 0x2341, 0x0043), 9600, timeout=1)
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.csv_writer = csv.DictWriter(open("sensorInfo.csv", "w"), fieldnames=["AnalogReadValue"])
        self.csv_writer.writeheader()


    def timer_callback(self):
        line = self.serial_port.readline().decode('utf-8').rstrip()
        # Process line and publish
        msg = String()
        msg.data = line  # or process as needed
        self.publisher_.publish(msg)
        self.get_logger().info(f'{line}')
        self.csv_writer.writerow({"AnalogReadValue": line})


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

def getPort(vid, pid) -> str:
    device_list = list_ports.comports()
    for device in device_list:
        print(device.serial_number)
        if device.vid == vid and device.pid == pid:
            return device.device
    raise OSError('Device not found')


if __name__ == '__main__':
    main()