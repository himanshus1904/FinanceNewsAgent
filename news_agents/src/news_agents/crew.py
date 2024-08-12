from crewai import Crew, Process
from config.agents import *
from config.tasks import *
import json

# Define the crew with the two agents and tasks
finance_news_crew = Crew(
    agents=[news_fetcher, news_formatter],
    tasks=[fetch_news_task, format_news_task],
    process=Process.sequential
)

# Kickoff the process
if __name__ == "__main__":
    result = finance_news_crew.kickoff()
    with open('formatted_finance_news.json', 'w') as f:
        json.dump(result, f, indent=4)
