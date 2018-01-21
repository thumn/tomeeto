From flask import Flask
app = Flask(__name__)

@app.route(‘/’)
def index():
    return “<h1>Hello, world!</h1>”
@app.route(‘/testing’)
def testing():
    return “<h1>This is another testing page</h1>”
If __name__ == ‘__main__’:
    app.run(debug=True)
