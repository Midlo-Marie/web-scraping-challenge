  
#################################################
# MongoDB and Flask Application
#################################################

# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_Midlomarie

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# PyMongo Connection Setup for local connection
#################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    print("from the Mongo pull")
    print(mars)
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars_Midlomarie.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars_Midlomarie.scrape_all()
    print(f"Retrieved data from scrape_mars  {mars_data}")
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)
