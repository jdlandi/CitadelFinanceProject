# def verify_input():
#     pass

# def create_user(): 
#     return {
#         "username": "",
#         "password": "",
#         "flashcards" : "",
#         "portfolios": ""
#     }

import requests

import openai
openai.organization = "org-XBgyex0IxY9JO9E4jyMua7ZM"
openai.api_key =  "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"
models = openai.Model.list()

def chatgpt(question):
    chat_completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", 
                                                   messages = [{"role":"system", "content":"You are a financial learning assistant. Please answer the following question in 15 words or less. "}, 
                                                               {"role": "user", "content":question}])

    return chat_completion.choices[0].message.content

# print(chatgpt("What is forex?"))


def get_search(query:str, num: int):
  url = 'https://newsapi.org/v2/everything?' + f'q="{query}"&' + 'from=2023-05-20&' + 'sortBy=relevancy&' + f'pageSize={num}&' + 'searchIn=title&' + 'apiKey=20178bc4c5624a8eb12652874011bc05'
  response = requests.get(url).json()
  simple = []
  for article in response["articles"]:
    #print(article)
    simple.append({
      "title": article["title"],
      "description": article['description']
    })
  return simple

#print(get_search("elon", 3))