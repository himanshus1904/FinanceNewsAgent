import json
import os
from langchain_huggingface import HuggingFaceEndpoint

class CustomSummarizationTool:
    def __init__(self):

        sec_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        repo_id = "facebook/bart-large-cnn"
        self.model = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=sec_key)

    def summarize(self, articles):

        summarized_articles = []

        for article in articles:
            content = article['news_content']
            if not content:
                continue

            summary = self.model(content, max_length=65, min_length=30, do_sample=False)[0]['summary_text']
            headline = self.model(content, max_length=10, min_length=5, do_sample=False)[0][
                'summary_text'].lower().capitalize()

            summarized_article = {
                "headline": headline,
                "news_content": summary.strip(),
                "image_url": article["image_url"],
                "news_source_url": article["news_source_url"],
                "article_date": article["article_date"]
            }

            summarized_articles.append(summarized_article)

        return summarized_articles


if __name__ == "__main__":
    summarization_tool = CustomSummarizationTool()
    with open('a.json', 'r') as file:
        data = json.load(file)
    summarized_articles = summarization_tool.summarize(data)
    print(summarized_articles)
    with open('b.json','w') as f:
        f.write(json.dumps(summarized_articles))

