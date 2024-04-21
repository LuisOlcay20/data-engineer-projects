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

#Bigquery
resource "google_bigquery_dataset" "dw_bigquery" {
  dataset_id = "stadium_data"
  location = "southamerica-east1"
}

resource "google_bigquery_table" "sa_stadium_table" {
  dataset_id = google_bigquery_dataset.dw_bigquery.dataset_id
  table_id   = "southamerica-stadiums" 
  deletion_protection = false

}
