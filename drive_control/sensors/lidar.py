import logging

from hokuyolx import HokuyoLX

class LiDAR:

    def __init__(self, front_lidar_en = True, front_lidar_addr = ('192.168.0.10', 10940), 
                            rear_lidar_en = True, rear_lidar_addr = ('192.168.0.10', 10940)):

        self.front_lidar_en = front_lidar_en
        self.rear_lidar_en = rear_lidar_en

        if front_lidar_en:
            self.front_lidar = HokuyoLX(addr=front_lidar_addr)
        else:
            self.front_lidar = HokuyoLX(addr=None)

        if rear_lidar_en:
            self.rear_lidar = HokuyoLX(addr=rear_lidar_addr)
        else:
            self.rear_lidar = HokuyoLX(addr=None)

    def close(self):
        if self.front_lidar_en:
            self.front_lidar.close()

        if self.rear_lidar_en:
            self.rear_lidar.close()
