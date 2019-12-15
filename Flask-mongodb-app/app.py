from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    mars_data = mongo.db.scape_responces.find_one()
    return render_template("index.html", data=mars_data)


@app.route("/scrape")
def scrape_mars():
    data = scrape.scrape()
    mongo.db.scape_responces.update({}, data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

