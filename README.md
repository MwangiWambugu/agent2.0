## Agent.

agents have become on of the leading ways of automation for repetitive tasks in organizations. This specific agent deals with the automation of customer support and sales. it can be customized to fit any kind of automation. 
Limitations: it can only use chatgpt API

### Key Technologies used

1. agency-swarm: this is an open source framework tool used to create the structure of the chatbot. https://agency-swarm.ai/welcome/getting-started/from-scratch

2. python-dotenv:  is used to load environment variables from a .env file into your Python application's environmen

3. openai: This tells OpenAI to follow a schema and return structured JSON automatically parsed into Python objects (like Decision(action, reason)).

4. instructor: for working with structured outputs from large language models. https://github.com/567-labs/instructor

5. pydantic: it is a litrary used for modeling, parsing and validation.

## Starting out

1. Create a python environment
2. Install the agency swarm package. {pip install agency-swarm}
3. Create individual template for the individual agents. {agency-swarm create-agent-template }(You can create as many as you want)
4. Create an agency.py file to import your agents and initialize the Agency class.

## Other information
 Tool.py is the knowledge base of the agent.
 