# Project Description
The goal of the XRAI project was to develop a system that implements explainable AI (XAI) and responsible AI (RAI) principles on a deep reinforcement learning model that is designed to control drone swarms. 
We used the pre-existing [Deep RL for Swarm Systems](https://github.com/ALRhub/deep_rl_for_swarms/tree/master) model, and created an RAI wrapper that applied custom environments and responsibility parameters. 

# Repo Description
This repo contains the code for the Dash app that is used as the interface for this [project's API](https://github.com/mklocinski/CapstoneTeamAPI). The app allows users to adjust swarm mission parameters (i.e. number of drones, drone physics, whether to avoid obstacles, minimum buffer distance to obstacles), run-pause-play drone swarm runs to allow for in-depth analysis, review data visualizations, and review all output data from the database in spreadsheet form.

## /assets
The assets directoy holds the CSS files for the app. It also contains the app's data dictionary, which is used to generate hover-over explanations in the app, as well as an inventory of all parameters that the user can adjust, which is used to auto-generate the app's input components.

## /components
The components directory contains the code for all of the major components of the app, including:
- "Chat With Assistant" interface
- Collapsible Sidebar (where user can adjust swarm mission parameters)
- Data Viewer (view swarm mission data from API database)
- NavBar (user can start, pause, then restart swarm mission
- Data Visualization (real-time swarm movements, reward graphs, trajectory graphs)

## /pages
The pages directory contains the code for the pages of the Dash app. 

## /utils
The utils directory contains helper functions for the data visualizations. 
