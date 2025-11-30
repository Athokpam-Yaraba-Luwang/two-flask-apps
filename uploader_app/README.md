Short instructions for uploader app (setup & deploy):
1.Create a GCP project and enable Cloud Run, Cloud Storage, Firestore APIs.
2.Create a GCS bucket and set BUCKET_NAME environment variable before running.
3.Locally export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json for ADC.

4.To build & run locally:

cd uploader_app
pip install -r requirements.txt
export BUCKET_NAME=your-bucket-name
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
python app.py

5.To deploy to Cloud Run (from repo root):

# build & deploy
gcloud run deploy uploader-app \
--source=./uploader_app \
--region=asia-south1 \
--platform=managed \
--allow-unauthenticated