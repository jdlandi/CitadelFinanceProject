import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import openai
from typing import List, Dict

openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")
models = openai.Model.list()

news_api_key = os.environ.get("NEWS_API_KEY")

prompts = {
    "flashcard": "You are a financial learning assistant charged with the role of providing easy to understand examples to a college level student learning about finance and economics. Please answer the following question with as much brevity as you can while still providing high-quality teaching. MAX 20 WORDS:",
    "analyze_news": "Your job is to analyze the following news regarding a financial object, whether it be a stock, currency, or anything else. Based on the following output, respond ONLY in one of three ways: [bad], [neutral], or [good]. Your response is taking into account the news and whether or not it will increase, decrease, or have no effect on the value of the financial asset. Again, you are only allowed to respond in these three ways and by no means are you allowed to deviate from this rule: [bad], [neutral], or [good]",
    "summ_news": "You are a financial assistant with the task of understanding and summarizing news relating to a certain financial object, such as a stock, currency, or bond. Given the following news articles, respond in an html format highlighting the key points of the news you receive and most importantly, analyze the impact they will have on the market, the financial object itself, and anything else you think may be important. Respond only in the following format: <ul>\n <li> [insert point 1]</li> \n <li> [insert point 2] </li> \n [more <li> elements here as necessary] \n </ul> <p>  [insert analysis here]</p> ",
    "stock_input": "Your role is to do your best to link a company name to it's corresponding finance symbol, for example, you would replace 'apple' with 'AAPL' and 'nvidia geforce' with 'NVDA'. Please keep the format exactly as is. Here is an example input: \"google\". Here is the output: \"GOOG\". Please interpret the following company/stock name into their stock symbol. Return ONLY a single stock symbol:  ",
    "format_currencies": "You will receive a forex rate, that is, a profit between two currencies that can be gained by trading USD to the first currency, the first currency to the second currency, then back to USD. It will look something like: HKD, JEP:1.00000032345. Please format exactly like this [currency1 name]([currency1 Symbol]) -> [currency2 name]([currency2 symbol]) : [rate] . The formatted version of the example input is like so: Hong Kong Dollars(HKD) -> Jersey Pounds(JEP):1.00000032345. Please format the following (or set of following) currencies:"
}


def get_previous_month() -> str:
    """
  Get the date of the previous month in the format "YYYY-MM-DD".

  Returns:
      str: The date of the previous month.
  """
    current_date = datetime.now()
    previous_month = current_date - relativedelta(months=1)
    return previous_month.strftime("%Y-%m-%d")


def ask_ai(question: str, prompt: str) -> str:
    """
  Get a response from the AI model based on the given question and prompt.

  Args:
      question (str): The question to ask the AI model.
      prompt (str): The prompt to use for the AI model.

  Returns:
      str: The AI model's response.
  """
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "system", "content": prompts[prompt]},
                                                             {"role": "user", "content": question}])
    return chat_completion.choices[0].message.content


def get_search(query: str, num: int) -> List[Dict[str, str]]:
    """
  Get a list of news articles based on the given query.

  Args:
      query (str): The query for the news search.
      num (int): The number of articles to retrieve.

  Returns:
      List[Dict[str, str]]: A list of news articles with title, description, and URL.
  """
    curr_month = get_previous_month()
    url = 'https://newsapi.org/v2/everything?' + f'q="{query}"&' + f'from={curr_month}&' + 'sortBy=relevancy&' + f'pageSize={num}&' + 'searchIn=title&' + "language=en&" + f'apiKey={news_api_key}'
    response = requests.get(url).json()

    if "articles" not in response:
        print(f"Error getting news articles: {response.get('message', 'Unknown error')}")
        return []

    articles = [{"title": article["title"],
                 "description": article['description'],
                 "url": article["url"]} for article in response["articles"]]
    return articles
