from agency_swarm.agents import Agent
from .tools.CustomerTool import CustomerCareTool

class CustomerCareAgent(Agent):
    def __init__(self):
        super().__init__(
            name="customer care",
            description="incharge of answering all customer questions.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CustomerCareTool()],
            tools_folder="customercare/tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        if not message or len(message.strip()) == 0:
            raise ValueError("Received an empty response")
        return message
