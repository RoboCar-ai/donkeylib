from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
import rospy


class RosOdomSubscriber(object):
    '''
    A ROS node to subscribe to a data stream
    '''

    def __init__(self, node_name, channel_name, stream_type=Odometry, anonymous=True):
        self.data = Point()
        rospy.init_node(node_name, anonymous=anonymous)
        self.sub = rospy.Subscriber(channel_name, stream_type, self.on_data_recv)

    def on_data_recv(self, data):
        self.data = data.pose.pose.position

    def run(self):
        return {'x': self.data.x, 'y': self.data.y}
