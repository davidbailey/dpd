from mesa.datacollection import DataCollector

body_agent_reporters = {"position": "position"}
kinematic_body_agent_reporters = body_agent_reporters | {"velocity": "velocity"}
kinematic_body_with_acceleration_agent_reporters = kinematic_body_agent_reporters | {
    "acceleration": "acceleration"
}
KinematicBodyWithAccelerationDataCollector = DataCollector(
    agent_reporters=kinematic_body_with_acceleration_agent_reporters
)
