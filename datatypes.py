import os
import requests
import random
from hashlib import sha256
from typing import TypedDict, List, Dict
from datetime import date


class Message(TypedDict):
    author: str
    content: str


class Conversation(TypedDict):
    subject: str
    conversation: List[Message]


class Flashcard(TypedDict):
    topic: str
    conversation: List[Message]


class Stock(TypedDict):
    ticker: str
    orig_price: float
    current_price: float
    price_difference: float
    day_high: float
    day_low: float


class ExchangePair(TypedDict):
    curr_one: str
    curr_two: str
    final_profit: float


class Forex(TypedDict):
    creation: date
    top_pairs: List[ExchangePair]


class Portfolio(TypedDict):
    name: str
    creation: str
    private: bool
    info: str
    stocks: List[Stock]


class User(TypedDict):
    username: str
    password: str
    private: bool
    name: str
    email: str
    location: str
    flashcards: List[Flashcard]
    messages: List[Conversation]
    portfolios: List[Portfolio]
    forexes: List[Forex]
    following: List[str]


def get_usd_rates() -> Dict[str, float]:
    url = 'https://api.exchangerate.host/latest'
    response = requests.get(url)
    data = response.json()
    return data['rates']


def get_conversion(rate1: str, rate2: str) -> float:
    url = f'https://api.exchangerate.host/convert?from={rate1}&to={rate2}'
    response = requests.get(url)
    data = response.json()
    return float(data['result'])


def calculate_forex(data: Dict[str, float], limit: int) -> List[ExchangePair]:
    profits: List[ExchangePair] = []

    for _ in range(limit):
        currency_one, currency_two = random.sample(data.keys(), 2)
        conversion_rate = get_conversion(currency_one, currency_two)
        final_profit = data[currency_one] * conversion_rate / data[currency_two]
        profits.append({
            "curr_one": currency_one,
            "curr_two": currency_two,
            "final_profit": final_profit
        })

    return profits


def password_check(input_pwd: str, hash: str) -> bool:
    return sha256(input_pwd.encode()).hexdigest() == hash


def hash(input_pwd: str) -> str:
    return sha256(input_pwd.encode()).hexdigest()


def input_verification(usr: str, pwd: str) -> str:
    if not usr or len(usr) < 6:
        return "Username must be at least 6 characters"
    if not pwd or len(pwd) < 6:
        return "Password must be at least 6 characters"
    return "OK"


def gen_new_user(usr: str, pwd_hash: str) -> User:
    return {
        "username": usr,
        "password": pwd_hash,
        "name": "",
        "email": "",
        "private": True,
        "location": "",
        "following": [],
        "flashcards": [{"topic": "What Are Different Ways Of Trading", "conversation": [
            {
                "author": "assistant",
                "content": "Some common ways of trading include day trading, swing trading, positional trading, and algorithmic trading."
            }
        ]}, {"topic": "Why Do People Short", "conversation": [
            {
                "author": "assistant",
                "content": "To profit from a decline in the price of an asset, or to hedge against potential losses in a portfolio."
            }
        ]}, {"topic": "What Is Citadel", "conversation": [
            {
                "author": "assistant",
                "content": "Citadel is a global investment firm that manages hedge funds, operates market-making initiatives, and provides other financial services."
            }
        ]}, {"topic": "Can You Explain Equity", "conversation": [
            {
                "author": "assistant",
                "content": "Equity represents ownership in a company, typically in the form of stocks. Higher equity means higher ownership and potential profits."
            }
        ]}, {"topic": "What Is Forex", "conversation": [
            {
                "author": "assistant",
                "content": "Forex refers to the market for trading currencies from around the world. It is short for 'foreign exchange'"
            }
        ]}, {"topic": "What Are Bollinger Bands", "conversation": [
            {
                "author": "assistant",
                "content": "Bollinger Bands are a technical analysis tool used to measure volatility. They consist of a moving average and upper and lower bands."
            }
        ]}
                       ],
        "messages": [],
        "forexes": [],
        "portfolios": [{"name": "AAPL", "creation": "04-01-2023",
                        "private": True,
                        "info": "<ul>\n<li>Investment firm Morgan Stanley raised Apple's price target to $190 based on the expectation of launching a virtual reality and augmented reality headset, which may dramatically expand the market.</li>\n<li>Yahoo Finance provides the latest Apple Inc. (AAPL) stock forecast based on top analysts' estimates, along with other investing and trading data.</li>\n<li>Apple is predicted for a small pullback, featuring a broken-wing butterfly trade that creates a profit zone between $155 and $175.</li>\n<li>Fred Alger Management released its Alger Spectra Fund's Q1 2023 investor letter, in which Apple was discussed for having outperformed in Q1.</li>\n<li>Despite any weakness in the market, holding onto AAPL stock is suggested, and buying at current prices is recommended as well.</li>\n</ul>\n<p>With Morgan Stanley raising its price target on Apple, it indicates that the prediction of an AR/VR headset launching appears to be the basis for this optimism. This product could substantially expand the market for Apple, thereby boosting its financial standing. This could lead to a rise in the company's stock price, causing a potentially profitable opportunity. However, the prediction of a small pullback in Apple's stock price may not affect its performance, given its positive forecast for the future. It is recommended for investors to buy AAPL stock at current prices or even hold onto it despite any existing weakness in the market, as the company has shown solid performance and is likely to outpace other contemporaries in the long run.</p>",
                        "stocks": [{"ticker": "AAPL",
                                    "orig_price": 100, "current_price": 23001,
                                    "price_difference": 100, "day_high": 123212, "day_low": 1234}]}]
    }


def gen_stock(name: str) -> Stock:
    return {
        "ticker": name,
        "orig_price": 1,
        "current_price": 1,
        "price_difference": 1,
        "day_high": 1,
        "day_low": 1
    }
