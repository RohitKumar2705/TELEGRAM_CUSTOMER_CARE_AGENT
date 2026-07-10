from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from google.adk.agents import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from modules.tools.run_pandas_query_tool import run_pandas_query_tool
from modules.tools.save_order import save_order
from modules.tools.calculate_order_price import calculate_order_price

# AGENT\\\\

def create_agent(df,client) -> tuple[SequentialAgent,Agent,Agent,Agent]:
    PRODUCTS_SCHEMA = """
    products table schema:
    - Product ID: String 
    - Perfume Name: String (Noor Mist, Thuraya Essence, Rihla Oud, Layali, Ameenah Musk, Safa Veil, Hanan Bloom, Taybah Elixir, Rayaheen Aura, Zahrah Veil)
    - Fragrance Notes: String 
    - Type: String 
    - Volume (ml): Integer 
    - Price (PKR): Integer 
    - Stock: Integer 
    - Gender: String (Men, Women, Unisex)
    - Alcohol-Free: String (e.g., Yes, No)
    - Collection: String (e.g., Luxury Oud)
    - Scent Strength: String (e.g., Strong, Medium, Light)
    - Rating: Float (e.g., 3.6)
    """

    query_refiner_agent = Agent(
        name = "query_generator_agent_v1",
        description = "Generates a pandas expression to query a pandas DataFrame based on a user query in plain english.",
        instruction=(
            "You take a user query in plain english and generate a pandas expression to query a pandas DataFrame."
            "Our dataframe is called `df`. Generate query accordingly."
            f"See the schema for reference: {PRODUCTS_SCHEMA}"
            "Your generated pandas expression should be clear and use column names from the given product_schema."
        ),
    )

    query_validator_agent = Agent(
        name="query_validator_agent_v1",
        description="Validates the generated pandas expression to ensure it is correct and can be used to query a pandas DataFrame.",
        instruction=(
            "You take a pandas expression and validate it to ensure it is correct and can be used to query a pandas DataFrame."
            "Use the tool `run_query_from_agent` with argument use_head=True to validate the query."
            "You return True if the query is valid and False if it is not."
        ),
        tools=[run_query_from_agent]
    )

    data_formatter_agent = Agent(
        name="data_formatter_v1",
        model="gemini-2.0-flash-exp",
        description="Executes validated Python expressions on the full DataFrame and formats results for further processing.",
        instruction=(
            "You take a pandas expression and execute it on a pandas DataFrame."
            "Use the tool `run_query_from_agent` with argument use_head=False to execute the query."
        ),
        tools=[run_query_from_agent],
    )
    
    convincing_response_agent = Agent(
        name="convincing_response_v1",
        model="gemini-2.0-flash-exp",
        description="Crafts detailed, persuasive responses for product queries, emphasizing quality and competitive pricing.",
        instruction=(
            "You are a Convincing Response AI for Muallim E-commerce. Your purpose is to take structured JSON data from data_formatter_v1 and craft persuasive, conversational responses as a passionate sales agent. Emphasize the quality, uniqueness, and competitive pricing of the perfumes."
            "Only reflect details from the JSON data. Do not make up any details."
            "DO NOT reply in Markdown."
        ),
    )

    product_query_agent = SequentialAgent(
        name="product_query_agent_v1",
        description="Orchestrates product query processing by sequentially invoking the query refiner, query generator, query validator, data formatter, and convincing response agents.",
        sub_agents=[query_refiner_agent, query_refiner_agent, query_validator_agent, data_formatter_agent, convincing_response_agent],
    )

    return product_query_agent, query_refiner_agent, query_validator_agent, data_formatter_agent
