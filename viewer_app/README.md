Short deploy steps (similar to uploader):
Ensure Firestore in Native mode is enabled in your project.
Deploy with Cloud Run:
gcloud run deploy viewer-app \
  --source=./viewer_app \
  --region=asia-south1 \
  --platform=managed \
  --allow-unauthenticated


Google Cloud setup checklist (quick)
Create a GCP project: gcloud projects create YOUR_PROJECT_ID (or use existing project)
gcloud config set project YOUR_PROJECT_ID
Enable APIs:
gcloud services enable run.googleapis.com storage.googleapis.com firestore.googleapis.com
Create a Storage bucket in same region as Cloud Run (e.g. asia-south1):
gsutil mb -l asia-south1 gs://YOUR_BUCKET_NAME
Initialize Firestore (Console: Firestore -> Create database -> Native mode)
Create a service account with roles: Cloud Run Invoker, Cloud Storage Object Admin (or Storage Object Creator), Firestore User (or appropriate). Use that SA when deploying Cloud Run services.


Notes & next steps
This setup uses blob.make_public() to make uploaded images public. For a production system you should use Signed URLs or lock down bucket access and use IAM properly.
If you'd like, I can:
add a simple /api/cards JSON endpoint in the uploader app,
add pagination or edit/delete features,
or create a single mono-r