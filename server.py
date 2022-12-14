from app import app
from auth import authbp

app.register_blueprint(authbp)

if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")