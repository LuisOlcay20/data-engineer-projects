# Cloud ETL Orchestration

## Overview
This project is designed to orchestrate the Extract, Transform, Load (ETL) process in the cloud using Google Cloud Platform services. It automates the process of extracting data from a source, transforming it, and loading it into a destination storage system, such as BigQuery.

## Components
- **Extractor**: Responsible for extracting data from the source and loading it into Cloud Storage.
- **Cloud Functions**: Performs data transformations and loads the transformed data into BigQuery.
- **Orchestrator (Cloud Composer)**: Orchestrates the ETL pipeline, scheduling and coordinating the execution of tasks using Apache Airflow.
- **Terraform**: Defines and manages the necessary infrastructure on Google Cloud Platform.

## Project Structure
- `extractor/`: Contains scripts for extracting data from the source and its dependencies.
- `cloud_functions/`: Contains Cloud Functions for data transformation and loading into BigQuery.
- `orchestrator/`: Includes the DAG (Directed Acyclic Graph) definition and its dependencies for orchestrating the ETL workflow.
- `terraform/`: Contains Terraform configuration files for defining and managing GCP infrastructure.

## Getting Started
1. Set up Google Cloud Platform account and project.
2. Install necessary tools (Google Cloud SDK, Terraform).
3. Configure authentication for GCP.
4. Create required resources (Cloud Storage bucket, BigQuery dataset, etc.).
5. Deploy infrastructure using Terraform.
6. Upload extractor script to Cloud Storage.
7. Deploy Cloud Functions for transformation and loading.
8. Create and schedule DAG in Cloud Composer.


