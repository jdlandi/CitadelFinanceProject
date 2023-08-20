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


def gen_stock(name: str) -> Stock:
    return {
        "ticker": name,
        "orig_price": 1,
        "current_price": 1,
        "price_difference": 1,
        "day_high": 1,
        "day_low": 1
    }
