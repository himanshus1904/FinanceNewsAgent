import requests
import json

class FinanceNewsTool:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://newsapi.org/v2/everything"
        self.query_params = {
            "q": "finance",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 50  # Number of articles to fetch
        }

    def fetch_news(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        response = requests.get(self.endpoint, headers=headers, params=self.query_params)

        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get('articles', [])

            # Format the articles into the required structure
            formatted_articles = []
            for article in articles:
                formatted_articles.append({
                    "headline": article.get('title', ''),
                    "news_content": article.get('description', ''),
                    "image_url": article.get('urlToImage', ''),
                    "news_source_url": article.get('url', ''),
                    "article_date": article.get('publishedAt', '')
                })

            return formatted_articles
        else:
            raise Exception(f"Failed to fetch news: {response.status_code} {response.text}")


# Example of using this tool
if __name__ == "__main__":
    api_key = "ee0084f788a14b7684004a0dcb3544e4"  # Replace with your actual NewsAPI key
    news_tool = FinanceNewsTool(api_key=api_key)
    articles = news_tool.fetch_news()
    with open('a.json','w') as f:
        f.write(json.dumps(articles))
