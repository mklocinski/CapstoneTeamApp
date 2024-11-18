import os
from utils import app_utils


# Default Parameters
model_run_status = {"run-status":"off"}

map_params = app_utils.create_user_inputs("Map")["values"]

rai_params = app_utils.create_user_inputs("RAI")["values"]

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
                "max_kl": 0.02,
                "cg_iters": 10,
                "cg_damping": 0.1,
                "gamma": 0.95,
                "lam": 0.95,
                "vf_iters": 5,
                "vf_stepsize": 0.001,}

chat_params = {"temperature": 0.5}




# Chat Variables
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME", "default-model")