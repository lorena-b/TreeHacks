"""
Flask API
"""
from flask import Flask, jsonify, request, render_template
import sentiment

app = Flask(__name__, template_folder='../client')


@app.route('/')
def index():
    """Index Route
    """
    return render_template('index.html')


@app.route('/', methods=['POST'])
def get_sent_data():
    """Route for sentiment

    Needs to receive input from front-end "stock topic"
    """
    topic = request.form['text']
    sentiment_data = sentiment.sentiment_report(topic)
    return jsonify(sentiment_data)


if __name__ == '__main__':
    app.run(debug=True)
