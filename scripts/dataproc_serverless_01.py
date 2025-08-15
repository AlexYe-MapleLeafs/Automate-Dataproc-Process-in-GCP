# Use Command below in workstation terminal to submit and run pyspark script
#######################################################################################################################
# 		gcloud dataproc batches submit pyspark ~/gcp_general_scripts/dataproc/image/scripts/dataproc_example_02.py \
# 		--batch="dataproctest07" \
# 		--project="cidat-10040-int-445d" \
# 		--region="us-central1" \
# 		--subnet="projects/cidat-10040-int-445d/regions/us-central1/subnetworks/dataproc-primary-usc1" \
# 		--kms-key="projects/cidat-10040-int-445d/locations/us-central1/keyRings/cidat-10040-int-445d-usc1/cryptoKeys/dataproc" \
# 		--tags='dataproc' \
# 		--service-account="dataproc@cidat-10040-int-445d.iam.gserviceaccount.com" \
# 		--impersonate-service-account="workstations@cidat-10040-int-445d.iam.gserviceaccount.com" \
# 		--deps-bucket="gs://us-central1-i-comm-ana-oaud-18d99f8e-bucket" \
#       --jars="gs://hadoop-lib/gcs/gcs-connector-hadoop2-2.1.1.jar"
#######################################################################################################################


from pyspark.sql import SparkSession
 
spark = SparkSession.builder.getOrCreate()

#######################################################################################################################
### REPLACE WITH YOUR PROJECT/JOB SPECIFIC VALUES ###
PROJECT_ID  = 'cidat-10040-int-445d'
 
# GCS Bucket Path - for input data on GCS
iGCS_BaseDir = "gs://us-central1-i-comm-ana-oaud-18d99f8e-bucket/data/AlexYe"
 
# GCS Bucket Path - for output data on GCS
oGCS_BaseDir="gs://us-central1-i-comm-ana-oaud-18d99f8e-bucket/data/AlexYe"
 
# GCS Bucket Name - temporary space for queueing output data on GCS before writing out to BQ tables in "indirect" mode
TempGCSBucket = "us-central1-i-comm-ana-oaud-18d99f8e-bucket"
 
# BQ Dataset ID - for input data on BQ
iBQ_DatasetID = "ceba_report_interactive"
 
# BQ Dataset ID - for output data on BQ
oBQ_DatasetID = "z_team_testing_interactive"
 
# BQ Dataset ID - temporary space for materializing SQL-query results on BQ tables before reading into Spark DataFrame
tmpBQ_DatasetID = "z_team_testing_interactive"

#######################################################################################################################

spark.conf.set("viewsEnabled", "true")
spark.conf.set("materializationProject", PROJECT_ID)       # Set to your consumer project ID
spark.conf.set("materializationDataset", tmpBQ_DatasetID)
spark.conf.set("temporaryGcsBucket", TempGCSBucket)

#######################################################################################################################
# iBQ_acct  = f"{PROJECT_ID}.{iBQ_DatasetID}.ceba_20250228_data"
iBQ_acct  = "cidat-10040-int-445d.ceba_report_interactive.ceba_20250228_data"
# sql_query = """
#      SELECT businesseffectivedate, oll_number, ic_gn_addr1 FROM `cidat-10040-int-445d.ceba_report_interactive.ceba_20250228_data`
#      """
# df_sql = spark.read.format("bigquery").load(sql_query)
# df_sql.show(5, truncate=False)

df_sql = spark.read.format("bigquery").option("table", iBQ_acct).load()

#######################################################################################################################

output_table = f"{PROJECT_ID}.{oBQ_DatasetID}.dataproc_02_example"
df_sql.write.mode("overwrite").format("bigquery").save(output_table)
