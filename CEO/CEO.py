from agency_swarm.agents import Agent
from .tools.CEOTool import CeoTool

class CeoAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEO",
            description="an agent that is in charge of the other bots. The CEO receives instructions and gives to the other bots",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[CeoTool()],
            tools_folder="CEO/tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )
    def response_validator(self, message):
        if not message or len(message.strip()) == 0:
            raise ValueError("Empty response received")
        return message