from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Variables to pass to the HTML template
    title = "孫盈盈"
    description = "This is my home page"
    items = ["t113590050@ntut.org.tw", "113590050", "原神啟動", "CSS"]

    # Render the template and pass the variables
    return render_template('index.html', title=title, description=description, items=items)

if __name__ == '__main__':
    app.run(debug=True)
