from mesa.datacollection import DataCollector

body_agent_reporters = {"position": "position"}
kinematic_body_agent_reporters = body_agent_reporters | {"velocity": "velocity"}
KinematicBodyDataCollector = DataCollector(
    agent_reporters=kinematic_body_agent_reporters
)
