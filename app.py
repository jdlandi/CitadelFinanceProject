# Standard libraries
import os

# Flask-related libraries
from flask import Flask, render_template, request, redirect, make_response
from flask_pymongo import PyMongo

# Local modules
import model
import datatypes

# Initialize Flask app
app = Flask(__name__)

# Check for required environment variables
required_env_vars = ['NEWS_API_KEY', 'OPENAI_API_KEY', 'OPENAI_ORG', 'MONGO_PWD', 'MONGO_USR']
for var in required_env_vars:
    if os.environ.get(var) is None:
        raise Exception(f'Environment variable {var} not found')

# Configure MongoDB
mongo_username = os.environ.get("MONGO_USR")
mongo_password = os.environ.get("MONGO_PWD")
mongo_uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.wohlkjh.mongodb.net/final"
app.config["MONGO_URI"] = mongo_uri
db = PyMongo(app).db


@app.route("/home")
def home():
    """
    Render the home page with the username retrieved from cookies.

    Returns:
        str: Rendered HTML of the home page.
    """
    username = request.cookies.get("username")
    if not username:
        return render_template("index.html")
    return render_template("index.html", user=username)


@app.route("/portfolio", methods=["POST", "GET"])
def portfolio():
    """
    Render the portfolio page. Add a new stock to the user's portfolio if the request method is POST.

    Returns:
        str: Rendered HTML of the portfolio page.
    """
    collection = db.profiles
    username = request.cookies.get("username")
    user_data = collection.find_one({"username": username})
    if not user_data:
        return render_template("portfolio.html", portfolios=[])

    user_portfolios = user_data["portfolios"]

    if request.method == "POST":
        add_stock_to_portfolio(username, user_portfolios, collection)

    return render_template("portfolio.html", portfolios=user_portfolios)


def add_stock_to_portfolio(username, user_portfolios, collection):
    """
    Add a new stock to the user's portfolio.

    Args:
        username (str): The username of the user.
        user_portfolios (list): The user's portfolio data.
    """
    new_stock = request.form["new_stock"]
    ticker = model.ask_ai(new_stock, "stock_input")
    stock_data = [datatypes.gen_stock(ticker)]
    news_data = model.get_search(ticker, 5)
    summary = model.ask_ai(str(news_data), "summ_news")

    new_portfolio = {
        "name": ticker,
        "creation": "4-9-2994",
        "private": True,
        "info": summary,
        "stocks": stock_data
    }

    user_portfolios.append(new_portfolio)
    collection.update_one({"username": username}, {"$set": {"portfolios": user_portfolios}})


@app.route("/news", methods=["POST", "GET"])
def news():
    """
    Render the news page. Display news articles based on the user's query if the request method is POST.

    Returns:
        str: Rendered HTML of the news page.
    """
    username = request.cookies.get("username")
    if request.method == "POST":
        query = request.form["news_query"]
        num_articles = int(request.form["num_articles"])
        news_data = model.get_search(query, num_articles)
        return render_template("news.html", output=news_data, user=username)

    return render_template("news.html", user=username)


@app.route("/currencyConverter", methods=["POST", "GET"])
def currency():
    """
    Render the currency converter page. Display currency conversion results if the request method is POST.

    Returns:
        str: Rendered HTML of the currency converter page.
    """
    username = request.cookies.get("username")
    if request.method == "POST":
        num_currencies = int(request.form["num_currencies"])
        forex_data = datatypes.calculate_forex(datatypes.get_usd_rates(), num_currencies)
        sorted_data = sorted(forex_data, key=lambda pair: pair['final_profit'], reverse=True)
        return render_template("currencyConverter.html", output=sorted_data, lim=num_currencies, user=username)

    return render_template("currencyConverter.html", output=[], lim=0, user=username)


def get_user_flashcards(username):
    collection = db.profiles
    user_data = collection.find_one({"username": username})
    return user_data["flashcards"] if user_data else []


@app.route("/flashcards", methods=["POST", "GET"])
def flashcards():
    """
    Render the flashcards page. Generate an answer for a question if the request method is POST.

    Returns:
        str: Rendered HTML of the flashcards page.
    """
    username = request.cookies.get("username")
    user_flashcards = get_user_flashcards(username)

    if request.method == "POST":
        question = request.form["question"].lower().title()
        answer = model.ask_ai(question, "flashcard")
        return render_template("flashcards.html", input=question, output=answer,
                               flashcards=user_flashcards, user=username)

    return render_template("flashcards.html", flashcards=user_flashcards, user=username)


@app.route("/save", methods=["POST", "GET"])
def save_flashcards():
    """
    Render the flashcards page. Save a new flashcard if the request method is POST.

    Returns:
        str: Rendered HTML of the flashcards page.
    """
    username = request.cookies.get("username")
    user_flashcards = get_user_flashcards(username)

    if request.method == "POST":
        question = request.form["new_term"].lower().title()
        answer = request.form["new_ans"]

        new_flashcard = {
            "topic": question,
            "conversation": [{"author": "user", "content": answer}]
        }
        user_flashcards = [new_flashcard] + user_flashcards
        collection = db.profiles
        collection.update_one({"username": username}, {"$set": {"flashcards": user_flashcards}})

    return render_template("flashcards.html", flashcards=user_flashcards, user=username)


@app.route("/")
@app.route("/signup", methods=["POST", "GET"])
def signup():
    """
    Handle user signup and login.

    Returns:
        str: Rendered HTML of the login page or a redirect to the home page.
    """
    if request.method == "POST":
        collection = db.profiles
        username = request.form['username']
        password = request.form['password']
        verification = datatypes.input_verification(username, password)
        if verification != "OK":
            return render_template("login.html", error=verification)

        if request.form['action'] == "Signup":
            return handle_signup(collection, username, password)
        elif request.form['action'] == 'Login':
            return handle_login(collection, username, password)

    response = make_response(render_template("login.html"))
    response.set_cookie("username", max_age=0)
    response.set_cookie("password", max_age=0)
    return response


def handle_signup(collection, username, password):
    if collection.find_one({"username": username}):
        return render_template("login.html", error="Username already exists")
    new_user = datatypes.gen_new_user(username, datatypes.hash(password))
    collection.insert_one(new_user)
    return redirect_to_home(username, password)


def handle_login(collection, username, password):
    profile = collection.find_one({"username": username})
    if not profile:
        return render_template("login.html", error="Username not found")
    if not datatypes.password_check(password, profile['password']):
        return render_template("login.html", error="Incorrect password")
    return redirect_to_home(username, password)


def redirect_to_home(username, password):
    response = redirect("/home")
    response.set_cookie("username", username)
    response.set_cookie("password", password)
    return response


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Shutdown the server.

    Returns:
        str: A message indicating that the server is shutting down.
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
