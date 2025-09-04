from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.analyze import analyze_bp
import os

# Point Flask to React build folder
app = Flask(__name__)

# Allow CORS if needed (can restrict origins for production)
CORS(app)

# Register Blueprint
app.register_blueprint(analyze_bp)

# Serve React App
@app.route("/")
def home():
    return {"message": "Amazon Review Analyzer API running!"}



# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) #Render provide $PORT
    app.run(host="0.0.0.0", port=port)

