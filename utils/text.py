import re

app_name = ''


# Run Model Page Text Elements
run_page_sidebar_title = 'Run Drone Swarm'
run_page_sidebar_description = 'Enter the parameters for the DRL model. Click here to review parameter definitions. '
run_page_map_text = "Select obstacle map"
run_page_agent_slider_text = "Select number of drones in swarm"
run_page_obs_mode_text = "Select observation mode"
run_page_comm_radius_text = "Select drones' communication radius"
run_page_world_size_text = "Select world size for swarm operation"
run_page_obs_mode_dropdown = ['2d_rbf_acc',
                              ' 3d_rbf',
                              ' 2d_rbf_acc_limited',
                              ' 2d_rbf_limited',
                              ' 2d_hist_acc',
                              ' sum_obs_acc',
                              ' sum_obs_acc_full',
                              ' sum_obs_acc_no_vel',
                              ' sum_obs_acc_limited',
                              ' sum_obs',
                              'sum_obs_limited',
                              ' fix_acc']

# Chat Assistant Text Elements
chat_about_assistant = 'Learn more about your assistant'
chat_about_assistant_description = 'Outline of instructions given to assistant'

# Tools Menu Text Elements
tools_menu_map_params_title = 'Map Parameters'
tools_menu_rai_params_title = 'Responsibility Parameters'
tools_menu_swarm_params_title = 'Swarm Parameters'
tools_menu_drl_params_title = 'DRL Parameters'
tools_menu_chat_params_title = 'ChatGPT Parameters'

# Parameter Menu

# About Page Text Elements
about_page_project = "About the project"
about_page_project_description = "This app was developed for GMU's SYST/OR 699 Capstone course. The project's goal was to integrate Explainable AI (XAI) and Responsible AI (RAI) subsystems with a drone swarm DRL. Specifically, the subsystems will be designed to enhance the functionality of the DeepRL for Swarm Systems (DRLSS) model, which is a model that helps drones learn how to work together, with the goal of increasing its ability to provide explainable output and responsible outcomes. "
about_page_model = "About the model"
about_page_model_description = ("This app is running the Deep RL for Drone Swarms codebase written for the paper, 'Deep Reinforcement Learning for Swarm Systems' by M. Hüttenrauch, A. Šošić, and G. Neumann. No changes have been made to the original code. All modifications were applied through wrapper classes. See links below for the authors' paper and GitHub repository.")

# Cleaned error messages
def error_summary(error_message):
    main = re.sub(r'(WARNING|INFO):.*\n?', '', error_message)
    summary = re.findall(r'(Traceback.*|Error.*|Exception.*|TypeError.*|RuntimeError.*)', main, re.DOTALL)
    error_summary = ";\n".join(summary)
    return error_summary