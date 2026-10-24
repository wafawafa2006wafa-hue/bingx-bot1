import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "BingX Bot & Radar is running 24/7 successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
