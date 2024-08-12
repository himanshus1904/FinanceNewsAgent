from crewai import Task
from agents import *
# Fetch News Task
fetch_news_task = Task(
    description=(
        "Fetch the latest finance-related news articles. "
        "Ensure the articles are relevant to the Indian stock market."
    ),
    expected_output='Raw news articles in JSON format.',
    agent=news_fetcher
)

# Format News Task
format_news_task = Task(
    description=(
        "Format the fetched news articles following these rules: "
        "1. Headline should be short and crisp. "
        "2. Do not add any opinion. "
        "3. Keep the headline in sentence case. "
        "4. Word count of the article should be less than 65 words. "
        "5. The news article should be in past tense and the sentence in present tense. "
        "6. Output only the headline and the news article. "
        "7. The article should not feel like an advertisement."
    ),
    expected_output='30 formatted news articles in JSON format.',
    agent=news_formatter
)
