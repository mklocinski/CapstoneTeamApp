import pandas as pd
from scikit.manifold import MDS
import warnings

warnings.filterwarnings("ignore")


def get_drone_data(json, num_drones):
    steps = [l['step'] for l in json]
    pos = [l['distance_matrix'] for l in json]
    reward = [l['reward'] for l in json]

    steps = []
    drone = []
    x_coor = []
    y_coor = []
    rewards = []
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
    for i in range(0, len(json)):
        steps.extend(num_drones * [json[i]['step']])
        drone.extend(["Drone " + str(d) for d in range(1, num_drones + 1)])
        coordinates = mds.fit_transform(json[i]['distance_matrix'])
        for c in coordinates:
            x_coor.append(c[0])
            y_coor.append(c[1])
        for r in json[i]['reward']:
            rewards.append(r)

    viz_df = pd.DataFrame({'Step': steps,
                           'Drone': drone,
                           'X': x_coor,
                           'Y': y_coor,
                           'Reward': rewards
                           })

    return viz_df