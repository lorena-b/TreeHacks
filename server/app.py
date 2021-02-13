"""
Flask API
"""
from flask import Flask, jsonify, request, render_template
import sentiment

app = Flask(__name__)


@app.route('/')
def index() -> object:
    """Index Route
    """
    return render_template('index.html')


@app.route('/sentiment', methods=['GET'])
def get_sent_data() -> object:
    """Route for sentiment

    Needs to receive input from front-end "stock topic"
    """
    sentiment_data = sentiment.sentiment_manager()
    return jsonify({'test': 'random test json'})


if __name__ == '__main__':
    app.run(debug=True)
