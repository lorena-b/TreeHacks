"""
Flask API
"""
from flask import Flask, jsonify, request, render_template, redirect, url_for
import sentiment
import basis
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='../templates/static', static_folder='../templates/static')
Bootstrap(app)


@app.route('/')
def index():
    """Index Route
    """
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def get_sent_data():
    """Route for sentiment

    Needs to receive input from front-end "ex: stock topic"
    """
    if request.method == 'POST':
        topic = request.form.get('text')

        res = []
        sentiment_data = sentiment.sentiment_report(topic)
        trend_data = basis.montharray(topic, 'stocks', basis.valuedicmonth)
        res.append(sentiment_data)
        res.append(trend_data)

        return render_template('base.html', data=res, topic=topic)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
