import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mhatami/Compost-Bin-ROS2/ws/install/ultrasonicSensorPub'
