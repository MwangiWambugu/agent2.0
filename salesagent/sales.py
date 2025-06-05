from agency_swarm.agents import Agent
from .tools.salesagentTool import CustomerCareTool, SalesAgentTool

class SalesAgent(Agent):
    def __init__(self):
        super().__init__(
            name="sales agent",
            description="incharge of selling products to the clients.",
            instructions="./instructions.md",
            files_folder="./files",
            schemas_folder="./schemas",
            tools=[SalesAgentTool()],
            tools_folder="salesagent/tools",
            temperature=0.3,
            max_prompt_tokens=25000,
        )

    def response_validator(self, message):
        if not message or not message.strip():
            raise ValueError("Received empty response.")
        return message