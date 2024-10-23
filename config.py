import os
import openai


# Callbacks

# Default Parameters
model_run_status = {"run-status":"off"}
map_params = {"obstacle1": 2,
              "obstacle2": 1,
              'num_no_fly_zones':3,
              'num_humans':5,
              'num_buildings':5,
              'num_trees':5,
              'num_animals':5}

rai_params = {"basic_collision_avoidance": True,
              "basic_collision_penalty": 10,
              "advanced_collision_avoidance": False,
               "advanced_collision_penalty": 10,
               "basic_damage_avoidance": False,
              "basic_damage_penalty": 10}

environment_params = {"environment_id": 'Rendezvous',
                "nr_agents": 20,
                "obs_mode": "sum_obs_acc",
                "comm_radius": 2,
                "world_size": 100,
                "distance_bins": 8,
                "bearing_bins": 8,
                "torus": False,
                "dynamics": "unicycle_acc"
}

model_params = {"timesteps_per_batch": 10,
                "max_kl": 0.01,
                "cg_iters": 10,
                "cg_damping": 0.1,
                "gamma": 0.99,
                "lam": 0.98,
                "vf_iters": 5,
                "vf_stepsize": 0.001,}

chat_params = {"temperature": 0.5}




# Chat Variables
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME", "default-model")