BODY_AGENT_REPORTERS = {"position": "position"}
KINEMATIC_BODY_AGENT_REPORTERS = BODY_AGENT_REPORTERS | {"velocity": "velocity"}
KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS = KINEMATIC_BODY_AGENT_REPORTERS | {
    "acceleration": "acceleration"
}
DYNAMIC_BODY_AGENT_REPORTERS = KINEMATIC_BODY_WITH_ACCELERATION_AGENT_REPORTERS | {}