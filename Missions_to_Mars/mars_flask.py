from flask import Flask, jsonify
import scrape_mars

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    dictionary = scrape_mars.scrape()
    return dictionary


if __name__ == '__main__':
    app.run(debug=True)
