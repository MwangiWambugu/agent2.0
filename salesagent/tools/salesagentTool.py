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
# api_key = os.getenv("MY_API_KEY")  # or access_token = os.getenv("MY_ACCESS_TOKEN")

class SalesDecision(BaseModel):
    action: str = Field(..., description="The action is based on the sales inquiry, such as 'respond_with_sales_info' or 'forward_to_customer_care'.")
    reason: str = Field(..., description="The reason for the action is determined by the content of the sales message, such as whether it relates to product information or a support issue.")
    response: str = Field(..., description="The response to the sales inquiry, which may include product information or a suggestion to contact customer care for support-related issues.")

# --- Simulated Customer Care Tool ---
class CustomerCareTool(BaseTool):
    """
    A tool used by the Customer Care Agent to handle customer service issues forwarded by the Sales Agent.
    """

    customer_care_message: str = Field(
        ..., description="A support-related question forwarded to Customer Care."
    )

    def run(self):
        # Simulate customer care logic
        return f"Customer Care Response: Thank you for reaching out. We will assist you with: '{self.customer_care_message}'"

# --- Sales Agent Tool ---
class SalesAgentTool(BaseTool):
    """
    A tool used by the Sales Agent to handle all sales inquiries.
    This includes answering product questions, initiating a sale,
    and forwarding support-related issues to the Customer Care Agent.
    """

    sales_message: str = Field(
        ..., description="The customer's sales inquiry or product-related question."
    )

    def run(self):
        logger.info("CustomerCareTool running...")

        try:
            decision = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": ("You are a helpful assistant. Classify the message and respond.\n"
                            "- If it's about buying or product info, respond as sales.\n"
                            "- If it's about a technical/support issue, suggest forwarding to customer care.\n"
                            "Return an 'action' and a 'response'."
                            )
                    },
                    {"role": "user", "content": self.sales_message}
                ],
                response_model = SalesDecision
            )
            logger.info(f"Sales decision: {decision.action} | Response: {decision.response}")

            if decision.action == "forward_to_customer_care":
                care_tool = CustomerCareTool(customer_care_message=self.sales_message)
                return f"[Forwarded to Customer Care]\n{care_tool.run()}"
            else:
                return f"[Sales Response]\n{decision.response}"

        except Exception as e:
            logger.error(f"Error in SalesAgentTool: {e}")
            return "An error occurred while processing the sales message."

