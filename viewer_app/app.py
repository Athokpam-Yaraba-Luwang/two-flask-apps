from flask import Flask, render_template, jsonify
from google.cloud import firestore
import os

app = Flask(__name__)
db = firestore.Client()

@app.route("/")
def show_cards():
    docs = db.collection("cards").order_by("created", direction=firestore.Query.DESCENDING).stream()
    cards = [doc.to_dict() for doc in docs]
    return render_template("view.html", cards=cards)

@app.route("/api/cards")
def get_cards_api():
    docs = db.collection("cards").order_by("created", direction=firestore.Query.DESCENDING).stream()
    cards = []
    for doc in docs:
        data = doc.to_dict()
        # Convert timestamp to string for JSON serialization
        if data.get("created"):
            data["created"] = data["created"].isoformat()
        cards.append(data)
    return jsonify(cards)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
