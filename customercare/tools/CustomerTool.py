from agency_swarm.tools import BaseTool
from pydantic import Field, BaseModel
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import instructor
# Load environment variables from .env file
load_dotenv(find_dotenv())
# Set up OpenAI API client
openai_client = instructor.patch(OpenAI(api_key=os.getenv("MY_API_KEY")))  # or use access_token=os.getenv("OPENAI_ACCESS_TOKEN")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# account_id = "MY_ACCOUNT_ID"
# api_key = os.getenv("MY_API_KEY") # or access_token = os.getenv("MY_ACCESS_TOKEN")

# Define structured response model
class RoutingDecision(BaseModel):
    action: str = Field(..., description="The action to take based on the customer's message. Options include 'forward_to_sales' or 'handle_by_customer_care'.")
    reason: str = Field(..., description="The reason for this decision is based on the content of the customer's message, such as whether it relates to sales or customer care issues.")

# ------------------- CustomerCareTool Implementation -------------------
class CustomerCareTool(BaseTool):
    """
    A tool used by the Customer Care Agent to respond to customer support questions.
    If a question is determined to be sales-related (e.g., pricing, purchasing, product details),
    the tool will suggest routing the request to the Sales Agent.
    This helps the agent provide accurate support and escalate appropriately.
    """

    customer_message: str = Field(
        ..., description="The question or issue raised by the customer that needs a response or solution."
    )

    def run(self):
        try:
            logger.info(f"Customer message received: {self.customer_message}")

            # Use OpenAI's model to determine routing
            decision: RoutingDecision = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful customer care assistant. "
                            "Classify the customer's message and return your decision in a structured format. "
                            "If it relates to pricing, subscriptions, or purchasing, choose 'forward_to_sales'. "
                            "Otherwise, choose 'handle_by_customer_care'."
                        )
                    },
                    {"role": "user", "content": self.customer_message}
                ],
                response_model=RoutingDecision
            )

            logger.info(f"Action: {decision.action} | Reason: {decision.reason}")
            return f"Action: {decision.action}\nReason: {decision.reason}"

        except Exception as e:
            logger.error(f"Error in CustomerCareTool: {str(e)}")
            return f"An error occurred while processing the message: {str(e)}"