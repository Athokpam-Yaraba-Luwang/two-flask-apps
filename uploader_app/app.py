from flask import Flask, render_template, request, redirect, url_for, flash
from google.cloud import storage, firestore
from werkzeug.utils import secure_filename
import uuid, os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret")

BUCKET_NAME = os.environ.get("BUCKET_NAME")
if not BUCKET_NAME:
    raise ValueError("BUCKET_NAME environment variable not set")

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

db = firestore.Client()

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files.get("image")
    title = request.form.get("title", "")
    description = request.form.get("description", "")

    if not file or file.filename == "":
        flash("No file selected")
        return redirect(url_for("index"))

    if not allowed(file.filename):
        flash("Invalid file type")
        return redirect(url_for("index"))

    ext = os.path.splitext(file.filename)[1]
    blob_name = f"{uuid.uuid4().hex}{ext}"

    blob = bucket.blob(blob_name)
    blob.upload_from_file(file.stream, content_type=file.content_type)

    blob.make_public()
    image_url = blob.public_url

    db.collection("cards").add({
        "title": title,
        "description": description,
        "image_url": image_url,
        "created": firestore.SERVER_TIMESTAMP
    })

    flash("Image uploaded successfully!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
