import streamlit as st
from crewai import Crew, Process
from config.agents import news_fetcher, news_formatter
from config.tasks import fetch_news_task, format_news_task, image_extractor
import json
import requests
from bs4 import BeautifulSoup

# Define the crew with the two agents and tasks
finance_news_crew = Crew(
    agents=[news_fetcher, news_formatter],
    tasks=[fetch_news_task, format_news_task],
    process=Process.sequential
)


def generate_finance_news():
    # Run the process
    result = finance_news_crew.kickoff()
    raw_data = result.raw  # Access the raw attribute directly

    try:
        parts = raw_data.split("```json", 1)
        formatted_string = parts[1].strip()[:-3]
        print(formatted_string)
        data = json.loads(formatted_string)
    except (IndexError, json.JSONDecodeError) as e:
        st.error(f"Error processing data: {str(e)}")
        return None
    print("Done")
    # Save the result to a JSON file
    with open('formatted_finance_news.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Extract images using the image_extractor function
    image_extractor()  # This function will update the JSON with image URLs

    # Reload the updated JSON to display
    with open('formatted_finance_news.json', 'r') as f:
        updated_data = json.load(f)

    return updated_data  # Return the updated JSON data to display in the Streamlit interface


if __name__ == '__main__':
    st.title("Finance News Generator")
    st.write("""
    Click the button below to generate the latest finance news. 
    The result will be saved in a JSON file and displayed below.
    """)

    # Button to generate finance news
    if st.button("Generate Finance News"):
        news_data = generate_finance_news()

        if news_data:
            st.write("Formatted Finance News:")
            st.json(news_data)  # Display the JSON data

            for entry in news_data:
                if 'img_url' in entry:
                    for img_url in entry['img_url']:
                        st.image(img_url, use_column_width=True)
