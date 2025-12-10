# lottery_app.py
from flask import Flask, render_template
from scraper import get_latest_power_lottery

app = Flask(__name__)

@app.route("/")
def index():
    data = get_latest_power_lottery()

    if "error" in data:
        return f"<h1>爬蟲發生錯誤：</h1><p>{data['error']}</p>"

    return render_template("index.html",
                           main=data["main"],
                           special=data["special"])

if __name__ == "__main__":
    app.run(debug=True)
