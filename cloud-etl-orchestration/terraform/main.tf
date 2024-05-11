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
resource "google_storage_bucket" "gcs_chilean_football" {
  name          = "chilean_football_bucket"
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

# BigQuery Dataset
resource "google_bigquery_dataset" "dw_bigquery" {
  dataset_id = "chilean_premier_league_2024"
  location   = "southamerica-east1"
}

# BigQuery Table for Teams
resource "google_bigquery_table" "teams_2024" {
  dataset_id = google_bigquery_dataset.dw_bigquery.dataset_id
  table_id   = "teams_2024"
  deletion_protection = false

  schema = jsonencode([
    {
      name = "team_id",
      type = "INTEGER",
      mode = "REQUIRED"
    },
    {
      name = "country",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "venue_city",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "name",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "founded",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "venue_name",
      type = "STRING",
      mode = "NULLABLE"
    }
  ])
}

# BigQuery Table for Scorers Information
resource "google_bigquery_table" "scorers_information_2024" {
  dataset_id = google_bigquery_dataset.dw_bigquery.dataset_id
  table_id   = "scorers_information_2024"
  deletion_protection = false

  schema = jsonencode([
    {
      name = "firstname",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "lastname",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "age",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "nationality",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "height",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "weight",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "injured",
      type = "BOOLEAN",
      mode = "NULLABLE"
    },
    {
      name = "team",
      type = "STRING",
      mode = "NULLABLE"
    }
  ])
}

# BigQuery Table for Scorers Statistics
resource "google_bigquery_table" "scorers_statistics_2024" {
  dataset_id = google_bigquery_dataset.dw_bigquery.dataset_id
  table_id   = "scorers_statistics_2024"
  deletion_protection = false

  schema = jsonencode([
    {
      name = "firstname",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "lastname",
      type = "STRING",
      mode = "NULLABLE"
    },
    {
      name = "goals",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "assists",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "conceded",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "penalty_scored",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "penalty_missed",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "total_passes",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "key_passes",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "total_duels",
      type = "INTEGER",
      mode = "NULLABLE"
    },
    {
      name = "duels_won",
      type = "INTEGER",
      mode = "NULLABLE"
    }
  ])
}
