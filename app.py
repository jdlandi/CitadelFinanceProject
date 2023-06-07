# -- Import section --
from flask import Flask
from flask import render_template, request, redirect, make_response
from pymongo import MongoClient

import model
import datatypes


# -- INITIALIZE APP --
app = Flask(__name__)

# CONFIGURE MONGO DB
# create the clent
username = "final"
password = "1BB8jrqKVpLOOYFH"
url = f"mongodb+srv://{username}:{password}@cluster0.wohlkjh.mongodb.net/"
client = MongoClient(url)

# our database manager object
db = client["final"]

# HOME PAGE
@app.route("/home")
def dashboard():
  collection = db.profiles
  events = collection.find({})
  return render_template("index.html", events=events)

#news
@app.route("/news", methods=["POST", "GET"])
def news():
  if request.method == "POST":
    query = request.form["news_query"]
    num = request.form["num_articles"]
    out = model.get_search(query, num)
    return render_template("news.html", output = out)
  else:
    return render_template("news.html")


#currencyConverter
@app.route("/currencyConverter", methods=["POST", "GET"])
def currency():
  out = sorted(datatypes.calculate_forex(datatypes.get_usd_rates()), key= lambda pair: pair['final_profit'], reverse = True)
  return render_template("currencyConverter.html", output = out)

#flashcards
@app.route("/flashcards", methods=["POST", "GET"])
def flashcards():
  if request.method == "POST":
    question = request.form["question"]
    answer = model.chatgpt(question)
    return render_template("flashcards.html", input = question, output=answer)
  else:

    collection = db.profiles
    events = collection.find({})
    return render_template("flashcards.html", events=events)
  
@app.route("/user-flashcards")
def get_flashcards():
  username = request.cookies.get("username")
  collection = db.profiles
  flashcards = collection.find_one({"username":username})["flashcards"]
  print(flashcards)
  return flashcards




#if successful login/signup, store in cookies and redirect to homepage

# HANDLE POST AND GET for login
@app.route("/")
@app.route("/signup", methods=["POST", "GET"])
def signup():
  if (request.method == "POST"):
    # our collection
    collection = db.profiles
    event = {"username": request.form["username"], "password": request.form["password"]}
    collection.insert_one(event)
    #verify
    response = redirect("/home") #make_response()
    response.set_cookie("username",request.form["username"])
    response.set_cookie("password",request.form["password"])
    
    return response
  else:
    response = make_response(render_template("login.html"))
    response.set_cookie("username", max_age=0)
    response.set_cookie("password", max_age=0)
    return response #render_template("login.html")


# # CLEAR OUT THE EVENTS
# @app.route("/clear", methods=["POST"])
# def clear_events():
#   collection = db.events
#   collection.delete_many({})
#   return render_template("index.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)


