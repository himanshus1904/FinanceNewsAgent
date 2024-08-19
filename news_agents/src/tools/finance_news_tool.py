import os
import requests
import json
from datetime import datetime
from langchain.agents import tool
from dotenv import load_dotenv
import streamlit as st
load_dotenv()


@tool("Fetch relevant news")
def fetch_news():
    """Prepare the data payload for the Exo API request"""
    api_key = os.getenv("EXO_KEY")
    endpoint = "https://api.exa.ai/search"
    query = "Indian News Related to Stock Markets and Finance"
    # start_published_date = "2024-08-12"
    start_published_date = datetime.now().strftime("%Y-%m-%d")  # The start date for published news

    data = {
        "startPublishedDate": start_published_date,
        "query": query,
        "type": "neural",
        "useAutoprompt": True,
        "numResults": 10,
        "endPublishedDate": start_published_date,
        "includeDomains": ["rediff.com", "moneycontrol.com", "reuters.com", "www.cnbc.com", "www.businesstoday.in", "www.livemint.com", "economictimes.indiatimes.com"],
        "contents": {
          "text": True
    }
    }

    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'x-api-key': api_key
    }
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        output_data = response.json()
        articles = output_data.get('results', [])

        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                "headline": article.get('title', ''),
                "news_content": article.get('text', ''),
                "image_url": article.get('image_url', ''),
                "news_source_url": article.get('url', ''),
                "article_date": article.get('publishedDate', '')
            })
        return formatted_articles
    else:
        raise Exception(f"Failed to fetch news: {response.status_code} {response.text}")


