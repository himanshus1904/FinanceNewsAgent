from crewai import Task
from config.agents import news_fetcher, news_formatter
import requests, json
from bs4 import BeautifulSoup
import streamlit as st

# Fetch News Task
fetch_news_task = Task(
    description=(
        "Fetch the latest finance-related news articles. "
        "Ensure the articles are relevant to the Finance and Indian stock market."
    ),
    expected_output='Raw news articles in JSON format.',
    agent=news_fetcher
)


def format_fetched_news(fetched_articles):
    """Process the fetched articles and format them according to the given rules."""
    formatted_articles = []
    for article in fetched_articles:
        headline_prompt = article.get('headline', '')
        content_prompt = article.get('news_content', '')

        # Use the news_formatter agent to summarize the article
        summarized_headline, summarized_news_content = news_formatter.tools['Summarize'](headline_prompt,
                                                                                         content_prompt)

        # Create the formatted article structure with the desired keys
        formatted_article = {
            "summarized_headline": summarized_headline,
            "summarized_news_content": summarized_news_content,
            "image_url": article.get('image_url', ''),  # Map image URL
            "news_source_url": article.get('news_source_url', ''),  # Map source URL
            "article_date": article.get('article_date', '')  # Map article date
        }
        formatted_articles.append(formatted_article)
    print("***************")
    print(formatted_articles)
    return formatted_articles


format_news_task = Task(
    description=(
        "Format the fetched news articles following these rules: "
        "1. Headline should be short and crisp. "
        "2. Remove any opinion. "
        "3. Keep the headline in sentence case. "
        "4. Word count of the article should be less than 65 words. "
        "5. The news article should be in past tense and the sentence in present tense. "
        "6. Output only the headline and the news article. "
        "7. The article should not feel like an advertisement."
    ),
    expected_output='Formatted news articles in JSON format.',
    agent=news_formatter,
    task_func=format_fetched_news,

)


def image_extractor():
    with open('formatted_finance_news.json', 'r') as file:
        data = json.load(file)
    for entry in data:
        st.write("Entry ", entry)
        url = entry['news_source_url']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        og_images = soup.find_all('meta', property='og:image')
        og_image_urls = [img['content'] for img in og_images]
        entry['img_url'] = og_image_urls
    with open('formatted_finance_news.json', 'w') as file:
        json.dump(data, file, indent=4)
