from agency_swarm import Agency
from customercare.customer import CustomerCareAgent
from CEO.CEO import CeoAgent
from salesagent.sales import SalesAgent # Assuming file is sales_agent/sales_agent.pyagent import SalesAgent # Assumi ng file is sales_agent/sales_agent.py
from agency_swarm.util.oai import set_openai_key
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
# Load environment variables from .env file
load_dotenv(find_dotenv())
# Set up OpenAI API client
# openai_client = OpenAI(api_key=os.getenv("MY_API_KEY"))

#  Set the OpenAI API Key from your environment variables
set_openai_key(os.getenv("MY_API_KEY"))

#  Instantiate your agents
sales = SalesAgent()  # Assuming file is sales_agent/sales_agent.py)
customer = CustomerCareAgent()  # Assuming file is customer_care/customer_care.pyt()
ceo = CeoAgent()

agency = Agency(
    [
        ceo,  # CEO will be the entry point for communication with the user
        [ceo, customer],  # CEO can initiate communication with Developer
        [ceo, sales],  # CEO can initiate communication with Sales Agent
        [customer, sales],  # Customer Care can communicate with Sales Agent

    ],
    shared_instructions='./agency_manifesto.md'  # shared instructions for all agents
)
agency.run_demo()