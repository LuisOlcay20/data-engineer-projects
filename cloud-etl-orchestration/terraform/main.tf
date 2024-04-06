terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.22.0"
    }
  }
}

provider "google" {
  project = "cloud-etl-orchestration"
  region  = "southamerica-east1"
}

#GCS: Bucket
resource "google_storage_bucket" "gcs_stadium_bucket" {
  name          = "stadiums_bucket"
  location      = "southamerica-east1"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

#GCF: Functions
resource "google_cloudfunctions_function" "gcf_transform_data" {
  name        = "transform_stadium_data"
  description = "Transform data when the file arrives to the bucket"
  runtime     = "nodejs14"

}


resource "google_cloudfunctions_function" "gcf_load_data" {
  name        = "load_stadium_data"
  description = "Load data to bigquery"
  runtime     = "nodejs14"
  
}

#Bigquery
resource "google_bigquery_dataset" "dw_bigquery" {
  dataset_id = "stadium_data"
  location = "southamerica-east1"
}

#GCC: Composer/Airflow
resource "google_composer_environment" "orchestrator_pipeline" {
  name   = "orchestrator_pipeline"
  region = "southamerica-east1"
}
