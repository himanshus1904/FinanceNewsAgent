import os
from crewai import Agent
from news_agents.src.news_agents.tools.finance_news_tool import FinanceNewsTool
from news_agents.src.news_agents.tools.summarize_news_tool import GoogleGeminiTool
from dotenv import load_dotenv
load_dotenv()


# News Fetcher Agent
news_fetcher = Agent(
    role='News Fetcher',
    goal='Fetch the latest finance-related news articles.',
    verbose=True,
    tools=[FinanceNewsTool(api_key=os.getenv("EXO_KEY"))],
    backstory=(
        "You are a seasoned journalist with a keen eye for finance news, "
        "and you always ensure that the latest information is brought to light."
    ),
    llm=None
)

# News Formatter Agent
news_formatter = Agent(
    role='News Formatter',
    goal='Format the fetched news articles according to the given rules using Google Gemini for summarization.',
    verbose=True,
    tools=[GoogleGeminiTool()],
    backstory=(
        "You specialize in using cutting-edge AI to generate concise and accurate news summaries "
        "for Indian Finance and Stock Market news."
    ),
    llm=None
)
