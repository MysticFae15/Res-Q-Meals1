from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- DATABASE CONFIG ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address = db.Column(db.String(250))
    claimed_by = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()

# ---------------------- ROUTES ----------------------
@app.route('/')
def home():
    return "🍽️ Surplus Food Donation Server (Python Flask) is running!"

# ---------------------- DONATION ROUTES ----------------------
@app.route('/donate', methods=['POST'])
def donate():
    data = request.form or request.get_json()  # works with both form and JSON

    new_donation = Donation(
        restaurant_name=data.get("restaurantName", "Restaurant"),
        lat=float(data.get("lat")),
        lng=float(data.get("lng")),
        address=data.get("address", "Unknown")
    )
    db.session.add(new_donation)
    db.session.commit()

    # ✅ Instead of redirecting to thank_you.html, return popup inline
    return """
    <html>
        <head>
            <title>Thank You!</title>
            <script>
                window.onload = function() {
                    alert('🎉 Thank you for your donation! You made a person\\'s day!');
                    window.location.href = '/map';  // redirect back to map after alert
                }
            </script>
        </head>
        <body>
        </body>
    </html>
    """

@app.route('/map')
def map_page():
    return render_template("map.html")  # your map UI

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    app.run(debug=True)
