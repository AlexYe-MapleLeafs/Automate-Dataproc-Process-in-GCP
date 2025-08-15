**Automated Process in Dataproc in Google Cloud Platform to Leverage Its Computing Power**

This repository contains a simplified, demonstration version of a real-world GCP project.
It illustrates the structure, configurations, and code required to automate process in **Google Cloud Platform** Dataproc services.

---

## Repository Structure

| File/Folder                         | Purpose                                                                                                                                                                                                                                                                |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`scripts/`**                      | Python scripts containing pyspark scripts for extracting data from multiple sources and loading data into **BigQuery** target tables. <br>_Note: The production environment contains 10+ scripts. This demo includes only a subset for clarity._                       |
| **`jars`**                          | In real project, it contains gcs-connector-hadoop2-2.1.1.jar and spark-3.2-bigquery-0.30.0.jar needed for the process. <br>_Note: jars are not included in repo to reduce sizes, users can download from original websites indicated on txt documents in this folder._ |
| **`miniconda3`**                    | In real project, it contains Miniconda3-py39*23.5.2-0-Linux-x86_64.sh needed for the process. <br>\_Note: minconda are not included in repo to reduce sizes, users can download from original websites indicated on txt document in this folder.*                      |
| **`accp.yaml`**                     | Pipeline configuration file defining build instructions for the container image, including image name, build context, and other ACCP pipeline parameters. <br>_Referenced during pipeline initialization._                                                             |
| **`Dockerfile`**                    | Image build specification defining the base image, system dependencies, and Python packages required to execute the scripts. Miniconda installation is indicated here. <br>_Referenced in `accp.yaml`._                                                                |
| **`dataproc_serverless_01_dag.py`** | **Apache Airflow DAG** for orchestrating and scheduling the end-to-end process. References the container image (in container_image parameter) built from the above files and defines execution logic and scheduling parameters.                                        |

---

## Workflow Overview

1. **Code and Configuration** — Python scripts, configuration files, and dependencies are stored in this repository.
2. **Image Build** — The ACCP pipeline uses `accp.yaml` and `Dockerfile` to build a container image with all required dependencies.
3. **Data Processing** — The container runs Python scripts to fetch, transform, and load data into BigQuery.
4. **Orchestration** — Airflow triggers the container execution according to the schedule defined in `dataproc_serverless_01_dag.py`.

---
