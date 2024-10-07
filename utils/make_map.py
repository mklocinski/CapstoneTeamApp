import numpy as np
import pandas as pd
import random



class Map:
    def __init__(self, world_size=100):
        self.world_size = world_size
        self.axis_values = [-self.world_size, self.world_size]
        self.position_matrix = None
        self.position_df = None

    def initialize(self, num_obstacles):

        # Point transformations to create adjacent zone
        adjacent_zone = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        limits = (0, 2*self.world_size)

        # Initialize map of random obstacles
        init_pos = random.sample(range(2*self.world_size * 2*self.world_size), num_obstacles)
        init_pos_matrix = np.array([1.0 if i in init_pos else 0.0 for i in range(2*self.world_size * 2*self.world_size)])
        self.position_matrix = init_pos_matrix.reshape(2*self.world_size, 2*self.world_size)

        # Add adjacent zone around obstacles
        rows, cols = np.where(self.position_matrix == 1)
        obstacle_coords = list(zip(rows, cols))

        for obstacle in obstacle_coords:
            point_trans = [(obstacle[0] + i[0], obstacle[1] + i[1]) for i in adjacent_zone]
            for point in point_trans:
                if point[0] >= limits[0] - 1 and point[0] <= limits[1] - 1 and point[1] >= limits[0] - 1 and point[1] <= \
                        limits[1] - 1:
                    self.position_matrix[point[0], point[1]] = 0.5

    def add_single_point_obstacle(self, x, y):

        # Point transformations to create adjacent zone
        adjacent_zone = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        limits = (0, self.ops_space[0])

        # Add obstacle
        self.position_matrix[x, y] = 1

        # Add adjacent zone
        point_trans = [(x + i[0], y + i[1]) for i in adjacent_zone]

        for point in point_trans:
            if point[0] >= limits[0] and point[0] <= limits[1] and point[1] >= limits[0] and point[1] <= limits[1]:
                self.position_matrix[point[0], point[1]] = 0.5

    def create_map_dataframe(self):
        x, y = np.meshgrid(np.arange(self.position_matrix.shape[1]), np.arange(self.position_matrix.shape[0]))
        self.position_df = pd.DataFrame({'X': x.ravel(),
                                         'Y': y.ravel(),
                                         'Value': self.position_matrix.ravel()})