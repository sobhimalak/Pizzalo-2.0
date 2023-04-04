from shop import app
import os
from flask_fontawesome import FontAwesome

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port=int(os.environ.get('PORT',5000)))