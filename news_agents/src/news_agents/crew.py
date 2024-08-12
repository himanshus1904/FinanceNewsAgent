from crewai import Agent, Task, Crew, Process
from tools.finance_news_tool import FinanceNewsTool
from tools.summarize_news_tool import CustomSummarizationTool
import os


news_tool = FinanceNewsTool(api_key=os.getenv("news_api_key"))
summarizer_tool = CustomSummarizationTool()

# Define agents
news_researcher = Agent(role='News Researcher', goal='Gather latest finance-related news', tools=[news_tool])
ai_filter = Agent(role='AI Filter', goal='Filter AI-related finance news')
summarizer = Agent(role='Summarizer', goal='Summarize AI finance news', tools=[summarizer_tool])

# Define tasks
collect_news_task = Task(description='Collect finance-related news', agent=news_researcher, tools=[news_tool])
filter_ai_articles_task = Task(description='Filter AI-relevant articles', agent=ai_filter)
summarize_articles_task = Task(description='Summarize articles', agent=summarizer, tools=[summarizer_tool])

# Define crew and process
crew = Crew(agents=[news_researcher, ai_filter, summarizer], tasks=[collect_news_task, filter_ai_articles_task, summarize_articles_task], process=Process.sequential)
result = crew.kickoff(inputs={})
print(result)
