import requests
import json
from datetime import datetime


class FinanceNewsTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.exa.ai/search"
        self.query = "Indian News Related to Stock Market and Finance"
        self.start_published_date = "2024-08-12"
        #self.start_published_date = datetime.now().strftime("%Y-%m-%d")  # The start date for published news

    def fetch_news(self):
        # Prepare the data payload for the Exo API request
        data = {
            "startPublishedDate": self.start_published_date,
            "query": self.query,
            "type": "neural",
            "useAutoprompt": True,
            "numResults": 10,
            "endPublishedDate": self.start_published_date,
            "excludeDomains": ["x.com", "twitter.com"],
            "contents": {
              "text": True
        }
        }

        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-api-key': self.api_key
        }

        # Sending the POST request to the Exo API
        response = requests.post(self.endpoint, headers=headers, json=data)

        if response.status_code == 200:
            output_data = response.json()
            articles = output_data.get('results', [])

            # Format the articles into the required structure
            formatted_articles = []
            for article in articles:
                print(article)
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


if __name__ == "__main__":
    api_key = "475aa0b2-827d-40fd-8f76-5cd8b3311935"  # Replace with your actual Exo API key
    news_tool = FinanceNewsTool(api_key=api_key)
    articles = news_tool.fetch_news()
    with open('exo_news.json', 'w') as f:
        json.dump(articles, f, indent=4)
