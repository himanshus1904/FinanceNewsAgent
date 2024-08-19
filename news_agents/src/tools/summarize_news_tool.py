import os
import google.generativeai as genai
from langchain.agents import tool
from dotenv import load_dotenv
load_dotenv()


@tool("Summarize")
def summarize(headline_prompt, content_prompt):
    """ Combine the headline and content prompts into one prompt"""

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "You are an Indian Finance and Stock Market News article creator. "
        "Follow the rules:"
        "1. Headline should be short and crisp. "
        "2. Do not add any opinion. "
        "3. Keep the headline in sentence case. "
        "4. Word count of the article should be less than 65 words. "
        "5. The news article should be in past tense and the sentence in present tense. "
        "6. Output only the headline and the news article. "
        "7. The article should not feel like an advertisement."
        "Generate a headline and summarize the following article using the rules:\n\n"
        f"Headline prompt: {headline_prompt}\n\n"
        f"Content prompt: {content_prompt}\n"
    )

    response = model.generate_content(prompt)
    response_text = response.text.strip()
    if "\n" in response_text:
        headline, summary = response_text.split("\n", 1)
    else:
        headline = response_text
        summary = ""

    return headline.strip(), summary.strip(),


