from flask import Flask, render_template
render_template
from stocks import get_price
from weather import get_temperature

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    if name is None:
        name = 'World'
    name = name.capitalize()
    return render_template('hello.html', name=name)


@app.route('/square/<int:n>')
def square(n):
    return f'{n} squared is {n ** 2}'

# Create a another route that shows the current price of any stock or current temperature of any city. 
@app.route('/stock/<ticker>')
def stock_price(ticker):
    price = get_price(ticker)
    return f'The current price of {ticker.upper()} is ${price:.2f}'

@app.route('/weather/<city>')
def weather(city):
    temp = get_temperature(city)
    return f''




if __name__ == '__main__':
    app.run(debug=True)
