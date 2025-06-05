from agency_swarm.tools import BaseTool
from pydantic import Field, BaseModel
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import instructor
from typing import List
# Load environment variables from .env file
load_dotenv(find_dotenv())
# Set up OpenAI API client

openai_client = instructor.patch(OpenAI(api_key=os.getenv("MY_API_KEY")))  # or use access_token=os.getenv("OPENAI_ACCESS_TOKEN")



# account_id = "MY_ACCOUNT_ID"
# api_key = os.getenv("MY_API_KEY") # or access_token = os.getenv("MY_ACCESS_TOKEN")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------- Pydantic Response Models -------------------

class Decision(BaseModel): 
    action: str = Field(..., description="The CEO will either handle the message internally, forward it to sales, customer care, or request more information.")
    reason: str = Field(..., description="The reason behind the action is dependent on the wordings of the message and the context provided by the user.")

# Example decisions
decisions = [
    Decision(
        action="handle_internally",
        reason="The message concerns strategic business planning about entering a new market, which falls under the CEO's responsibilities."
    ),
    Decision(
        action="request_more_information",
        reason="The user asked about launching a campaign, but did not provide details on the target audience, budget, or timing."
    ),
    Decision(
        action="forward_to_customer_care",
        reason="The user reported that the app crashes after login, which is best handled by customer support."
    ),
    Decision(
        action="forward_to_sales",
        reason="The user requested a custom pricing quote for a large enterprise client, which is within the sales team's domain."
    )
]

class CeoResponse(BaseModel):
    decisions: List[Decision]

# ------------------- CeoTool Implementation -------------------


class CeoTool(BaseTool):
    """
    A tool used by the CEO agent to receive and process a single user message (a_message).
    This message can contain a command, question, or request, and is used to guide downstream logic.
    The CEO agent is responsible for executing tasks that require high-level decision-making and strategic planning.
    It is the point of contact for the Agent and is designed to handle complex operations that may involve multiple steps or require access to external resources.
    The end user interacts with the CEO agent to initiate tasks, and the agent uses its tools to perform these tasks efficiently.
    """

    # Define the fields with descriptions using Pydantic Field
    message: str = Field(
        ..., 
        description="The message or command from the user for the CEO agent to process."
   )

    def run(self):
        try:
            logger.info(f"CEO Agent received message: {self.message}")

            # Use OpenAI to process the message more intelligently
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                    "You are a CEO assistant that decides how to route messages. "
                    "Return a list of decisions. Each decision must contain an 'action' and a 'reason'. "
                    "Possible actions include: 'handle_internally', 'forward_to_sales', "
                    "'forward_to_customer_care', 'request_more_information'."
                       )},
                {"role": "user", "content": self.message}
                ],
                response_model = CeoResponse,  # Specify the response model
            )

            output = []
            for decision in response.decisions:
                logger.info(f"Action: {decision.action}, Reason: {decision.reason}")
                output.append(f"- Action: {decision.action}\n  Reason: {decision.reason}")

            return "\n".join(output)

        except Exception as e:
            logger.error(f"Error in CeoTool: {str(e)}")
            return f"An error occurred while processing the message: {str(e)}"