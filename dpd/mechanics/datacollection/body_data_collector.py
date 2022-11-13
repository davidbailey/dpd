from mesa.datacollection import DataCollector

body_agent_reporters = {"position": "position"}
BodyDataCollector = DataCollector(agent_reporters=body_agent_reporters)
