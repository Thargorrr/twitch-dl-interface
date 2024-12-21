from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')


if __name__ == '__main__':
    app.run(debug=True)
