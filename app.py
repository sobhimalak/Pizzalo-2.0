from shop import app
from flask_fontawesome import FontAwesome

fa = FontAwesome(app)
if __name__ == "__main__":
    app.run(debug = True)