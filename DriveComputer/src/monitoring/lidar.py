from hokuyolx import HokuyoLX
import numpy as np

track_width = 2.0  # wheel center to center distance of car
forward_constant = 1.0  # multiplier for speed of car, adjust for proper braking distance
car_length = 6.0  # length of car from front to back wheels, center to center

graph = True

if graph:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from matplotlib.patches import Arc


def in_path(points, speed, angle):
    """
    Given an array of x, y points, the speed of the cart, and the front steering angle, returns whether or not the points are in the cart's predicted path.
    :param points: np.ndarray of shape (n, 2) and dtype float64 - Array of x, y data points returned from the LIDAR scanner.
    :param speed: float - Speed of the golf cart
    :param angle: float - Steering angle of the golf cart, in degrees. 0 is straight, positive is left and negative is right
    :return: Boolean - whether there are any data points in the cart's predicted path
    """
    # workaround for angle of 0
    if angle < 1e-4:
        angle = 1e-4

    r_center = car_length * np.tan(np.radians(90 - angle))  # left turn = positive angle

    # transform points to match new origin at turn center
    points[:, 0] += r_center
    points[:, 1] += car_length

    r_cf = np.hypot(r_center, car_length)  # front center radius

    r_left = np.hypot(r_center - track_width / 2, car_length)  # left wheel turn radius
    r_right = np.hypot(r_center + track_width / 2, car_length)  # right wheel turn radius

    y_max = car_length + forward_constant * speed

    # check if y_max is past the turning circle
    y_large = np.minimum(np.fabs(r_left), np.fabs(r_right)) < y_max
    if y_large:
        x_min = r_center - track_width / 2 if angle < 0 else 0
        x_max = r_center + track_width / 2 if angle > 0 else 0
    else:
        x_min = r_center - track_width / 2 if angle < 0 else \
            np.sqrt(
                np.power(r_left, 2) - np.power(y_max, 2)
            )
        x_max = r_center + track_width / 2 if angle > 0 else \
            -np.sqrt(
                np.power(r_right, 2) - np.power(y_max, 2)
            )

    if graph:
        fig, ax = plt.subplots()
        # ax.plot(0, 0, label='Turn Center')
        ax.add_patch(Rectangle((r_center - track_width / 2, 0),
                               track_width, car_length))
        # check if y_max is past the turning circle
        if y_large:
            x1 = np.linspace(r_center - track_width / 2, 0, 100)  # left boundary
            x2 = np.linspace(r_center + track_width / 2, 0, 100)  # right boundary
        else:
            if angle < 0:
                x1 = np.linspace(r_center - track_width / 2,
                                 -np.sqrt(
                                     np.power(r_left, 2) - np.power(y_max, 2)
                                 ),
                                 100)  # left boundary
                x2 = np.linspace(r_center + track_width / 2,
                                 -np.sqrt(
                                     np.power(r_right, 2) - np.power(y_max, 2)
                                 ),
                                 100)  # right boundary
            else:
                x1 = np.linspace(r_center - track_width / 2,
                                 np.sqrt(
                                     np.power(r_left, 2) - np.power(y_max, 2)
                                 ),
                                 100)  # left boundary
                x2 = np.linspace(r_center + track_width / 2,
                                 np.sqrt(
                                     np.power(r_right, 2) - np.power(y_max, 2)
                                 ),
                                 100)  # right boundary
        y1 = np.sqrt(np.power(r_left, 2) - np.power(x1, 2))
        y2 = np.sqrt(np.power(r_right, 2) - np.power(x2, 2))
        ax.plot(x1, y1)
        ax.plot(x2, y2)
        if not y_large:
            if angle < 0:
                ax.plot(
                    (-np.sqrt(np.power(r_left, 2) - np.power(y_max, 2)), -np.sqrt(np.power(r_right, 2) - np.power(y_max, 2))),
                    (y_max, y_max))
            else:
                ax.plot(
                    (np.sqrt(np.power(r_left, 2) - np.power(y_max, 2)), np.sqrt(np.power(r_right, 2) - np.power(y_max, 2))),
                    (y_max, y_max))
        # ax.plot((0, r_center + track_width / 2), (0, 0))
        # ax.plot((0, r_center - track_width / 2), (0, car_length))
        # ax.plot((0, r_center + track_width / 2), (0, car_length))
        # ax.plot((0, r_center), (0, car_length))
        # ax.add_patch(Arc((0, 0), width=r_cf * 2, height=r_cf * 2, theta1=0.0, theta2=90.0))
        ax.scatter(points[:, 0], points[:, 1])
        plt.show()
        # plt.savefig('plt.png')

    # filter points to x range
    points = points[(points[:, 0] <= x_max) & (points[:, 0] >= x_min)]

    # check points
    if angle < 0:
        return np.any(points[
                          (np.hypot(points[:, 0], points[:, 1]) > r_right)
                          &
                          (np.hypot(points[:, 0], points[:, 1]) < r_left)
                          &
                          (points[:, 1] > car_length)
                          &
                          (points[:, 1] < y_max)
                          ])
    else:
        return np.any(points[
                          (np.hypot(points[:, 0], points[:, 1]) < r_right)
                          &
                          (np.hypot(points[:, 0], points[:, 1]) > r_left)
                          &
                          (points[:, 1] > car_length)
                          &
                          (points[:, 1] < y_max)
                          ])

if __name__ == "__main__":
    print(in_path(np.asarray([[2, .5], [1, 1]], dtype=np.float64), 5, 0))