import os
from datetime import datetime, timedelta, date

from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator,
    DataprocDeleteBatchOperator,
    DataprocGetBatchOperator,
)


# Define base environment variables for batch operator
ENV_ID = "interactive" # Set environment type
DAG_ID = "dataproc_serverless_example_02"
PROJECT_ID = "cidat-10040-int-445d"  # Set GCP project
REGION = "us-central1"

# Make the batch ID name different each time, because batch ID cannnot overwrite
today = datetime.today()
today = today.strftime('%Y%m%d%H%M%S')
BATCH_ID = "dp-example-" + today

BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": "gs://us-central1-i-comm-ana-oaud-18d99f8e-bucket/dependencies/dataproc_example_02.py",  # Path to GCS bucket containing Py job files
        # "jar_file_uris": ["gs://spark-lib/bigquery/spark-3.2-bigquery-0.30.0.jar"],
    },
    "environment_config": {
        "execution_config": {
            "service_account": "dataproc@cidat-10040-int-445d.iam.gserviceaccount.com",  # Change Dataproc Service Account based on the project, see IAM page.
            "subnetwork_uri": "projects/cidat-10040-int-445d/regions/us-central1/subnetworks/dataproc-primary-usc1",  # Subnet names can be dataproc-primary-usc1 or dataproc-primary-use4
            "network_tags": ["dataproc"],  # Mandatory for proper network communications
            "kms_key": "projects/cidat-10040-int-445d/locations/us-central1/keyRings/cidat-10040-int-445d-usc1/cryptoKeys/dataproc"
        }
    },
    # Add Image location (pull tag)
    "runtime_config": {"container_image": "us-central1-docker.pkg.dev/cida-tenant-deploy-vx9m/cidat-10040/dataproc-image-02:0.0.2"}
}
 
# Create Airflow DAG
with models.DAG(
    DAG_ID,
    schedule_interval='0 12 * * *',
    start_date=datetime(2025, 3, 17),
    catchup=False,
    # tags=[ENV_ID, "dataproc"],
) as dag:
    # Create a Dataproc Batch operator
    create_batch = DataprocCreateBatchOperator(
        task_id="dataproc_01",
        project_id=PROJECT_ID,
        region=REGION,
        batch=BATCH_CONFIG,
        batch_id=BATCH_ID,
        impersonation_chain=["dataproc@cidat-10040-int-445d.iam.gserviceaccount.com"],  # Change Dataproc Service Account based on the project, see IAM page.
    )
create_batch
