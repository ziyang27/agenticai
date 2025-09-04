import os
from strands import Agent
from strands.models import BedrockModel
from dotenv import load_dotenv
import boto3

load_dotenv(".env")

class BudgetBuddyAgent:
    """
    A simple agentic AI financial coach that creates personalized savings plans.
    """
    def __init__(self):
        # Initialize the Bedrock client and provider with environment variables
        self.session = boto3.Session(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),      # Changed
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), # Changed
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bedrock_runtime = self.session.client('bedrock-runtime')

        self.model_provider = BedrockModel(
            client=self.bedrock_runtime,
            model_id=os.getenv('BEDROCK_MODEL_ID', 'aanthropic.claude-3-5-haiku-20241022-v1:0')  # Changed
        )

        # Define the agent's personality and goal
        self.system_prompt = """You are BudgetBuddy Pro, a comprehensive financial advisor. Provide detailed, personalized financial advice including:

        1. Savings optimization strategies
        2. Expense reduction techniques  
        3. Investment recommendations based on risk profile
        4. Retirement planning insights
        5. Risk assessment and warnings
        6. Actionable steps for improvement

        Be specific, practical, and supportive. Use financial data to provide quantitative recommendations.
        """

        # Create the agent with access to its tools
        self.agent = Agent(
            model=self.model_provider,
            system_prompt=self.system_prompt
        )

    def run(self, user_input: str) -> str:
        response = self.agent(user_input)
        return response