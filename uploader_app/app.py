from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import uuid, os
from google.cloud import storage, firestore

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'your-bucket-name')


# Clients (uses Application Default Credentials)
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

db = firestore.Client()


@app.route('/')
def index():
	return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
	if 'image' not in request.files:
		flash('No image provided')
		return redirect(url_for('index'))

	file = request.files['image']
	title = request.form.get('title', '')
	description = request.form.get('description', '')

	if file.filename == '':
		flash('No selected file')
		return redirect(url_for('index'))

	filename = secure_filename(file.filename)
	ext = os.path.splitext(filename)[1] or '.jpg'
	blob_name = f"{uuid.uuid4().hex}{ext}"

	blob = bucket.blob(blob_name)
	blob.upload_from_file(file.stream, content_type=file.content_type)

	# Make public (simple option). In production consider Signed URLs or proper IAM.
	try:
		blob.make_public()
		image_url = blob.public_url
	except Exception:
		# fallback to storage URL form
		image_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{blob_name}"

	# Save metadata to Firestore
	data = {
		'title': title,
		'description': description,
		'image_url': image_url,
		'blob_name': blob_name,
		'created': firestore.SERVER_TIMESTAMP
	}

	db.collection('cards').add(data)

	flash('Uploaded successfully')
	return redirect(url_for('index'))

if __name__ == '__main__':
	# For local dev use PORT=8080
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port, debug=True)