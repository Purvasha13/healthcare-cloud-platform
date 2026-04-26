from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

app = Flask(__name__)

app.register_blueprint(routes)
@app.route("/")
def home():
    return "Flask is running successfully!"
