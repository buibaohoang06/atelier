from app import app
from auth import authbp
from index import indexbp

app.register_blueprint(authbp)
app.register_blueprint(indexbp)

if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")