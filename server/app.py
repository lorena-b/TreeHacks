from flask import Flask, jsonify, request, render_template  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getdata', methods=['GET'])    
def get_data():
    return jsonify({'test': 'random test json'})

if __name__ == '__main__':
    app.run(debug=True)