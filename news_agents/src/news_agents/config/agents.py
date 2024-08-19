import os
from crewai import Agent
import google.generativeai as genai
from news_agents.src.news_agents.tools.finance_news_tool import fetch_news
from news_agents.src.news_agents.tools.summarize_news_tool import summarize
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


news_fetcher = Agent(
    role='News Fetcher',
    goal='Fetch the latest finance-related news articles.',
    tools=[fetch_news],
    backstory=(
        "You are a seasoned journalist with a keen eye for finance news, "
        "and you always ensure that the latest information is brought to light."
    ),
    llm=ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-flash")
)

news_formatter = Agent(
    role='News Formatter',
    goal='Format the fetched news articles according to the given rules using Google Gemini for summarization.',
    tools=[summarize],
    backstory=(
        "You specialize in using cutting-edge AI to generate concise and accurate news summaries "
        "for Indian Finance and Stock Market news. Add the news_source_url and the article date in the json"
    ),
    llm=ChatGoogleGenerativeAI(google_api_key=os.getenv("GOOGLE_API_KEY"), model="gemini-1.5-flash")
)
